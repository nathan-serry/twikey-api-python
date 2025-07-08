class MandateActionRequest:
    """
    MandateActionRequest holds parameters to perform actions on a mandate
    via the Twikey API.

    Attributes:
        mndtId (str): Mandate reference (Twikey internal ID). Required.
        invite (bool, optional): If True, send an invitation email to the customer.
        reminder (bool, optional): If True, send a reminder email to the customer.
        access (bool, optional): If True, send the customer a link to access their mandate.
        automaticCheck (bool, optional): If True, enable automatic validation for B2B mandates.
        manualCheck (bool, optional): If True, disable automatic validation for B2B mandates.
    """

    __slots__ = ["mndt_id", "type", "reminder"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {"mndtId": self.mndt_id, "type": self.type}
        if self.reminder is not None and self.reminder != "":
            retval["reminder"]=self.reminder
        return retval
