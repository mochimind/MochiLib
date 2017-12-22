import json

from . import token
from . import tdistengine


QUERY_TAG = "query"
EXIT_TAG = "exit"


class Command:
	def __init__(self, data_str):
		self.valid = False
		self.error_str = "invalid command: " + data_str

	def isValid(self):
		return self.valid

	def getError(self):
		return error_str


class QueryCommand(Command):
	INPUT_TAG = "input"
	RESULT_TAG = "result"
	INSERT_TAG = "insert"

	RESULT_TYPE_DATA = "data"
	RESULT_TYPE_ANOMALY = "anomaly"

	def __init__(self, data_str):
		super().__init__("")

		# now let's parse the data string to see if it's valid JSON
		try:
			data = json.loads(data_str)
			self.error_str = "server error"
		except ValueError as e:
			self.data = ""
			print (e)
			self.error_str = "invalid json string: " + data_str
			return

		# input is valid JSON, let's try to get the mandatory arguments
		if not QueryCommand.INPUT_TAG in data:
			self.error_str = "missing required tag: " + QueryCommand.INPUT_TAG
			return
		else:
			self.input = data[QueryCommand.INPUT_TAG]

		# now let's populate the optional arguments
		if QueryCommand.RESULT_TAG in data and self.resultTypeValid(data[QueryCommand.RESULT_TAG]):
			self.result_type = data[QueryCommand.RESULT_TAG]
		else:
			self.result_type = QueryCommand.RESULT_TYPE_ANOMALY
		if QueryCommand.INSERT_TAG in data and self.insertTagValid(data[QueryCommand.INSERT_TAG]):
			self.insert_type = data[QueryCommand.INSERT_TAG]

		self.valid = True
		self.error_str = ""

	def resultTypeValid(self, result_type):
		if result_type == QueryCommand.RESULT_TYPE_DATA or result_type == QueryCommand.RESULT_TYPE_ANOMALY:
			return True
		return False

	def insertTagValid(self, insert_tag):
		if insert_tag == True or insert_tag == False:
			return True
		return False

	def execute(self):
		self.valid = False
		data = token.tokenize(token.TokenType.WordData, self.input).compress()
		if self.insert_type == True:
			data.save()
		if self.result_type == QueryCommand.RESULT_TYPE_DATA:
			self.output = json.dump(data)
			self.valid = True
		elif self.result_type == QueryCommand.RESULT_TYPE_ANOMALY:
			data = tdistengine.GetAnomalies(data)
			self.output = json.dump(data.toJSON())
			self.valid = True


class ExitCommand(Command):
	def __init__(self, data_str=""):
		self.valid = True


def GetCommand(raw_str):
	first_space = raw_str.find(' ')
	check_str = raw_str
	if first_space != -1:
		# there was a space, check the first token
		check_str = raw_str[:first_space]
	print ("first space: ", first_space, " ", check_str)
	if check_str == QUERY_TAG:
		return QueryCommand(raw_str[first_space:])
	elif check_str == EXIT_TAG:
		return ExitCommand(raw_str[first_space:])
	else:
		return Command(raw_str)

