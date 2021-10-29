import re
import json
import logging
from requests import session


class ProxyApi(object):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) "
                                      "Chrome/19.0.1055.1 Safari/535.24"
                        }
        self._session = session()
        self.proxies = {
                        "http": "http://127.0.0.1:1087",
                        "https": "https://127.0.0.1:1087"
                    }
        self._token = "axm4YZIL9xN8US8v1586314574247"

    def _get(self, url, **query_parameters):

        # response = self._session.get(url, headers=self.headers, params=query_parameters, timeout=(30, 120))
        response = self._session.get(url, headers=self.headers, proxies=self.proxies, params=query_parameters, timeout=(30, 120))
        return response

    def extract_proxy(self, number=1):
        print("11111111111111")

        # url = "http://list.rola-ip.site:8088/user_get_ip_list"
        url = "http://tiqu.linksocket.com:81/abroad"
        # http://tiqu.linksocket.com:81/abroad?num=1&type=1&lb=1&sb=0&flow=1&regions=&n=0
        # token = "axm4YZIL9xN8US8v1586314574247"
        # token = "euQy6orCvWlmuSmz1586773688372"
        # params = {
        #     "token": self._token,
        #     "qty": number,
        #     "country": "",
        #     "time": 10,
        #     "format": "json",
        #     "protocol": "http",
        #     "filter": 1
        # }
        params = {
            "num": number,
            "type": 2,
            "lb": 1,
            "sb": 0,
            "flow": 1,
            "regions": "",
            "n": 0
        }
        response = self._get(url, **params)
        # print(response.status_code)
        content = response.json()
        print(content)
        if content["code"] == 0 and content["data"]:
            logging.info("获取可用代理，代理响应信息：{}".format(content))
            return content["data"]
        else:
            logging.error("尚未获取代理， 代理响应信息：{}".format(content))
            return content["data"]

    def get_real_info(self, proxy):
        def get_city(city_content):
            pattern = re.compile('var returnCitySN = ({.*});')
            patterns = pattern.match(city_content)
            dict_city = json.loads(patterns.group(1))
            return dict_city
        url = "https://pv.sohu.com/cityjson"
        proxies = {'http': "http://{}".format(proxy), 'https': "https://{}".format(proxy)}
        try:
            response = self._session.get(url, headers=self.headers, proxies=proxies)
            content = response.content
            if 200 == response.status_code:
                logging.info("获取代理真实信息：{}".format(content))
                return get_city(content.decode(encoding="gbk"))
            else:
                return None
        except Exception as msg:
            logging.exception("代理信息提取异常，异常信息：{}".format(msg))
            return None

    def add_whitelist(self, local_ip, remark=None):
        url = "http://admin.rola-ip.site/user_add_whitelist"
        params = {
            "token": self._token,
            "remark": remark,
            "ip": local_ip
        }
        self._get(url, **params)
