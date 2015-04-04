__author__ = "Martin Blais <blais@furius.ca>"

import unittest

from beancount import loader
from beancount.plugins import sellgains
from beancount.ops import validation
from beancount.parser import printer


class TestSellGains(unittest.TestCase):

    @loader.loaddoc
    def test_sellgains_success(self, entries, errors, options_map):
        """
        option "plugin" "beancount.ops.auto_accounts"
        option "plugin" "beancount.plugins.sellgains"

        1999-07-31 * "Sell"
          Assets:US:Company:ESPP          -81 ADSK {26.3125 USD} @ 26.4375 USD
          Assets:US:Company:Cash      2141.36 USD
          Expenses:Financial:Fees        0.08 USD
          Income:US:Company:ESPP:PnL
        """
        printer.print_errors(errors)
        self.assertEqual([], errors)

    @loader.loaddoc
    def test_sellgains_fail_balance(self, entries, errors, options_map):
        """
        option "plugin" "beancount.ops.auto_accounts"
        option "plugin" "beancount.plugins.sellgains"

        1999-07-31 * "Sell"
          Assets:US:Company:ESPP          -81 ADSK {26.3125 USD} @ 26.4375 USD
          Assets:US:Company:Cash      2141.36 USD
          Expenses:Financial:Fees        1.08 USD
          Income:US:Company:ESPP:PnL   -11.13 USD
        """
        self.assertEqual([sellgains.SellGainsError], list(map(type, errors)))

    @loader.loaddoc
    def test_sellgains_fail_imbalance(self, entries, errors, options_map):
        """
        option "plugin" "beancount.ops.auto_accounts"
        option "plugin" "beancount.plugins.sellgains"

        1999-07-31 * "Sell"
          Assets:US:Company:ESPP          -81 ADSK {26.3125 USD} @ 26.4375 USD
          Assets:US:Company:Cash      2141.36 USD
          Income:US:Company:ESPP:PnL   -11.13 USD
        """
        self.assertEqual([sellgains.SellGainsError,
                          validation.ValidationError], list(map(type, errors)))
