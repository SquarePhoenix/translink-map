import requests
from ConfigParser import SafeConfigParser
from bs4 import BeautifulSoup

parser = SafeConfigParser()
parser.read('api.config')
APIKEY = parser.get('api', 'apiKey')


class QueryBus:

    def getBusesByRoute(self, route):
        r = self.__apiQuery(
            'http://api.translink.ca/rttiapi/v1/buses',
            {'routeNo': route}, True)
        return r.json()

    def isApiOnline(self):
        r = self.__apiQuery(
            'http://api.translink.ca/rttiapi/v1/status/location',
            None, False)
        xml = BeautifulSoup(r.text, 'xml')
        return xml.find('Value').string == 'Online'

    def __apiQuery(self, url, params, useJson):
        try:
            if not params:
                params = dict()
            params['apikey'] = APIKEY
            if useJson:
                headers = {'accept': 'application/JSON'}
            else:
                headers = None
            r = requests.get(url, headers=headers, params=params)
        except Exception, e:
            raise e
        else:
            if r.status_code != requests.codes.ok:
                r.raise_for_status()
            return r
