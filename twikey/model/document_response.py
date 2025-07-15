class Document:
    __slots__ = [
        "mandate_id", "state", "local_instream", "sequential_type", "sign_date",
        "debtor_name", "debtor_street", "debtor_city", "debtor_zip", "debtor_country", "btw_nummer",
        "country_of_residence", "debtor_email", "customer_number", "debtor_iban", "Debtor_bic", "debtor_bank",
        "referenced_document", "supplementary_data"
    ]

    def __init__(self, **kwargs):
        mndt = kwargs.get("mandate", {})
        headers = kwargs.get("headers", {})

        self.mandate_id = mndt.get("MndtId")
        self.state = headers.get("X-STATE")
        self.local_instream = mndt.get("LclInstrm")

        ocrncs = mndt.get("Ocrncs", {})
        self.sequential_type = ocrncs.get("SeqTp")
        self.sign_date = ocrncs.get("Drtn", {}).get("FrDt")

        dbtr = mndt.get("Dbtr", {})
        addr = dbtr.get("PstlAdr", {})
        ctct = dbtr.get("CtctDtls", {})

        self.debtor_name = dbtr.get("Nm")
        self.debtor_street = addr.get("AdrLine")
        self.debtor_city = addr.get("TwnNm")
        self.debtor_zip = addr.get("PstCd")
        self.debtor_country = addr.get("Ctry")
        self.btw_nummer = dbtr.get("Id")
        self.country_of_residence = dbtr.get("CtryOfRes")
        self.debtor_email = ctct.get("EmailAdr")
        self.customer_number = ctct.get("Othr")

        self.debtor_iban = mndt.get("DbtrAcct")

        agent = mndt.get("DbtrAgt", {}).get("FinInstnId", {})
        self.Debtor_bic = agent.get("BICFI")
        self.debtor_bank = agent.get("Nm")

        self.referenced_document = mndt.get("RfrdDoc")

        # Convert SplmtryData into a dict for easier use
        self.supplementary_data = {
            item["Key"]: item["Value"]
            for item in mndt.get("SplmtryData", [])
        }

    def __str__(self):

        base_info = "\n".join(
            f"{slot:<22}: {getattr(self, slot, None)}" for slot in self.__slots__ if slot != "supplementary_data"
        )

        supp_info = "Supplimentary Data\n\n"
        for key, value in self.supplementary_data.items():
            supp_info += f"{key:<22}: {value}\n"

        return base_info + "\n\n" + supp_info

    def __repr__(self):
        return self.__str__()


class InviteResponse:
    __slots__ = ["url", "key", "mndtId"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __str__(self):
        return f"InviteResponse url={self.url}, key={self.key}, mndtId={self.mndtId}"


class SignResponse:
    __slots__ = ["MndtId"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __str__(self):
        return (
            f"MndtId {self.MndtId}\n"
        )


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


class CustomerAccessResponse:
    __slots__ = ["token", "url"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __str__(self):
        return f"InviteResponse url={self.url}, token={self.token}"