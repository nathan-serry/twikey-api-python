class CustomerAccessRequest:
    """
    CustomerAccessRequest holds the parameter to request
    customer access to their mandate via the Twikey API.

    Attributes:
        mndt_id (str): Mandate reference (Twikey internal ID). Required.
    """

    __slots__ = ["mndt_id"]

    def __init__(self, mndt_id: str):
        self.mndt_id = mndt_id


    def to_request(self) -> dict:
        """
        Converts the CustomerAccessRequest object to a dictionary
        suitable for sending as request parameters in the Twikey API.

        Returns:
            dict: Dictionary containing the mandate reference.
        """
        return {"mndtId": self.mndt_id}


class CustomerAccessResponse:
    __slots__ = ["token", "url"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __str__(self):
        return f"InviteResponse url={self.url}, token={self.token}"