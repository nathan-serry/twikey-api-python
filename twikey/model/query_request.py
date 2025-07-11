class QueryMandateRequest:
    """
    MandateQuery holds the parameters used to query mandates/contracts
    in the Twikey API.

    Attributes:
        iban (str): The IBAN of the contract. Required.
        customer_number (str): The customer number. Required.
        email (str): Email address of the customer. Required.
        state (str, optional): Filter mandates by state (e.g., "SIGNED"). Defaults to "SIGNED".
                               Should be uppercase if specified.
        page (int, optional): Page number for pagination.
    """

    __slots__ = ["iban", "customer_number", "email", "state", "page"]

    def __init__(self, iban: str, customer_number: str, email: str, state: str = "SIGNED", page: int = None):
        self.iban = iban
        self.customer_number = customer_number
        self.email = email
        self.state = state.upper() if state else None
        self.page = page

    def to_request(self) -> dict:
        """
        Converts the MandateQuery object to a dictionary suitable
        for sending as query parameters in the Twikey API request.

        Returns:
            dict: Dictionary with keys mapped to API parameters.
        """
        retval = {
            "iban": self.iban,
            "customerNumber": self.customer_number,
            "email": self.email,
        }
        if self.state:
            retval["state"] = self.state
        if self.page is not None:
            retval["page"] = self.page
        return retval

class QueryMandateResponse:
    __slots__ = [
        "id", "type", "state", "suspended", "pdf_available", "mandate_number",
        "contract_number", "ct", "sign_date", "iban", "bic"
    ]

    def __init__(self, data: dict):
        for key in self.__slots__:
            if "_" in key:
                prefix, suffix = key.split("_")
                datakey = f"{prefix}{suffix.title()}"
                setattr(self, key, data.get(datakey))
            else:
                setattr(self, key, data.get(key))

    def __str__(self):
        return "\n".join(f"{slot:<18}: {getattr(self, slot, None)}" for slot in self.__slots__)
