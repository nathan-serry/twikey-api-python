import logging

import requests

from twikey.model import (
    InviteRequest, FetchMandateRequest, Document, SignRequest, MandateActionRequest, UpdateMandateRequest,
    PdfRetrieveRequest, PdfUploadRequest, CustomerAccessRequest, QueryMandateRequest, InviteResponse, SignResponse,
    QueryMandateResponse, PdfResponse, CustomerAccessResponse
)


class DocumentService(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.logger = logging.getLogger(__name__)

    def create(self, request: InviteRequest) -> InviteResponse:
        url = self.client.instance_url("/invite")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Invite", response)
            json_response = response.json()
            # self.logger.debug("Added new mandate : %s" % json_response["mndtId"])
            return InviteResponse(**json_response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Invite", e)

    def sign(self, request: SignRequest) -> SignResponse:  # pylint: disable=W8106
        url = self.client.instance_url("/sign")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Sign", response)
            json_response = response.json()
            self.logger.debug("Added new mandate : %s" % json_response["MndtId"])
            return SignResponse(**json_response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Sign", e)

    def fetch(self, request: FetchMandateRequest) -> Document:
        data = request.to_request()
        url = self.client.instance_url("/mandate/detail")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url, params=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("detail", response)
            json_response = response.json()
            json_response["headers"] = response.headers
            self.logger.debug("Mandate details : %s" % json_response)
            return Document(mandate=json_response.get("Mndt"), headers=json_response.get("headers"))
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("detail", e)

    def query(self, request: QueryMandateRequest) -> list:
        data = request.to_request()
        url = self.client.instance_url("/mandate/query")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url,
                params=data,
                headers=self.client.headers(),
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("query", response)

            json_response = response.json()
            contracts_data = json_response.get("Contracts", [])
            self.logger.debug("Mandate query result: %s" % json_response)
            return [QueryMandateResponse(contract) for contract in contracts_data]
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("query", e)

    def action(self, request: MandateActionRequest):
        data = request.to_request()
        url = self.client.instance_url(f"/mandate/{data.get('mndtId')}/action")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("action", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("detail", e)

    def update(self, request: UpdateMandateRequest):
        url = self.client.instance_url("/mandate/update")
        data = request.to_request()
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            self.logger.debug("Updated mandate : {} response={}".format(data, response))
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Update", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update", e)

    def cancel(self, mandate_number, reason):
        url = self.client.instance_url(
            "/mandate?mndtId=" + mandate_number + "&rsn=" + reason
        )
        try:
            self.client.refresh_token_if_required()
            response = requests.delete(
                url=url, headers=self.client.headers(), timeout=15
            )
            self.logger.debug(
                "Cancel mandate : %s status=%d" % (mandate_number, response.status_code)
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Cancel", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Cancel", e)

    def feed(self, document_feed, start_position=False):
        url = self.client.instance_url(
            "/mandate?include=id&include=mandate&include=person"
        )
        try:
            self.client.refresh_token_if_required()
            initheaders = self.client.headers()
            if start_position:
                initheaders["X-RESUME-AFTER"] = str(start_position)
            response = requests.get(
                url=url,
                headers=initheaders,
                timeout=15,
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Feed", response)
            feed_response = response.json()
            while len(feed_response["Messages"]) > 0:
                self.logger.debug(
                    "Feed handling : %d from %s till %s"
                    % (
                        len(feed_response["Messages"]),
                        start_position,
                        response.headers["X-LAST"],
                    )
                )
                document_feed.start(
                    response.headers["X-LAST"], len(feed_response["Messages"])
                )
                error = False
                for msg in feed_response["Messages"]:
                    if "AmdmntRsn" in msg:
                        mndt_id_ = msg["OrgnlMndtId"]
                        self.logger.debug("Feed update : %s" % mndt_id_)
                        mndt_ = msg["Mndt"]
                        rsn_ = msg["AmdmntRsn"]
                        at_ = msg["EvtTime"]
                        error = document_feed.updated_document(
                            mndt_id_, mndt_, rsn_, at_
                        )
                    elif "CxlRsn" in msg:
                        mndt_ = msg["OrgnlMndtId"]
                        rsn_ = msg["CxlRsn"]
                        at_ = msg["EvtTime"]
                        self.logger.debug("Feed cancel : %s" % mndt_)
                        error = document_feed.cancelled_document(mndt_, rsn_, at_)
                    else:
                        mndt_ = msg["Mndt"]
                        at_ = msg["EvtTime"]
                        self.logger.debug("Feed create : %s" % mndt_)
                        error = document_feed.new_document(mndt_, at_)
                    if error:
                        break
                if error:
                    self.logger.debug("Error while handing invoice, stopping")
                    break
                response = requests.get(
                    url=url,
                    headers=self.client.headers(),
                    timeout=15,
                )
                if "ApiErrorCode" in response.headers:
                    raise self.client.raise_error("Feed", response)
                feed_response = response.json()
            self.logger.debug("Done handing mandate feed")
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Mandate feed", e)

    def upload_pdf(self, request: PdfUploadRequest):
        data = request.to_request()
        url = self.client.instance_url(
            f"/mandate/pdf?mndtId={data.get('mndtId')}&bankSignature={data.get('bankSignature')}")
        try:
            self.client.refresh_token_if_required()
            with open(data.get('pdfPath'), "rb") as file:
                response = requests.post(
                    url=url, data=file, headers=self.client.headers('application/pdf'), timeout=15
                )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("pdf", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("detail", e)

    def retrieve_pdf(self, request: PdfRetrieveRequest) -> PdfResponse:
        data = request.to_request()
        url = self.client.instance_url(f"/mandate/pdf?mndtId={data.get('mndtId')}")
        try:
            self.client.refresh_token_if_required()
            response = requests.get(
                url=url, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("pdf", response)
            filename = None
            if "Content-Disposition" in response.headers:
                disposition = response.headers["Content-Disposition"]
                parts = disposition.split("=")
                if len(parts) == 2:
                    filename = parts[1].strip().strip('"')
            return PdfResponse(content=response.content, filename=filename)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("detail", e)

    def update_customer(self, customer_id, data):
        url = self.client.instance_url("/customer/" + str(customer_id))
        try:
            self.client.refresh_token_if_required()
            response = requests.patch(
                url=url, params=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Cancel", response)
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("Update customer", e)

    def customer_access(self, request: CustomerAccessRequest) -> CustomerAccessResponse:
        data = request.to_request()
        url = self.client.instance_url("/customeraccess")
        try:
            self.client.refresh_token_if_required()
            response = requests.post(
                url=url, data=data, headers=self.client.headers(), timeout=15
            )
            if "ApiErrorCode" in response.headers:
                raise self.client.raise_error("Cancel", response)
            return CustomerAccessResponse(**response.json())
        except requests.exceptions.RequestException as e:
            raise self.client.raise_error_from_request("customer access", e)


class DocumentFeed:
    def start(self, position, number_of_updates):
        """
        Allow storing the start of the feed
        Useful for storing or logging the current feed position and the number of items
        :param position: position where the feed started returned by the 'X-LAST' header
        :param number_of_updates: number of items in the feed
        """
        pass

    def new_document(self, doc, evt_time) -> bool:
        """
        Handle a newly available document
        :param doc: actual document as a dictionary
        :param evt_time: time of creation (ISO 8601 format)
        :return: Return True if an error occurred else return False
        """
        pass

    def updated_document(self, original_doc_number, doc, reason, evt_time) -> bool:
        """
        Handle an update of a document
        :param original_doc_number: original reference to the document
        :param doc: actual document as a dictionary
        :param reason: reason of change as a dictionary
        :param evt_time: time of creation (ISO 8601 format)
        :return: Return True if an error occurred else return False
        """
        pass

    def cancelled_document(self, doc_number, reason, evt_time) -> bool:
        """
        Handle a cancelled document
        :param doc_number: reference to the document
        :param reason: reason of cancellation  as a dictionary
        :param evt_time: time of creation (ISO 8601 format)
        :return: Return True if an error occurred else return False
        """
        pass
