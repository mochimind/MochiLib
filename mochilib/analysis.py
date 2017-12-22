import json

from MochiLib import token


DATAPOINT_RESULT = "data"
ANOMALY_RESULT = "anomaly"
ID_RESULT = "id"


class Analysis:
    def __init(self, data):
        try:
            self.data = json.loads(data)
            self.resultStr = "server error"
        except ValueError as e:
            self.data = ""
            self.resultStr = "invalid json string"

    def handleAnalyze(self):
        if self.data == "":
            return False

        # get parameters
        if not hasattr(self.data, "data"):
            self.resultStr = "no data provided"
            return False

        if hasattr(self.data, "result") and self.isValidCommand(self.data['result']):
            command = self.data['result']
        else:
            command = DATAPOINT_RESULT

        if hasattr(self.data, "insert") and isinstance(self.data, bool):
            insert = self.data['insert']
        else:
            insert = True

        if hasattr(self.data, 'get_exact') and isinstance(self.data, bool):
            get_exact = self.data['get_exact']
        else:
            get_exact = False

        # process the data
        data_ctl = mochitoken.CompressedTokenList()
        data_ctl.compress(mochitoken.tokenize(self.data))

    def getResultString(self):
        return self.resultStr

    def isValidResult(self, result):
        if result == DATAPOINT_RESULT or result == ANOMALY_RESULT or result == ID_RESULT:
            return True

        return False

