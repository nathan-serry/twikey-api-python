class FetchMandateRequest:
    """
    FetchMandateRequest holds the parameters required to fetch
    the details of a specific mandate from the Twikey API.

    Attributes:
        mndtId (str): Mandate reference (Twikey's internal ID). Required.
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

class FetchResponse:
    __slots__ = ["MndtId", "State", "LclInstrm", "SeqTp", "Cdtr", "Dbtr", "DbtrAcct", "SignerMethod"]

    def __init__(self, **kwargs):
        Mndt = kwargs.get("Mndt", {})
        self.MndtId = Mndt.get("MndtId")
        self.State = kwargs.get("headers", {}).get("X-STATE")
        self.LclInstrm = Mndt.get("LclInstrm")
        self.SeqTp = Mndt.get("Ocrncs").get("SeqTp")
        self.Cdtr = Mndt.get("Cdtr").get("Nm")
        self.Dbtr = Mndt.get("Dbtr").get("Nm")
        self.DbtrAcct = Mndt.get("DbtrAcct")


        # Extract 'SignerMethod' from SplmtryData
        supp_data = Mndt.get("SplmtryData", [])
        for item in supp_data:
            if item.get("Key") == "SignerMethod#0":
                self.SignerMethod = item.get("Value")
            else:
                self.SignerMethod = None

    def __str__(self):
        return (
            f"MndtId {self.MndtId}: State {self.State} \n"
            f"LclInstrm={self.LclInstrm} \n"
            f"SeqTp={self.SeqTp} \n"
            f"Cdtr={self.Cdtr} \n"
            f"Dbtr={self.Dbtr} \n"
            f"DbtrAcct={self.DbtrAcct} \n"
            f"SignerMethod={self.SignerMethod}"
        )