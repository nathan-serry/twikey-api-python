import os
import twikey
import unittest
from twikey.model.paylink_request import *

class TestPaylinks(unittest.TestCase):
    _twikey = None

    ct = 1

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        base_url = "https://test.beta.twikey.com/api/creditor"
        if "TWIKEY_API_URL" in os.environ:
            base_url = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, base_url)

    def test_new_invite(self):
        tx = self._twikey.paylink.create(
            PaymentLinkRequest(
                email="no-reply@twikey.com",
                title="Test Message",
                ref="Merchant Reference",
                amount=10.00
            )
        )
        self.assertIsNotNone(tx.id)
        self.assertIsNotNone(tx.amount)
        self.assertIsNotNone(tx.msg)
        self.assertIsNotNone(tx.url)

    def test_status(self):
        tx = self._twikey.paylink.status_details(
            StatusRequest(
                id="644722"
            )
        )
        self.assertIsNotNone(tx)
        self.assertIsNotNone(tx.id)
        self.assertIsNotNone(tx.amount)
        self.assertIsNotNone(tx.msg)
        self.assertIsNotNone(tx.state)

    @unittest.skipIf("PAID_PAYLINK_ID" not in os.environ, "No PAID_PAYLINK_ID set")
    def test_refund(self):
        refund = self._twikey.paylink.refund(
            RefundRequest(
                id="PAID_PAYLINK_ID",
                message="hello",
                iban="BE51561419613262",
                bic="GKCCBEBB",
            )
        )
        self.assertIsNotNone(refund.id)
        self.assertIsNotNone(refund.amount)
        self.assertIsNotNone(refund.msg)
        print(refund)

    def test_remove(self):
        tx = self._twikey.paylink.create(
            PaymentLinkRequest(
                email="no-reply@twikey.com",
                title="Test Message",
                ref="Merchant Reference",
                amount=10.00,
                iban="BE51561419613262"
            )
        )
        self.assertIsNotNone(tx.id)

        self._twikey.paylink.remove(
            RemoveRequest(
                id=tx.id
            )
        )

    def test_feed(self):
        self._twikey.paylink.feed(MyFeed())


class MyFeed(twikey.PaylinkFeed):
    def paylink(self, paylink):
        print(paylink)
        print("-" * 50)


if __name__ == "__main__":
    unittest.main()
