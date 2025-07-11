import os
import twikey
import unittest
import time
import uuid
from datetime import date, timedelta
from twikey.model import InvoiceRequest, Customer, LineItem


class TestInvoices(unittest.TestCase):
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
        invoice = self._twikey.invoice.create(
            InvoiceRequest(
                id=str(uuid.uuid4()),
                number="Inv-" + str(round(time.time())),
                title="Invoice " + date.today().strftime("%B"),
                remittance="596843697521",
                ct=1988,
                amount=100,
                date=date.today().isoformat(),
                duedate=(date.today() + timedelta(days=7)).isoformat(),
                customer=Customer(
                    customerNumber="customer123",
                    email="no-reply@twikey.com",
                    firstname="Twikey",
                    lastname="Support",
                    address="Derbystraat 43",
                    city="Gent",
                    zip="9000",
                    country="BE",
                    l="nl",
                    mobile="32498665995",
                ),
                # "pdf": "JVBERi0xLj....RU9GCg=="
                lines=[
                    LineItem(
                        code="A100",
                        description="Gymnastiekpakje maat M",
                        quantity=1,
                        uom="st",
                        unitprice=41.32,
                        vatcode="21",
                        vatsum=8.68,
                        vatrate=21.0,
                    ),
                    LineItem(
                        code="A101",
                        description="Springtouw",
                        quantity=2,
                        uom="st",
                        unitprice=20.66,
                        vatcode="21",
                        vatsum=8.68,
                        vatrate=21.0,
                    )
                ]
            )
        )
        self.assertIsNotNone(invoice)
        # print("New invoice to be paid @ " + invoice.url)
        # print(invoice)

    @unittest.skip("reason for skipping")
    def test_feed(self):
        self._twikey.invoice.feed(MyFeed(), False, "meta", "include", "lastpayment")


class MyFeed(twikey.InvoiceFeed):
    def invoice(self, invoice):
        new_state = ""
        if invoice["state"] == "PAID":
            lastpayment_ = invoice["lastpayment"]
            if lastpayment_:
                new_state = "PAID via " + lastpayment_["method"]
        else:
            new_state = "now has state " + invoice["state"]
        print(
            "Invoice update with number {0} {1} euro {2}".format(
                invoice["number"], invoice["amount"], new_state
            )
        )


if __name__ == "__main__":
    unittest.main()
