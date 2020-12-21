import unittest

from cashaddress import convert
from cashaddress.convert import Address, InvalidAddress


class TestConversion(unittest.TestCase):
    def test_to_legacy_p2sh(self):
        self.assertEqual(convert.to_legacy_address('3CWFddi6m4ndiGyKqzYvsFYagqDLPVMTzC'),
                         '3CWFddi6m4ndiGyKqzYvsFYagqDLPVMTzC')
        self.assertEqual(convert.to_legacy_address('bitcoincash:ppm2qsznhks23z7629mms6s4cwef74vcwvn0h829pq'),
                         '3CWFddi6m4ndiGyKqzYvsFYagqDLPVMTzC')

    def test_to_legacy_p2pkh(self):
        self.assertEqual(convert.to_legacy_address('155fzsEBHy9Ri2bMQ8uuuR3tv1YzcDywd4'),
                         '155fzsEBHy9Ri2bMQ8uuuR3tv1YzcDywd4')
        self.assertEqual(convert.to_legacy_address('bitcoincash:qqkv9wr69ry2p9l53lxp635va4h86wv435995w8p2h'),
                         '155fzsEBHy9Ri2bMQ8uuuR3tv1YzcDywd4')

    def test_to_cash_p2sh(self):
        self.assertEqual(convert.to_cash_address('3CWFddi6m4ndiGyKqzYvsFYagqDLPVMTzC'),
                         'bitcoincash:ppm2qsznhks23z7629mms6s4cwef74vcwvn0h829pq')
        self.assertEqual(convert.to_cash_address('bitcoincash:ppm2qsznhks23z7629mms6s4cwef74vcwvn0h829pq'),
                         'bitcoincash:ppm2qsznhks23z7629mms6s4cwef74vcwvn0h829pq')

    def test_to_cash_p2pkh(self):
        self.assertEqual(convert.to_cash_address('155fzsEBHy9Ri2bMQ8uuuR3tv1YzcDywd4'),
                         'bitcoincash:qqkv9wr69ry2p9l53lxp635va4h86wv435995w8p2h')
        self.assertEqual(convert.to_cash_address('bitcoincash:qqkv9wr69ry2p9l53lxp635va4h86wv435995w8p2h'),
                         'bitcoincash:qqkv9wr69ry2p9l53lxp635va4h86wv435995w8p2h')

    def test_to_legacy_p2sh_testnet(self):
        self.assertEqual(convert.to_legacy_address('2MwikwR6hoVijCmr1u8UgzFMHFP6rpQyRvP'),
                         '2MwikwR6hoVijCmr1u8UgzFMHFP6rpQyRvP')
        self.assertEqual(convert.to_legacy_address('bchtest:pqc3tyspqwn95retv5k3c5w4fdq0cxvv95u36gfk00'),
                         '2MwikwR6hoVijCmr1u8UgzFMHFP6rpQyRvP')

    def test_to_legacy_p2pkh_testnet(self):
        self.assertEqual(convert.to_legacy_address('mqp7vM7eU7Vu9NPH1V7s7pPg5FFBMo6SWK'),
                         'mqp7vM7eU7Vu9NPH1V7s7pPg5FFBMo6SWK')
        self.assertEqual(convert.to_legacy_address('bchtest:qpc0qh2xc3tfzsljq79w37zx02kwvzm4gydm222qg8'),
                         'mqp7vM7eU7Vu9NPH1V7s7pPg5FFBMo6SWK')

    def test_to_cash_p2sh_testnet(self):
        self.assertEqual(convert.to_cash_address('2MwikwR6hoVijCmr1u8UgzFMHFP6rpQyRvP'),
                         'bchtest:pqc3tyspqwn95retv5k3c5w4fdq0cxvv95u36gfk00')
        self.assertEqual(convert.to_cash_address('bchtest:pqc3tyspqwn95retv5k3c5w4fdq0cxvv95u36gfk00'),
                         'bchtest:pqc3tyspqwn95retv5k3c5w4fdq0cxvv95u36gfk00')

    def test_to_cash_p2pkh_testnet(self):
        self.assertEqual(convert.to_cash_address('mqp7vM7eU7Vu9NPH1V7s7pPg5FFBMo6SWK'),
                         'bchtest:qpc0qh2xc3tfzsljq79w37zx02kwvzm4gydm222qg8')
        self.assertEqual(convert.to_cash_address('bchtest:qpc0qh2xc3tfzsljq79w37zx02kwvzm4gydm222qg8'),
                         'bchtest:qpc0qh2xc3tfzsljq79w37zx02kwvzm4gydm222qg8')

    def test_is_valid(self):
        self.assertTrue(convert.is_valid('bitcoincash:qqkv9wr69ry2p9l53lxp635va4h86wv435995w8p2h'))
        self.assertTrue(convert.is_valid('2MwikwR6hoVijCmr1u8UgzFMHFP6rpQyRvP'))
        self.assertFalse(convert.is_valid('bitcoincash:aqkv9wr69ry2p9l53lxp635va4h86wv435995w8p2h'))
        self.assertFalse(convert.is_valid('bitcoincash:qqqqqqqq9ry2p9l53lxp635va4h86wv435995w8p2h'))
        self.assertFalse(convert.is_valid('22222wR6hoVijCmr1u8UgzFMHFP6rpQyRvP'))
        self.assertFalse(convert.is_valid(False))
        self.assertFalse(convert.is_valid('Hello World!'))

    def test_prefixes(self):
        """Test a few identical addresses with different CashAddr prefixes"""
        legacy_address = "1NLcNpAaBBMekgBZk7NxwdxwtSUTfTV8Aq"
        addr = Address.from_string(legacy_address)
        default_prefix = addr.prefix
        self.assertEqual(default_prefix, Address.MAINNET_PREFIX)
        self.assertEqual(addr.cash_address(),
                         'bitcoincash:qr4pqy6q4cy2d50zpaek57nnrja7289fkskz6jm7yf')
        self.assertEqual(addr.cash_address(prefix='abc'),
                         'abc:qr4pqy6q4cy2d50zpaek57nnrja7289fksqt4c50w9')
        self.assertEqual(addr.cash_address(prefix='simpleledger'),
                         'simpleledger:qr4pqy6q4cy2d50zpaek57nnrja7289fks6e3fw76h')

        regtest_address = 'regtest:qr4pqy6q4cy2d50zpaek57nnrja7289fksjm6es9se'
        addr2 = Address.from_string(regtest_address)
        self.assertEqual(addr2.legacy_address(), legacy_address)
        # The prefix defaults to the one in the input string.
        self.assertEqual(addr2.prefix, 'regtest')
        self.assertEqual(addr2.cash_address(), regtest_address)

    def test_prefix_case(self):
        with self.assertRaises(InvalidAddress):
            Address.from_string(
                'rEgTeSt:qr4pqy6q4cy2d50zpaek57nnrja7289fksjm6es9se')
        with self.assertRaises(InvalidAddress):
            Address.from_string(
                'regtest:QR4PQY6Q4CY2D50ZPAEK57NNRJA7289FKSJM6ES9SE')

        addr = Address.from_string('regtest:qr4pqy6q4cy2d50zpaek57nnrja7289fksjm6es9se')
        # The address should take the same case as the specified prefix
        self.assertEqual(addr.cash_address(prefix="SLP"),
                         'SLP:QR4PQY6Q4CY2D50ZPAEK57NNRJA7289FKSWF89PY2G')
        # Do not allow mixed-case prefixes
        with self.assertRaises(InvalidAddress):
            addr.cash_address(prefix="sLp")


if __name__ == '__main__':
    unittest.main()
