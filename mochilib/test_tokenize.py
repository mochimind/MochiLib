import unittest


class TokenizeTestCase(unittest.TestCase):
    def testTokenizeNoData(self):
        tmp = tokenize.tokenize(tokenize.TokenType.WordData, "")
        self.assertEqual(tmp.words, 0)

    def testTokenizeNormalData(self):
        tmp = tokenize.tokenize(tokenize.TokenType.WordData, "the quick brown fox was quick")
        expected = ['the', 'quick', 'brown', 'fox', 'was', 'quick']
        for i in range(0, len(expected)):
            self.assertEqual(expected[i], tmp.tokens[i])
        self.assertEqual(tmp.words, 6)

    def testTokenizePunctuationData(self):
        tmp = tokenize.tokenize(tokenize.TokenType.WordData, "@the. $quick, ^&*=+- 'brown'! ?fox% (was) {quick}")
        expected = ['the', 'quick', 'brown', 'fox', 'was', 'quick']
        for i in range(0, len(expected)):
            self.assertEqual(expected[i], tmp.tokens[i])
        self.assertEqual(tmp.words, 6)

class CTLTestCases(unittest.TestCase):
    def testCompressNormal(self):
        data = tokenize.tokenize(tokenize.TokenType.WordData, "the quick brown fox was quick")
        tmp = ctl.CompressedTokenList()
        tmp.compress(data)
        desired_results = {'the': 1, 'quick': 2, 'brown': 1, 'fox': 1, 'was': 1}
        for token in desired_results:
            self.assertEqual(desired_results[token], tmp.tokens[token])
        self.assertEqual(data.words, 6)

if __name__ == '__main__':
    unittest.main()