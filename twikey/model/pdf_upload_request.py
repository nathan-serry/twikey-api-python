class PdfUploadRequest:
    """
    PdfUploadRequest holds the parameters to upload a PDF for a mandate via the Twikey API.

    Attributes:
        mndt_id (str): Mandate reference (Twikey internal ID). Required.
        pdf_path (str): Path to the pdf you want to upload. Required
        bankSignature (str, optional): Includes the bank signature, typically "true" or "false". Defaults to "true".
    """

    __slots__ = ["mndt_id", "pdf_path", "bank_signature"]

    def __init__(self, mndt_id: str, pdf_path: str, bank_signature: bool = "true"):
        self.mndt_id = mndt_id
        self.pdf_path = pdf_path
        self.bank_signature = bank_signature


    def to_request(self) -> dict:
        """
        Converts the PdfUploadRequest to a dictionary
        for sending as request parameters to the Twikey API.

        Returns:
            dict: Dictionary of parameters for the PDF upload request.
        """
        retval = {"mndtId": self.mndt_id, "pdfPath": self.pdf_path}
        if self.bank_signature is not None:
            retval["bankSignature"] = self.bank_signature
        return retval