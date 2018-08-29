import requests
import json


class ElJurRequest:
    mainUrl = 'https://api.eljur.ru/api'
    params = {
        'devkey': '8227490faaaa60bb94b7cb2f92eb08a4',
        'vendor': 'hselyceum',
        'out_format': 'json'
    }

    def __init__(self, method):
        self._query = requests.get(ElJurRequest.mainUrl + method, params=ElJurRequest.params)
        self.request_processing()

    def request_processing(self):
        try:
            self._query.raise_for_status()
        except requests.exceptions.HTTPError:
            try:
                self._query = self._query.json()
            except json.decoder.JSONDecodeError:
                self._query = 'Ошибка кодировки'
            else:
                self._query = self._query['response']['error'].capitalize()
            finally:
                self._is_valid = False
        else:
            try:
                self._query = self._query.json()
            except json.decoder.JSONDecodeError:
                self._query = 'Ошибка кодировки'
            else:
                self._query = self._query['response']['result']
            finally:
                self._is_valid = True

    @property
    def query(self):
        return self._query

    @property
    def is_valid(self):
        return self._is_valid
