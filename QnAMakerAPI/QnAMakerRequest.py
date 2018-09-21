import requests


class QnAMakerRequest:
    mainUrl = "https://westus.api.cognitive.microsoft.com/qnamaker/v2.0/knowledgebases/1df2ec54-c653-44c3-9fc3-33fbef695b44"
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '558d2204992b4a59bba419e98bd2d39d',
    }

    def __init__(self, method, payload=None):
        if method == '/generateAnswer':
            self._query = requests.post(QnAMakerRequest.mainUrl + method, headers=QnAMakerRequest.headers, json=payload)
            try:
                self._query.raise_for_status()
            except Exception:
                self._query = self._query.json()['error']
                self._isValid = False
            else:
                self._query = self._query.json()['answers'][0]
                self._isValid = True
        # elif method == 'update':
        #     self._query = requests.patch(QnAMakerRequest.mainUrl, headers=QnAMakerRequest.headers, json=payload)
        # elif method == 'publish':
        #     self._query = requests.put(QnAMakerRequest.mainUrl, headers=QnAMakerRequest.headers)

    @property
    def query(self):
        return self._query

    @property
    def isValid(self):
        return self._isValid
