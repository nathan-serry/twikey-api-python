import requests
from twikey.model.paylink_request import *
from twikey.model.paylink_response import *


class Paylink(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def create(self, request: PaymentLinkRequest) -> CreatedPaylinkResponse:
        """
        See https://www.twikey.com/api/#create-paymentlink
        Posts a new payment link via the api to the server
        :param request: the create parameters as a dictionary. (see PaymentLinkRequest)
        :return: a typed version of the response
        """
        url = self.client.instance_url("/payment/link")
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
                raise self.client.raise_error("Create paylink", response)
            return CreatedPaylinkResponse(response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Create paylink", e)

    def status_details(self, request: StatusRequest) -> PaylinkEntry:
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
        url = self.client.instance_url("/payment/link")
        try:
            self.client.refresh_token_if_required()
            headers = self.client.headers("application/json")
            response = requests.get(url=url, params=params, headers=headers, timeout=15)
            if response.status_code != 200:
                raise self.client.raise_error("Transaction detail", response)
            _links = response.json()["Links"]
            if len(_links) > 0:
                return PaylinkEntry(_links[0])
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Transaction detail", e)

    def refund(self, request: RefundRequest) -> PaylinkEntry:
        """
        See https://www.twikey.com/api/#refund-paymentlink
        Creates a refund for a given transaction. If the beneficiary account does not exist yet,
        it will be registered to the customer using the mandate IBAN or the one provided.
        Parameters:
            api_key (str): Twikey API key used for authentication
            data (dict): Must include 'id', 'message', and 'amount'. May include
                         'ref', 'place', 'iban', or 'bic'
        Returns:
            dict: Response payload containing refund entry details
        """
        data = request.to_request()
        url = self.client.instance_url("/payment/link/refund")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(url=url, data=data, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update transaction", response)
            return PaylinkEntry(response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update transaction", e)

    def remove(self, request: RemoveRequest):
        """
        See https://www.twikey.com/api/#remove-paymentlink
        Removes a payment link that has not yet been sent to the bank.
        Parameters:
            data (dict): Dictionary with 'id' to identify the payment link
        Returns:
            None: A successful deletion returns HTTP 204 with no content
        """
        data = request.to_request()
        url = self.client.instance_url(f"/payment/link?id={data.get('id')}")
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(url=url, headers=self.client.headers(), timeout=15)
            response.raise_for_status()
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update transaction", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update transaction", e)

    def feed(self, paylink_feed):
        """
        See https://www.twikey.com/api/#paymentlink-feed
        does the api call to the server
        :param paylink_feed: your feed class with a function that handels the seperate paylinks
        :return: returns a typed version of the payment link to the function in your custom feed class
        """
        url = self.client.instance_url("/payment/link/feed")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Feed paylink", response)
            feed_response = response.json()
            while len(feed_response["Links"]) > 0:
                for msg in feed_response["Links"]:
                    feed_break = paylink_feed.paylink(PaylinkEntry(msg))
                    if feed_break == False:
                        raise self.client.raise_error("MyFeed threw error")
                response = requests.get(
                    url=url,
                    headers=self.client.headers(),
                    timeout=15,
                )
                if "ApiErrorCode" in response.headers:
                    raise self.client.raise_error("Feed paylink", response)
                feed_response = response.json()
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Feed paylink", e)


class PaylinkFeed:
    def paylink(self, paylink) -> bool:
        """
        Custom logic for handeling the paylinks gained from the api call

        :param paylink: information about a singular paylink
        :return: in case of your business logic decides stop processing updates return False
        """
        pass
