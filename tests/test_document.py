import os
import twikey
import unittest

from twikey.model import (
    InviteRequest, FetchMandateRequest, Document, SignRequest, MandateActionRequest, UpdateMandateRequest,
    PdfRetrieveRequest, PdfUploadRequest, CustomerAccessRequest, QueryMandateRequest, SignMethod
)


class TestDocument(unittest.TestCase):

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        if "TWIKEY_API_KEY" not in os.environ:
            self.skipTest("No TWIKEY_API_KEY set")

        key = os.environ["TWIKEY_API_KEY"]
        base_url = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, base_url)

    # @unittest.skip("reason for skipping")
    def test_new_invite(self):
        ct = 1
        if "CT" in os.environ:
            ct = os.environ["CT"]

        invite = self._twikey.document.create(
            InviteRequest(
                ct=ct,
                email="no-reply@twikey.com",
                firstname="Info",
                lastname="Twikey",
                l="en",
                address="Abby road",
                city="Liverpool",
                zip="1526",
                country="BE",
                mobile="",
                iban="BE51561419613262",
                bic="GKCCBEBB",
            )
        )
        # print("invite:", invite)
        self.assertIsNotNone(invite)

    # @unittest.skip("testing unsigned doc = reason for skipping")
    def test_sign(self):
        signed_mandate = self._twikey.document.sign(
            SignRequest(
                ct="772",
                l="en",
                iban="BE51561419613262",
                bic="GKCCBEBB",
                customer_number="CUST001",
                email="joe.doe@gmail.com",
                last_name="Doe",
                first_name="John",
                mobile="+32499000001",
                address="Main Street 1",
                city="Brussels",
                zip="1000",
                country="BE",
                company_name="Acme Corp",
                vat_no="BE0123456789",
                campaign="Summer2025",
                prefix="Mr.",
                check=True,
                ed="2025-07-31",
                reminder_days=3,
                send_invite=False,
                token="abc123token",
                require_validation=False,
                transaction_amount=49.95,
                transaction_message="Welcome fee",
                transaction_ref="TXN001",
                plan="monthly",
                subscription_start="2025-08-01",
                subscription_recurrence="1m",
                subscription_stop_after=12,
                subscription_amount=9.99,
                subscription_message="Monthly membership",
                subscription_ref="SUB001",
                method=SignMethod.ITSME,
                # sign_date="2025-07-03T14:21:45",
                place="Brussels",
            )
        )
        print("signed Response:", signed_mandate)
        self.assertIsNotNone(signed_mandate)
        self.assertIsNotNone(signed_mandate.MndtId)

    @unittest.skip("reason for skipping")
    def test_fetch(self):
        fetched_mandate = self._twikey.document.fetch(
            FetchMandateRequest(
                mndt_id="CORERECURRENTNL17071",
                force=True,
            )
        )
        # print(f"fetching Response: \n{fetched_mandate}")
        self.assertIsNotNone(fetched_mandate)

    @unittest.skip("reason for skipping")
    def test_query(self):
        query = self._twikey.document.query(
            QueryMandateRequest(
                iban="BE51561419613262",
                customer_number="customer123",
                email="no-reply@twikey.com",
            )
        )
        # for contract in query:
        #     print("-" * 40)
        #     print(contract)
        self.assertIsNotNone(query)

    @unittest.skip("cancelling random document over and over")
    def test_cancel(self):
        cancelled_mandate = self._twikey.document.cancel(
            "MN543210",
            "hello",
        )

    @unittest.skip("reason for skipping")
    def test_action(self):
        mandate_action = self._twikey.document.action(
            MandateActionRequest(
                mndt_id="CORERECURRENTNL17071",
                type="reminder",
                reminder="1"
            )
        )

    @unittest.skip("reason for skipping")
    def test_update(self):
        update = self._twikey.document.update(
            UpdateMandateRequest(
                mndt_id="MN543210",
                ct="772",
                state="active",
                mobile="+32499000001",
                iban="BE51561419613262",
                bic="GKCCBEBB",
                customer_number="CUST001",
                email="joe.doe@gmail.com",
                first_name="John",
                last_name="Doe",
                company_name="Acme Corp",
                coc="BE0123456789",
                l="en",
                address="Main Street 1",
                city="Brussels",
                zip="1000",
                country="BE",
            )
        )

    @unittest.skip("already signed over and over = reason for skipping")
    def test_upload_pdf(self):
        uploaded_pdf = self._twikey.document.upload_pdf(
            PdfUploadRequest(
                mndt_id="CORERECURRENTNL17229",
                pdf_path="/Users/nathanserry/Downloads/dummy.pdf",
                bank_signature=False,
            )
        )

    @unittest.skip("reason for skipping")
    def test_retrieve_pdf(self):
        retrieved_pdf = self._twikey.document.retrieve_pdf(
            PdfRetrieveRequest(
                mndt_id="CORERECURRENTNL17192"
            )
        )
        # print("pdf retrieval:", retrieved_pdf)
        retrieved_pdf.save("/tmp/pdf.pdf")
        self.assertIsNotNone(retrieved_pdf)

    @unittest.skip("reason for skipping")
    def test_customer_access(self):
        access_url = self._twikey.document.customer_access(
            CustomerAccessRequest(
                mndt_id="MN543210"
            )
        )
        # print("url:", access_url)
        self.assertIsNotNone(access_url)

    @unittest.skip("reason for skipping")
    def test_feed(self):
        print(self._twikey.document.feed(MyDocumentFeed()))


class MyDocumentFeed(twikey.DocumentFeed):
    def new_document(self, doc, evt_time):
        fetched_doc = Document(mandate=doc, headers={"X-STATE": doc.get("State", "UNKNOWN")})
        print("Document created @", evt_time)
        print(fetched_doc)
        print("-" * 50)

    def updated_document(self, original_number, doc, reason, evt_time):
        fetched_doc = Document(mandate=doc, headers={"X-STATE": doc.get("State", "UNKNOWN")})
        print(f"Document updated ({original_number}) b/c {reason['Rsn']} @ {evt_time}")
        print(fetched_doc)
        print("-" * 50)

    def cancelled_document(self, number, reason, evt_time):
        print(f"Document cancelled {number} b/c {reason['Rsn']} @ {evt_time}")
        print("-" * 50)


if __name__ == "__main__":
    unittest.main()
