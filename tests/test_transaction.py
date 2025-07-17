import os
import time
import twikey
import unittest
from twikey.model.transaction_request import *


class TestTransaction(unittest.TestCase):
    _twikey = None

    ct = 1

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        base_url = "https://test.beta.twikey.com/api/creditor"
        if "CT" in os.environ:
            self.ct = os.environ["CT"]
        if "TWIKEY_API_URL" in os.environ:
            base_url = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, base_url)

    def test_new_invite(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id="CORERECURRENTNL16318",
                message="Test Message",
                ref="Merchant Reference",
                amount=10.00,
                place="Here",
            )
        )
        self.assertIsNotNone(tx)
        self._twikey.transaction.batch_send(self.ct)

    def test_tx_status(self):
        tx = self._twikey.transaction.status_details(
            StatusRequest(
                mndt_id="CORERECURRENTNL16318",
                state="ERROR",
                include=["collection", "lastupdate", "links"]
            )
        )
        self.assertIsNotNone(tx)

    def test_action(self):
        self._twikey.transaction.action(
            ActionRequest(
                id="6302230",
                action="archive",
            )
        )

    def test_update(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id="CORERECURRENTNL16318",
                message="Test Message",
                ref="Merchant Reference",
                amount=10.00,
                place="Here",
            )
        )

        self._twikey.transaction.update(
            UpdateRequest(
                id=tx.id,
                message="Test Message",
                ref="Merchant Reference",
                amount=10.00,
                place="Here",
            )
        )

    def test_refund(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id="CORERECURRENTNL16318",
                message="Test Message",
                ref="Merchant Reference",
                amount=50.00,
                place="Here",
            )
        )
        self._twikey.transaction.batch_send(self.ct)
        time.sleep(1)
        self._twikey.transaction.batch_send(self.ct)
        time.sleep(1)

        refund = self._twikey.transaction.refund(
            RefundRequest(
                id=tx.id,
                message="Test message",
                amount=50.00,
            )
        )
        self.assertIsNotNone(refund)

    @unittest.skipIf("PAIN008_FILEPATH" not in os.environ, "No PAIN008_FILEPATH set")
    def test_batch_import(self):
        self._twikey.transaction.batch_import(self.ct, "PAIN008_FILEPATH")
        try:
            self._twikey.transaction.reporting_import("")
        except twikey.TwikeyError as e:
            self.assertEqual("invalid_file", e.get_code())

    def test_query(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id="CORERECURRENTNL16318",
                message="Test Message",
                ref="Merchant Reference",
                amount=50.00,
                place="Here",
            )
        )
        self._twikey.transaction.batch_send(self.ct)
        time.sleep(1)
        self._twikey.transaction.batch_send(self.ct)
        time.sleep(1)

        mandates = self._twikey.transaction.query(
            QueryTransactionsRequest(
                from_id=(tx.id-2),
            )
        )
        self.assertIsNotNone(mandates)

    def test_remove(self):
        tx = self._twikey.transaction.create(
            NewTransactionRequest(
                mndt_id="CORERECURRENTNL16318",
                message="Test Message",
                ref="Merchant Reference",
                amount=50.00,
                place="Here",
            )
        )

        self._twikey.transaction.remove(
            RemoveTransactionRequest(
                id=tx.id
            )
        )

    def test_feed(self):
        self._twikey.transaction.feed(MyFeed())


class MyFeed(twikey.TransactionFeed):
    def transaction(self, transaction):
        print(transaction)
        print("-" * 50)
        _final = ""
        if transaction.is_paid():
            _state = "is now paid"
        elif transaction.is_error():
            _state = "failed due to '" + transaction.bkmsg + "'"
            if transaction.final:
                # final means Twikey has gone through all dunning steps, but customer still did not pay
                _final = "with no more dunning steps"
        print(
            "Transaction update",
            transaction.amount,
            "euro with",
            transaction.ref,
            transaction.state,
            _final,
        )


if __name__ == "__main__":
    unittest.main()
