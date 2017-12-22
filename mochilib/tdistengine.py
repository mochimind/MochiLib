from scipy.stats import t

from . import token
from . import baseline

# this function performs a single sample T-test for each token in the token list
def GetAnomalies(ctl, _baseline=None):
	anomalies = mochitoken.AnomalyTokenList()
	bl = baseline.GetCurrentBaseline() if _baseline == None else _baseline

	for tok in ctl.tokens:
		# we haven't seen this token, so it must be super rare, set it as 1
		if not hasattr(baseline.tokens, tok):
			anomalies.add(mochitoken.AnomalyToken(1, 0))
		else:
			btok = bl.tokens[tok]
			test_stat = (ctl.tokens[tok] - btok.mean) / btok.stdev
			anomalies.add(mochitoken.AnomalyToken(t.cdf(test_stat, btok.n - 1),
												  btok.n / bl.datapoints))


