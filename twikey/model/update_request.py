class UpdateMandateRequest:
    """
    UpdateMandateRequest holds the parameters for updating a mandate
    via the Twikey API.

    Attributes:
        mndt_id (str): Mandate reference (Twikey internal ID). Required.
        ct (int, optional): Move the document to a different template ID (of the same type).
        state (str, optional): 'active' or 'passive' (activate or suspend mandate).
        mobile (str, optional): Customer's mobile number in E.164 format.
        iban (str, optional): Debtor's IBAN.
        bic (str, optional): Debtor's BIC code.
        customer_number (str, optional): Customer number (add/update or move mandate).
        email (str, optional): Debtor's email address.
        first_name (str, optional): Debtor's first name.
        last_name (str, optional): Debtor's last name.
        company_name (str, optional): Company name on mandate.
        coc (str, optional): Enterprise number (only changeable if companyName is changed).
        l (str, optional): Language code on mandate.
        address (str, optional): Street address (required if updating address).
        city (str, optional): City of debtor (required if updating address).
        zip (str, optional): Zip code of debtor (required if updating address).
        country (str, optional): Country code in ISO format (required if updating address).
    """

    __slots__ = [
        "mndt_id", "ct", "state", "mobile", "iban", "bic", "customer_number",
        "email", "first_name", "last_name", "company_name", "coc", "l",
        "address", "city", "zip", "country"
    ]

    _field_map = {
        "mndt_id": "mndtId",
        "ct": "ct",
        "state": "state",
        "mobile": "mobile",
        "iban": "iban",
        "bic": "bic",
        "customer_number": "customerNumber",
        "email": "email",
        "first_name": "firstName",
        "last_name": "lastName",
        "company_name": "companyName",
        "coc": "coc",
        "l": "l",
        "address": "address",
        "city": "city",
        "zip": "zip",
        "country": "country",
    }

    def __init__(self, mndt_id: str, **kwargs):
        self.mndt_id = mndt_id
        for attr in self.__slots__:
            if attr == "mndt_id":
                continue
            setattr(self, attr, kwargs.get(attr, None))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr)
            if value is not None:
                key = self._field_map.get(attr, attr)
                if isinstance(value, bool):
                    retval[key] = "true" if value else "false"
                else:
                    retval[key] = value
        return retval