from http.client import HTTPConnection
import json.decoder
from time import sleep

DEFAULT_HTTP_PORT = 80


class IPConverter:
    COUNTRY = 'country'
    PROVINCE = 'province'
    CITY = 'city'
    ISP = 'isp'
    STAT = 'stat'
    IP = 'ip'
    STAT_TRUE = 200
    STAT_FALSE = 100
    # ip list >>> result list<dict>
    # 数据交换协议：{country, province, city, isp, ip, stat}
    def convert(self, ip_list):
        pass


class DatabaseIPConverter(IPConverter):  # TODO 稍后完成，基于 sqlite3
    def convert(self, ip_list):
        pass

    def update_ip(self, ip_info_list):
        pass


class PersistenceCachedIPConverter(IPConverter):
    def __init__(self, cached_converter, ip_converter):
        """
        cached_converter: database
        ip_converter: taobao, ipip.net
        """
        self.__cached_converter = cached_converter
        self.__ip_converter = ip_converter

    def convert(self, ip_list):
        not_cached_ips = []
        result = []
        db_result = self.__cached_converter.convert(ip_list)
        for r in db_result:
            if self.STAT_TRUE == r.get(self.STAT):
                result.append(r)
            else:
                not_cached_ips.append(r[self.IP])
        new_ips = self.__ip_converter.convert(not_cached_ips)
        self.__cached_converter.update(new_ips)
        result.extend(new_ips)
        return result


class TaobaoIPConverter(IPConverter):
    def __init__(self, host, url):
        self.__host = host
        self.__url = url
        self.__decoder = json.decoder.JSONDecoder()

    def convert(self, ip_list):
        ip_result = []
        for ip in ip_list:
            ip_result.append(self.__do_convert(ip))
            sleep(0.29)
        return ip_result

    def __do_convert(self, ip):
        connection = HTTPConnection(self.__host, port=DEFAULT_HTTP_PORT, timeout=30)
        url = self.__url + ip
        json_data = None
        try:
            connection.request(method='GET', url=url)
            response = connection.getresponse()
            json_data = response.read()
        except Exception as e:
            print(e.args)
        finally:
            try:
                connection.close()
            except Exception as e:
                pass

        if not json_data:
            return {self.IP: ip, self.STAT: self.STAT_FALSE}
        json_data = str(json_data, encoding='unicode_escape')
        result = self.__json2dict(json_data, ip)
        return result

    def __json2dict(self, json_line, ip):
        data = self.__decoder.decode(json_line).get('data', None)
        result = {}
        if data:
            result.update({self.COUNTRY: data.get('country')})
            result.update({self.PROVINCE: data.get('region')})
            result.update({self.CITY: data.get('city')})
            result.update({self.ISP: data.get('isp')})
            result.update({self.IP: ip})
            result.update({self.STAT: self.STAT_TRUE})
            print(result)
        return result


class IPIPNETIPConverter(IPConverter):  # TODO 稍后完成，基于 ipip.net
    pass


TAOBAO_HOST = 'ip.taobao.com'
TAOBAO_URL = '/service/getIpInfo.php?ip='
taobao_ip_converter = TaobaoIPConverter(TAOBAO_HOST, TAOBAO_URL)
db_ip_converter = DatabaseIPConverter()
cached_ip_converter = PersistenceCachedIPConverter(db_ip_converter, taobao_ip_converter)


def get_ip_from_tb():
    ip_list = []
    with open('ip.log', 'r') as stream:
        for line in stream.readlines():
            ip_list.append(line.strip())

    print('Read ip file successful')
    locations = taobao_ip_converter.convert(ip_list)
    for location in locations:
        print(location)


if __name__ == '__main__':
    get_ip_from_tb()
