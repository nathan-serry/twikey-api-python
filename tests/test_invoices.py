import os
import twikey
import unittest
import time
import uuid
from datetime import date, timedelta
from twikey.model.invoice_request import *
from twikey.model.invoice_response import InvoiceResponse


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
                date=(date.today() + timedelta(days=7)).isoformat(),
                duedate=(date.today() + timedelta(days=14)).isoformat(),
                customer=Customer(
                    customerNumber="customer2",
                    email="no-reply@twikey.com",
                    firstname="Twikey",
                    lastname="Support",
                    address="Derbystraat 43",
                    city="Gent",
                    zip="9051",
                    country="BE",
                    l="en",
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

    def test_update(self):
        invoice = self._twikey.invoice.update(
            UpdateInvoiceRequest(
                id="58073359-7fd0-4683-a60f-8c08096a189e",
                title="Invoice " + date.today().strftime("%B"),
                date=(date.today() + timedelta(days=7)).isoformat(),
                duedate=(date.today() + timedelta(days=14)).isoformat(),
                state="BOOKED"
            )
        )
        self.assertIsNotNone(invoice)

    def test_delete(self):
        invoice = self._twikey.invoice.create(
            InvoiceRequest(
                id=str(uuid.uuid4()),
                number="Inv-" + str(round(time.time())),
                title="Invoice " + date.today().strftime("%B"),
                remittance="596843697521",
                ct=1988,
                amount=100,
                date=(date.today() + timedelta(days=7)).isoformat(),
                duedate=(date.today() + timedelta(days=14)).isoformat(),
                customer=Customer(
                    customerNumber="customer2",
                    email="no-reply@twikey.com",
                    firstname="Twikey",
                    lastname="Support",
                    address="Derbystraat 43",
                    city="Gent",
                    zip="9051",
                    country="BE",
                    l="en",
                    mobile="32498665995",
                ),
                # "pdf": "JVBERi0xLj....RU9GCg=="
            )
        )
        self.assertIsNotNone(invoice)

        self._twikey.invoice.delete(
            DeleteRequest(
                id=invoice.id,
            )
        )

    def test_details(self):
        invoice = self._twikey.invoice.details(
            DetailsRequest(
                id="89946636-373f-4011-b13f-ac59f26a58cb",
                include_lastpayment=True,
                include_meta=True,
                include_customer=True,
            )
        )
        self.assertIsNotNone(invoice)

    def test_action(self):
        self._twikey.invoice.action(
            request=ActionRequest(
                id="1394e983-c6cd-4c58-98d9-6bf69c997547",
                type=ActionType.EMAIL,
            )
        )

    def test_UBL_upload(self):
        new_invoice = self._twikey.invoice.upload_ubl(
            UblUploadRequest(
                xml_path="/Users/nathanserry/Downloads/Inv-1752246605_ubl.xml",
            )
        )
        self.assertIsNotNone(new_invoice)

    def test_bulk_create_invoices(self):
        batch_invoices = self._twikey.invoice.bulk_create(
            BulkInvoiceRequest(
                invoices=[
                    InvoiceRequest(
                        id=str(uuid.uuid4()),
                        number="Inv-" + str(round(time.time()) + i),
                        title="Invoice " + date.today().strftime("%B"),
                        ct=1988,
                        amount=42.50,
                        date=(date.today() + timedelta(days=7)).isoformat(),
                        duedate=(date.today() + timedelta(days=14)).isoformat(),
                        customer=Customer(
                            customerNumber="customer2",
                            email="no-reply@twikey.com",
                            firstname="Twikey",
                            lastname="Support",
                            address="Derbystraat 43",
                            city="Gent",
                            zip="9051",
                            country="BE",
                            l="en",
                            mobile="32498665995",
                        ),
                    )
                    for i in range(5)
                ]
            )
        )
        self.assertIsNotNone(batch_invoices)

    def test_batch_details(self):
        batch_invoices = self._twikey.invoice.bulk_create(
            BulkInvoiceRequest(
                invoices=[
                    InvoiceRequest(
                        id=str(uuid.uuid4()),
                        number="Inv-" + str(round(time.time()) + i),
                        title="Invoice " + date.today().strftime("%B"),
                        ct=1988,
                        amount=42.50,
                        date=(date.today() + timedelta(days=7)).isoformat(),
                        duedate=(date.today() + timedelta(days=14)).isoformat(),
                        customer=Customer(
                            customerNumber="customer2",
                            email="no-reply@twikey.com",
                            firstname="Twikey",
                            lastname="Support",
                            address="Derbystraat 43",
                            city="Gent",
                            zip="9051",
                            country="BE",
                            l="en",
                            mobile="32498665995",
                        ),
                    )
                    for i in range(2)
                ]
            )
        )
        self.assertIsNotNone(batch_invoices)

        batch_info = self._twikey.invoice.bulk_details(
            BulkBatchDetailsRequest(
                batch_id=batch_invoices.batch_id,
            )
        )
        self.assertIsNotNone(batch_info)

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
        print(InvoiceResponse(**invoice))
        print("-" * 50)


if __name__ == "__main__":
    unittest.main()
