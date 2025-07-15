class InvoiceCreatedResponse:
    """
    InvoiceResponse maps the response from the Twikey API after creating an invoice.

    Attributes:
        id (str): Unique identifier of the invoice.
        number (str): Invoice number.
        title (str): Title or message associated with the invoice.
        ct (int): Contract template ID.
        amount (float): Amount billed.
        date (str): Invoice creation date.
        duedate (str): Invoice due date.
        status (str): Status of the invoice (e.g., 'BOOKED').
        url (str): URL to view the invoice.
        lines (list[InvoiceLineItem]): Line items on the invoice.
    """

    __slots__ = ["id", "number", "title", "ct", "amount", "date", "duedate", "state", "url", "lines"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            if attr != "lines":
                setattr(self, attr, kwargs.get(attr))
            else:
                self.lines = [InvoiceLineItem(**line) for line in kwargs.get("lines", [])]

    def __str__(self):
        base_info = "\n".join(f"{attr:<10}: {getattr(self, attr, None)}" for attr in self.__slots__)

        line_info = "\n\nLine Items:\n"
        if self.lines:
            for line in self.lines:
                line_info += f" - {str(line)}\n"
        else:
            line_info += " - (none)\n"

        return base_info + line_info


class InvoiceResponse:
    """
    InvoiceDetailsResponse parses the response from the invoice details endpoint.

    Attributes:
        id (str): UUID of the invoice.
        number (str): Invoice number.
        title (str): Invoice title.
        remittance (str): Remittance message.
        ref (str): Custom reference.
        state (str): Status of the invoice.
        amount (float): Invoice amount.
        date (str): Invoice date.
        duedate (str): Invoice due date.
        ct (int): Contract template ID.
        url (str): URL to view the invoice.
        lines (list[InvoiceLineItem]): Line items on the invoice.
        last_payment (list[dict]): Optional list of payment attempts.
        meta (dict): Optional metadata about the invoice.
        customer (dict): Optional full customer information.
    """

    __slots__ = [
        "id", "number", "title", "remittance", "ref", "state", "amount",
        "date", "duedate", "ct", "url", "lines",
        "last_payment", "meta", "customer"
    ]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.number = kwargs.get("number")
        self.title = kwargs.get("title")
        self.remittance = kwargs.get("remittance")
        self.ref = kwargs.get("ref")
        self.state = kwargs.get("state")
        self.amount = kwargs.get("amount")
        self.date = kwargs.get("date")
        self.duedate = kwargs.get("duedate")
        self.ct = kwargs.get("ct")
        self.url = kwargs.get("url")

        # Optional includes
        self.lines = [InvoiceLineItem(**line) for line in kwargs.get("lines", [])]
        self.last_payment = kwargs.get("lastpayment", [])
        self.meta = kwargs.get("meta", {})
        self.customer = kwargs.get("customer", {})

    def __str__(self):
        base_info = "\n".join(
            f"{slot:<15}: {getattr(self, slot, None)}"
            for slot in self.__slots__ if slot not in {"lines", "last_payment", "meta", "customer"}
        )

        line_info = "\n\nLine Items:\n"
        if self.lines:
            for line in self.lines:
                line_info += f" - {str(line)}\n"
        else:
            line_info += " - (none)\n"

        payment_info = "\nLast Payments:\n"
        if self.last_payment:
            for p in self.last_payment:
                payment_info += " - " + ", ".join(f"{k}: {v}" for k, v in p.items()) + "\n"
        else:
            payment_info += " - (none)\n"

        meta_info = ""
        if self.meta:
            meta_info += "\nMeta:\n"
            meta_info += "\n".join(f"{k:<15}: {v}" for k, v in self.meta.items()) + "\n"

        customer_info = ""
        if self.customer:
            customer_info += "\nCustomer:\n"
            customer_info += "\n".join(f"{k:<15}: {v}" for k, v in self.customer.items()) + "\n"

        return base_info + line_info + payment_info + meta_info + customer_info


class InvoiceLineItem:
    """
    InvoiceLineItem represents a single line item on the invoice.

    Attributes:
        code (str): Product or service code.
        description (str): Description of the item.
        quantity (float): Quantity ordered.
        unitprice (float): Unit price (excl. VAT).
        uom (str): Unit of measure (e.g., 'st').
        vatrate (float): VAT rate applied.
        vatsum (float): VAT amount.
    """

    __slots__ = ["code", "description", "quantity", "unitprice", "uom", "vatrate", "vatsum"]

    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.description = kwargs.get("description")
        self.quantity = kwargs.get("quantity")
        self.unitprice = kwargs.get("unitprice")
        self.uom = kwargs.get("uom")
        self.vatrate = kwargs.get("vatrate")
        self.vatsum = kwargs.get("vatsum")

    def __str__(self):
        return f"{self.code:<8} | {self.description:<30} | {self.quantity} x {self.unitprice:.2f} {self.uom} | VAT {self.vatrate:.0f}% = {self.vatsum:.2f}"


class BulkInvoiceResponse:
    """
    BulkInvoiceResponse represents the response after creating invoices in bulk.

    Attributes:
        batch_id (str): The UUID identifier of the created batch.
    """

    __slots__ = ["batch_id"]

    def __init__(self, **kwargs):
        self.batch_id = kwargs.get("batchId")

    def __str__(self):
        return f"Bulk Invoice Batch ID: {self.batch_id}"


class BulkBatchDetailsItem:
    """
    BulkBatchDetailsItem represents the status of a single invoice in a bulk batch.

    Attributes:
        id (str): The invoice ID.
        status (str): Status of the invoice ('OK' or error).
    """

    __slots__ = ["id", "status"]

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.status = kwargs.get("status")

    def __str__(self):
        return f"Invoice ID: {self.id}, Status: {self.status}"


class BulkBatchDetailsResponse:
    """
    BulkBatchDetailsResponse represents the result of a completed bulk invoice upload.

    Attributes:
        results (list[BulkBatchDetailsItem]): List of individual invoice statuses.
    """

    __slots__ = ["results"]

    def __init__(self, raw: list):
        self.results = [BulkBatchDetailsItem(**item) for item in raw]

    def __str__(self):
        return "\n".join(str(item) for item in self.results)
