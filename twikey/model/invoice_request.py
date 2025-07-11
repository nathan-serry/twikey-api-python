class InvoiceRequest:
    """
    InvoiceRequest holds the full set of fields used to create an invoice via the Twikey API.

    Attributes:
    id (str): UUID of the invoice
    number (str): Invoice number (unique identifier). (required)
    title (str): Title or description for the invoice.
    remittance (str): Payment message, defaults to title if not specified.
    ref (str): Internal reference for your system.
    ct (str): Contract template identifier.
    amount (float): Amount to be billed. (required)
    date (str): Invoice issue date (YYYY-MM-DD). (required)
    duedate (str): Due date for payment (YYYY-MM-DD). (required)
    locale (str): Language of the invoice (e.g., 'nl', 'fr', 'de').
    manual (bool): Whether the invoice should be collected automatically.
    pdf (str): Base64-encoded PDF content.
    pdf_url (str): URL pointing to a downloadable PDF.
    redirect_url (str): Redirect URL after payment.
    email (str): Custom email address for invoicing.
    related_invoice_number (str): Reference to link a credit note to an invoice.
    cc (str): Comma-separated CC emails.
    customer (Customer): Nested Customer details.
    lines (list[LineItem]): Optional invoice line items.
    """

    __slots__ = [
        "id", "number", "title", "remittance", "ref", "ct", "amount", "date", "duedate", "locale",
        "manual", "pdf", "pdf_url", "redirect_url", "email", "related_invoice_number", "cc",
        "customer", "lines"
    ]

    _field_map = {
        "id": "id",
        "number": "number",
        "title": "title",
        "remittance": "remittance",
        "ref": "ref",
        "ct": "ct",
        "amount": "amount",
        "date": "date",
        "duedate": "duedate",
        "locale": "locale",
        "manual": "manual",
        "pdf": "pdf",
        "pdf_url": "pdfUrl",
        "redirect_url": "redirectUrl",
        "email": "email",
        "related_invoice_number": "relatedInvoiceNumber",
        "cc": "cc",
        "customer": "customer",
        "lines": "lines",
    }

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_request(self) -> dict:
        retval = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                key = self._field_map.get(attr, attr)
                if isinstance(value, bool):
                    retval[key] = "true" if value else "false"
                elif isinstance(value, list):
                    retval[key] = [item.to_dict() for item in value]
                elif hasattr(value, "to_dict"):
                    retval[key] = value.to_dict()
                else:
                    retval[key] = value
        return retval


class Customer:
    """
    Customer contains customer information used in an invoice.

    Attributes:
        customer_number (str): Unique customer ID. (required if object is passed or email)
        email (str): Email address. (required if object is passed or customer_number)
        first_name (str): First name.
        last_name (str): Last name.
        company_name (str): Optional company name.
        coc (str): Chamber of commerce number.
        lang (str): Language.
        address (str): Street address.
        city (str): City.
        zip (str): Postal code.
        country (str): Country code.
        mobile (str): Mobile number.
        customer_by_document (str): Mandate number.
        customer_by_ref (str): Alternative reference.
    """
    __slots__ = [
        "customer_number", "email", "first_name", "last_name", "company_name", "coc", "lang",
        "address", "city", "zip", "country", "mobile", "customer_by_document", "customer_by_ref"
    ]

    _field_map = {
        "customer_number": "customerNumber",
        "email": "email",
        "first_name": "firstname",
        "last_name": "lastname",
        "company_name": "companyName",
        "coc": "coc",
        "lang": "lang",
        "address": "address",
        "city": "city",
        "zip": "zip",
        "country": "country",
        "mobile": "mobile",
        "customer_by_document": "customerByDocument",
        "customer_by_ref": "customerByRef",
    }

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_dict(self):
        data = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                key = self._field_map.get(attr, attr)
                data[key] = value
        return data


class LineItem:
    """
    LineItem represents a line in the invoice.

    Attributes:
        code (str): Code of the item.
        description (str): Description of the item.
        quantity (float): Number of units.
        uom (str): Unit of measurement.
        unitprice (float): Price per unit.
        vatcode (str): VAT code.
        vatsum (float): VAT amount.
    """
    __slots__ = [
        "code", "description", "quantity", "uom", "unitprice", "vatcode", "vatsum"
    ]

    _field_map = {
        "code": "code",
        "description": "description",
        "quantity": "quantity",
        "uom": "uom",
        "unitprice": "unitprice",
        "vatcode": "vatcode",
        "vatsum": "vatsum",
    }

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def to_dict(self):
        data = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is not None and value != "":
                key = self._field_map.get(attr, attr)
                data[key] = value
        return data

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
    """

    __slots__ = ["id", "number", "title", "ct", "amount", "date", "duedate", "status", "url"]

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr))

    def __str__(self):
        return "\n".join(f"{attr:<10}: {getattr(self, attr, None)}" for attr in self.__slots__)