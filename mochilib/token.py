from enum import Enum
from . import config
import re
import pymongo

NameDB = {}
IDDB = {}


class AnomalyToken:
	def __init__(self, token, percent_strength=0, frequency_strength=0):
		self.token = token
		self.percentage_strength = percent_strength
		self.frequency_strength = frequency_strength

class TokenType(Enum):
	word = 0
	punctuation = 1
	number = 2
	invalid = 3


class AnomalyTokenList:
	def __init__(self):
		self.anomalies = []

	def add(self, anomaly):
		self.anomalies.append(anomaly)


class Token:
	def __init__(self, word="", id=0, token_type=TokenType.invalid):
		self.word = word
		self.id = id if id != 0 else GetTokenByString(word)
		self.token_type = GetType(word) if token_type == TokenType.invalid else token_type
		if self.id == 0:
			# we've never seen this word before, let's save it
			self.save()

	def save(self):
		if NameDB.get(word) != None:
			return
		client = pymongo.MongoClient(config.server, username=config.user, password=config.password)
		db = client.mochi
		new_symbol = {'text': self.word, 'type': self.token_type}
		self.id = db.symbols.insert_one(new_symbol).inserted_id


def GetType(_str):
	if _str.length == 0:
		return TokenType.invalid
	# check if there is a non 'word' character
	if re.match("[^\a-zA-z'-]", _str) != None and _str != "-" and _str != "'":
		# check if this is a number
		if re.match("[^\d.]", _str) != None and _str != ".":
			# if not a number, then must be punctuations
			return TokenType.punctuation
		else:
			return TokenType.number
	else:
		return TokenType.word

def Initialize():
	client = pymongo.MongoClient(config.server, username=config.user, password=config.password)
	db = client.mochi
	for iter in list(db.symbols.find()):
		tok = Token(iter.name, iter.id, iter.type)
		NameDB[iter.name] = tok
		IDDB[iter.id] = tok


def GetTokenByID(_id):
	return NameDB.get(_id) or 0

def GetTokenByString(_str):
	return IDDB.get(_str) or 0


class CompressedTokenList:
	def __init__(self):
		self.tokens = {}
		self.words = 0

	def add(tok):
		if tok not in self.tokens:
			self.tokens[token] = 0
		self.tokens[token] += 1
		self.words += 1

	def __repr__(self):
		outstr = "["
		for token in self.tokens:
			if len(outstr) != 1:
				outstr += ',' + token
			else:
				outstr += token
		return 'CTL: ' + outstr + ']'

	def save(self):
		client = pymongo.MongoClient(config.server, username=config.user, password=config.password)
		db = client.mochi
		new_list = {}
		db.datapoints.insert_one(self.tokens)
		

class TokenList:
	def __init__(self):
		self.tokens = []
		self.words = 0

	def add(self, data):
		self.tokens.append(data)
		self.words += 1

	def compress(self):
		ctl = CompressedTokenList()
		for tok in self.tokens:
			ctl.add(tok)
		return ctl

	def __repr__(self):
		outstr = "["
		for token in self.tokens:
			if len(outstr) != 1:
				outstr += ',' + token
			else:
				outstr += token
		return "TokenList: " + outstr + '], self.words'


class TokenType(Enum):
	CharData = 1
	WordData = 2
	CSVData = 3


def tokenize(type, data):
	if type == TokenType.CharData:
		return parseCharData(data)
	elif type == TokenType.WordData:
		return parseWordData(data)
	elif type == TokenType.CSVData:
		return parseCSV(data)
	else:
		print("error: type not supported" + type)
	return None


def parseCharData(data):
	print("error: char lists currently not implemented")
	return None


def parseCSV(data):
	print("error: CSV currently not implemented")
	return None


def parseWordData(data):
	tl = TokenList()
	# first remove all symbols except ' - we won't be working with them
	# TODO: this code doesn't filter out '_', investigate if this is an issue
	processed_data = re.sub("[^\w']", " ", data)
	# TODO: implement numbers and punctuation
	# remove numbers, we're not handling them right now
	processed_data = re.sub("\d", "", processed_data)

	# now split into list of tokens
	processed_data = processed_data.split()
	for tok in processed_data:
		# remove ' from the beginning or end of strings - maybe it'd be faster to not use regex
		tok = re.sub("^'|'$", "", tok)
		if len(tok.strip()) != 0:
			tl.add(Token(tok))

	return tl
