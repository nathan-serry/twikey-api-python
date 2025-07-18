import os
import twikey
import unittest
import uuid
from twikey.model.refund_request import *

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

    @unittest.skip
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
        print(benef)

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
        # print(refund)

    @unittest.skip
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
        print(refund)

        details = self._twikey.refund.details(
            CreditTransferDetailRequest(
                id=refund.id
            )
        )
        print(details)

    @unittest.skip
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
        print(refund)

        self._twikey.refund.remove(
            RemoveCreditTransferRequest(
                id=refund.id
            )
        )

    @unittest.skip
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
        print(credit_transfers)

    @unittest.skip
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
        print(details)

    @unittest.skip
    def test_get_beneficiaries(self):
        beneficiaries = self._twikey.refund.get_beneficiary_accounts(
            GetBeneficiariesRequest(
                with_address=False
            )
        )
        print(beneficiaries)

    def test_disable_beneficiary(self):
        pass

    @unittest.skip
    def test_feed(self):
        self._twikey.refund.feed(MyFeed())


class MyFeed(twikey.RefundFeed):
    def refund(self, refund):
        # print(
        #     "Refund update #{0} {1} Euro with new state={2}".format(
        #         refund["id"], refund["amount"], refund["state"]
        #     )
        # )
        print(refund)
        print("-" * 50)


if __name__ == "__main__":
    unittest.main()
