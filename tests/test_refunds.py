import os
import twikey
import unittest
import uuid
from twikey.model.refund_request import AddBeneficiaryRequest, CreateCreditTransferRequest, \
    CreateTransferBatchRequest, TransferBatchDetailsRequest, DisableBeneficiaryRequest
from twikey.model.refund_response import Refund


class TestRefunds(unittest.TestCase):
    _twikey = None

    ct = 1

    @unittest.skipIf("TWIKEY_API_KEY" not in os.environ, "No TWIKEY_API_KEY set")
    def setUp(self):
        key = os.environ["TWIKEY_API_KEY"]
        base_url = "https://test.beta.twikey.com/api/creditor"
        if "TWIKEY_API_URL" in os.environ:
            base_url = os.environ["TWIKEY_API_URL"]
        self._twikey = twikey.TwikeyClient(key, base_url)

    def test_new_beneficiary(self):
        customer_number = str(uuid.uuid4())
        benef = self._twikey.refund.create_beneficiary_account(
            AddBeneficiaryRequest(
                    customer_number=customer_number,
                    email="info@twikey.com",
                    name="Info Twikey",
                    l="en",
                    address="Abby road",
                    city="Liverpool",
                    zip="1526",
                    country="BE",
                    mobile="",
                    iban="NL46ABNA8910219718",
                    bic="ABNANL2A",
            )
        )
        self.assertIsNotNone(benef)

        refund = self._twikey.refund.create(
            CreateCreditTransferRequest(
                    customer_number=customer_number,
                    iban="NL46ABNA8910219718",
                    message="Refund faulty item",
                    ref="My internal reference",
                    amount=10.99,
            )
        )
        self.assertIsNotNone(refund)

    def test_detail(self):
        customer_number = str(uuid.uuid4())
        benef = self._twikey.refund.create_beneficiary_account(
            AddBeneficiaryRequest(
                customer_number=customer_number,
                email="info@twikey.com",
                name="Info Twikey",
                l="en",
                address="Abby road",
                city="Liverpool",
                zip="1526",
                country="BE",
                mobile="",
                iban="NL46ABNA8910219718",
                bic="ABNANL2A",
            )
        )
        self.assertIsNotNone(benef)

        refund = self._twikey.refund.create(
            CreateCreditTransferRequest(
                customer_number=customer_number,
                iban="NL46ABNA8910219718",
                message="Refund faulty item",
                ref="My internal reference",
                amount=10.99,
            )
        )
        self.assertIsNotNone(refund)

        details = self._twikey.refund.details(refund_id=refund.id)
        self.assertIsNotNone(details)

    def test_remove(self):
        customer_number = str(uuid.uuid4())
        benef = self._twikey.refund.create_beneficiary_account(
            AddBeneficiaryRequest(
                customer_number=customer_number,
                email="info@twikey.com",
                name="Info Twikey",
                l="en",
                address="Abby road",
                city="Liverpool",
                zip="1526",
                country="BE",
                mobile="",
                iban="NL46ABNA8910219718",
                bic="ABNANL2A",
            )
        )
        self.assertIsNotNone(benef)

        refund = self._twikey.refund.create(
            CreateCreditTransferRequest(
                customer_number=customer_number,
                iban="NL46ABNA8910219718",
                message="Refund faulty item",
                ref="My internal reference",
                amount=10.99,
            )
        )
        self.assertIsNotNone(refund)

        self._twikey.refund.remove(refund_id=refund.id)

    def test_create_batch(self):
        customer_number = str(uuid.uuid4())
        benef = self._twikey.refund.create_beneficiary_account(
            AddBeneficiaryRequest(
                customer_number=customer_number,
                email="info@twikey.com",
                name="Info Twikey",
                l="en",
                address="Abby road",
                city="Liverpool",
                zip="1526",
                country="BE",
                mobile="",
                iban="NL46ABNA8910219718",
                bic="ABNANL2A",
            )
        )
        self.assertIsNotNone(benef)

        refund = self._twikey.refund.create(
            CreateCreditTransferRequest(
                customer_number=customer_number,
                iban="NL46ABNA8910219718",
                message="Refund faulty item",
                ref="My internal reference",
                amount=10.99,
            )
        )
        self.assertIsNotNone(refund)

        credit_transfers = self._twikey.refund.create_batch(
            CreateTransferBatchRequest(
                ct="772",
                iban="NL36RABO0115531548",
            )
        )
        self.assertIsNotNone(credit_transfers)

    def test_batch_details(self):
        customer_number = str(uuid.uuid4())
        benef = self._twikey.refund.create_beneficiary_account(
            AddBeneficiaryRequest(
                customer_number=customer_number,
                email="info@twikey.com",
                name="Info Twikey",
                l="en",
                address="Abby road",
                city="Liverpool",
                zip="1526",
                country="BE",
                mobile="",
                iban="NL46ABNA8910219718",
                bic="ABNANL2A",
            )
        )
        self.assertIsNotNone(benef)

        refund = self._twikey.refund.create(
            CreateCreditTransferRequest(
                customer_number=customer_number,
                iban="NL46ABNA8910219718",
                message="Refund faulty item",
                ref="My internal reference",
                amount=10.99,
            )
        )
        self.assertIsNotNone(refund)

        credit_transfers = self._twikey.refund.create_batch(
            CreateTransferBatchRequest(
                ct="772",
                iban="NL36RABO0115531548",
            )
        )
        self.assertIsNotNone(credit_transfers)

        details = self._twikey.refund.batch_detail(
            TransferBatchDetailsRequest(
                id=credit_transfers.id
            )
        )
        self.assertIsNotNone(details)

    def test_get_beneficiaries(self):
        beneficiaries = self._twikey.refund.get_beneficiary_accounts(with_address=True)
        self.assertIsNotNone(beneficiaries)

    def test_disable_beneficiary(self):
        customer_number = str(uuid.uuid4())
        benef = self._twikey.refund.create_beneficiary_account(
            AddBeneficiaryRequest(
                customer_number=customer_number,
                email="info@twikey.com",
                name="Info Twikey",
                l="en",
                address="Abby road",
                city="Liverpool",
                zip="1526",
                country="BE",
                mobile="",
                iban="NL46ABNA8910219718",
                bic="ABNANL2A",
            )
        )
        self.assertIsNotNone(benef)

        self._twikey.refund.disable_beneficiary_accounts(
            DisableBeneficiaryRequest(
                iban = "NL46ABNA8910219718",
                customer_number = customer_number
            )
        )

    def test_feed(self):
        self._twikey.refund.feed(MyFeed())


class MyFeed(twikey.RefundFeed):
    def refund(self, refund:Refund):
        print(
            "Refund update #{0} {1} Euro with new state={2}".format(
                refund.id, refund.amount, refund.state
            )
        )


if __name__ == "__main__":
    unittest.main()
