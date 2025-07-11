class PdfRetrieveRequest:
    """
    PdfRetrieveRequest holds the parameter to retrieve
    the PDF document of a mandate via the Twikey API.

    Attributes:
        mndt_id (str): Mandate reference (Twikey internal ID). Required.
    """

    __slots__ = ["mndt_id"]

    def __init__(self, mndt_id: str):
        self.mndt_id = mndt_id

    def to_request(self) -> dict:
        """
        Converts the PdfRetrieveRequest object to a dictionary
        suitable for sending as request parameters in the Twikey API.

        Returns:
            dict: Dictionary containing the mandate reference.
        """
        return {"mndtId": self.mndt_id}

class PdfResponse:
    def __init__(self, content: bytes, filename: str = None, content_type: str = "application/pdf"):
        self.content = content
        self.content_type = content_type
        self.filename = filename or "mandate.pdf"

    def save(self, path: str = None):
        path = path or self.filename
        with open(path, "wb") as f:
            f.write(self.content)
        return path

    def __str__(self):
        return f"PdfResponse(filename='{self.filename}', size={len(self.content)} bytes)"
