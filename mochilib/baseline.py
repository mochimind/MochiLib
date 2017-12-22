import statistics


def GetCurrentBaseline():
	return None

def UpdateBaseline():
	print ("not implemented")

class BaselineToken:
	# takes as input a list of numbers
	def __init__(self, observations=None):
		self.data = ""
		self.mean = 0
		self.stdev = 0
		self.n = 0

		if observations is not None:
			self.mean = statistics.mean(observations)
			self.stdev = statistics.stdev(observations)
			self.n = len(observations)


class Baseline:
	def __init__(self, data=None):
		self.tokens = {}
		self.datapoints = 0

		self.words = 0
		self.unique_words = 0
		self.average_mean = 0
		self.average_frequency = 0
		self.stdev_mean = 0
		self.stdev_frequency = 0
		self.max_mean = 0

		if data is not None:
			observations = {}
			for ctl in data:
				for tok in ctl.tokens:
					if not hasattr(observations, tok):
						observations[tok] = []
					# we want the percentage of total words in the tokenlist this token represents
					observations[tok].append(ctl.tokens[tok] / ctl.words)

			for key in observations:
				self.tokens[key] = BaselineToken(observations[key])

	def save(self, is_default):
		print ("error")

