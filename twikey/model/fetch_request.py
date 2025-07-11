class FetchMandateRequest:
    """
    FetchMandateRequest holds the parameters required to fetch
    the details of a specific mandate from the Twikey API.

    Attributes:
        mndt_Id (str): Mandate reference (Twikey's internal ID). Required.
        force (bool, optional): If True, include non-signed mandate states in the response.
                                Defaults to False.
    """

    __slots__ = ["mndt_id", "force"]

    def __init__(self, mndt_id: str, force: bool = False):
        self.mndt_id = mndt_id
        self.force = force

    def to_request(self) -> dict:
        """
        Converts the FetchMandateRequest object to a dictionary
        suitable for sending as query parameters in the Twikey API.

        Returns:
            dict: Dictionary with keys mapped to API parameters.
        """
        retval = {"mndtId": self.mndt_id}
        if self.force:
            retval["force"] = "true"
        return retval


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
