import requests
from twikey.model.refund_request import *
from twikey.model.refund_response import *


class Refund(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def create_beneficiary_account(self, request: AddBeneficiaryRequest):
        """
        Creation a beneficiary account (with accompanied customer)
        :param request: data all_customer fields + iban and bic
        :return  {
            "name": "Beneficiary Name",
            "iban": "BE68068897250734",
            "bic": "JVBABE22",
            "available": true,
            "address": {
                "street": "Veldstraat 11",
                "city": "Gent",
                "zip": "9000",
                "country": "BE"
            }
        }
        """
        url = self.client.instance_url("/transfers/beneficiaries")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create beneficiary", response)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create beneficiary", e)

    def create(self, request: CreateCreditTransferRequest):
        """
        Creation of a refund provided the customer was created and has a customerNumber
        :param request: customerNumber The customer number (required) and transactionDetails required

        transactionDetails should contain
            * iban:	Iban of the beneficiary
            * message:	Message to the creditor	Yes	string
            * amount:	Amount to be sent
            * ref:	Reference of the transaction
            * date:	Required execution date of the transaction (ReqdExctnDt)
            * place:	Optional place

        :return {
                    "id": "11DD32CA20180412220109485",
                    "iban": "BE68068097250734",
                    "bic": "JVBABE22",
                    "amount": 12,
                    "msg": "test",
                    "place": null,
                    "ref": "123",
                    "date": "2018-04-12"
                }
        """
        url = self.client.instance_url("/transfer")
        data = request.to_request()
        data["_state"] = "PAID"
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create refund", response)
            _links = response.json()["Entries"]
            if _links and len(_links) > 0:
                return RefundStatusEntry(_links[0])
            return None
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create refund", e)

    def details(self, request: CreditTransferDetailRequest):
        """
        See https://www.twikey.com/api/#status-paymentlink
        Retrieve transaction status by ID, ref, or mandate ID.
        Args:
            request (TransactionStatusRequest): The query parameters. (See StatusPaymentLinkRequest)
        Returns:
            TransactionStatusResponse: List of transaction status entries.
        Raises:
            TwikeyError: On error responses.
        """
        params = request.to_request()
        url = self.client.instance_url("/transfer/detail")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.get(url=url, params=params, headers=headers, timeout=15)
            if response.status_code != 200:
                raise self.client.raise_error("Transfer detail", response)
            _links = response.json()["Entries"]
            if _links and len(_links) > 0:
                return RefundStatusEntry(_links[0])
            return None
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Transaction detail", e)

    def remove(self, request: RemoveCreditTransferRequest):
        """
        See https://www.twikey.com/api/#remove-a-credit-transfer
        Removes a credit transfer that has not yet been sent to the bank.
        At least one of 'id' or 'ref' must be provided.
        Parameters:
            request (TransactionStatusRequest): the id of the credit_transfer
        Returns:
            None: A successful deletion returns HTTP 204 with no content
        """
        data = request.to_request()
        url = self.client.instance_url(f"/transfer?id={data.get('id')}")
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(url=url, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Remove Credit Transfer", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Remove Credit Transfer", e)

    def create_batch(self, request: CreateTransferBatchRequest):
        """
        Creation of a batch of refunds
        :param request: Contract Template. (Required) Iban if different from the profile iban (Optional)
        :return {
                    "CreditTransfers": [
                        {
                            "id": 2837,
                            "pmtinfid": "Twikey-20220330113125070605075",
                            "entries": 2
                        }
                    ]
                }
        """
        url = self.client.instance_url("/transfer/complete")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create batch refunds", response)
            _links = response.json()["CreditTransfers"]
            if _links and len(_links) > 0:
                return CreditTransferEntry(_links[0])
            return None
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create batch refunds", e)

    def batch_detail(self, request: CreateTransferBatchRequest):
        """
        Creation of a batch of refunds
        :param request: Contract Template. (Required) Iban if different from the profile iban (Optional)
        :return {
                    "CreditTransfers": [
                        {
                            "id": 2837,
                            "pmtinfid": "Twikey-20220330113125070605075",
                            "entries": 2
                        }
                    ]
                }
        """
        url = self.client.instance_url("/transfer/complete")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                params=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Create refund", response)
            _links = response.json()["CreditTransfers"]
            if _links and len(_links) > 0:
                return CreditTransferEntry(_links[0])
            return None
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create refund", e)

    def get_beneficiary_accounts(self, request: GetBeneficiariesRequest):
        """
        get beneficiary accounts (with accompanied customer)
        :param request: withAddress: if the address needs to be included
        :return  {
            "beneficiaries": [
                {
                    "name": "sdfsf",
                    "iban": "BE92221216720939",
                    "bic": "GEBABEBB",
                    "available": true,
                    "address": null
                },
                {
                    "name": "beneficiary2",
                    "iban": "BE16645348971174",
                    "bic": "JVBABE22",
                    "available": true,
                    "address": {
                        "street": "Veldstraat 11",
                        "city": "Gent",
                        "zip": "9000",
                        "country": "BE"
                    }
                }
            ]
        }
        """
        url = self.client.instance_url("/transfers/beneficiaries")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                data=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("get beneficiaries", response)
            return GetbeneficiarieResponse(response.json()['beneficiaries'])
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("get beneficiaries", e)

    def disable_beneficiary_accounts(self, request: GetBeneficiariesRequest):
        """
        disable beneficiary account (with accompanied customer)
        :param request: withAddress: if the address needs to be included
        :return  None
        """
        data = request.to_request()
        url = self.client.instance_url(f"/transfers/beneficiaries/{data['iban']}?customerNumber={data['customerNumber']}")
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(
                url=url,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("get beneficiaries", response)
            return GetbeneficiarieResponse(response.json()['beneficiaries'])
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("get beneficiaries", e)

    def feed(self, refund_feed):
        url = self.client.instance_url("/transfer")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers()
            response = requests.get(
                url=url,
                headers=headers,
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Feed refunds", response)
            feed_response = response.json()
            while len(feed_response["Entries"]) > 0:
                for msg in feed_response["Entries"]:
                    refund_feed.refund(RefundStatusEntry(msg))
                response = requests.get(
                    url=url,
                    headers=self.client.headers(),
                    timeout=15,
                )
                if "ApiErrorCode" in response.headers:
                    raise self.client.raise_error("Feed refunds", response)
                feed_response = response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Feed refunds", e)


class RefundFeed:
    def refund(self, refund):
        """
        :refund: – Class object containing
            * id: Twikey id
            * iban: IBAN of the beneficiary
            * bic: BIC of the beneficiary
            * amount: Amount of the refund
            * msg: Message for the beneficiary
            * place: Optional place
            * ref: Your reference
            * date: Date when the transfer was requested
            * state: Paid
            * bkdate: Date when the transfer was done
        """
        pass
