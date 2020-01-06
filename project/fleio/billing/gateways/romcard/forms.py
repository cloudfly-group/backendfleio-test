from django import forms


class RomcardPayForm(forms.Form):
    """User payment form"""
    AMOUNT = forms.CharField(widget=forms.HiddenInput())
    CURRENCY = forms.CharField(widget=forms.HiddenInput())
    ORDER = forms.CharField(widget=forms.HiddenInput())
    DESC = forms.CharField(widget=forms.HiddenInput())
    MERCH_NAME = forms.CharField(widget=forms.HiddenInput())
    MERCH_URL = forms.CharField(widget=forms.HiddenInput())
    MERCHANT = forms.CharField(widget=forms.HiddenInput())
    TERMINAL = forms.CharField(widget=forms.HiddenInput())
    EMAIL = forms.CharField(widget=forms.HiddenInput())
    TRTYPE = forms.CharField(widget=forms.HiddenInput())
    COUNTRY = forms.CharField(widget=forms.HiddenInput(), required=False)
    MERCH_GMT = forms.CharField(widget=forms.HiddenInput(), required=False)
    TIMESTAMP = forms.CharField(widget=forms.HiddenInput())
    NONCE = forms.CharField(widget=forms.HiddenInput())
    BACKREF = forms.CharField(widget=forms.HiddenInput())
    P_SIGN = forms.CharField(widget=forms.HiddenInput())
    LANG = forms.CharField(widget=forms.HiddenInput())


class RomcardSubscribeForm(forms.Form):
    """Subscription adds two fields"""
    AMOUNT = forms.CharField(widget=forms.HiddenInput())
    CURRENCY = forms.CharField(widget=forms.HiddenInput())
    ORDER = forms.CharField(widget=forms.HiddenInput())
    DESC = forms.CharField(widget=forms.HiddenInput())
    MERCH_NAME = forms.CharField(widget=forms.HiddenInput())
    MERCH_URL = forms.CharField(widget=forms.HiddenInput())
    MERCHANT = forms.CharField(widget=forms.HiddenInput())
    TERMINAL = forms.CharField(widget=forms.HiddenInput())
    EMAIL = forms.CharField(widget=forms.HiddenInput())
    TRTYPE = forms.CharField(widget=forms.HiddenInput())
    COUNTRY = forms.CharField(widget=forms.HiddenInput(), required=False)
    MERCH_GMT = forms.CharField(widget=forms.HiddenInput(), required=False)
    TIMESTAMP = forms.CharField(widget=forms.HiddenInput())
    NONCE = forms.CharField(widget=forms.HiddenInput())
    BACKREF = forms.CharField(widget=forms.HiddenInput())
    RECUR_FREQ = forms.CharField(widget=forms.HiddenInput(), required=False)
    RECUR_EXP = forms.CharField(widget=forms.HiddenInput(), required=False)
    P_SIGN = forms.CharField(widget=forms.HiddenInput())
    LANG = forms.CharField(widget=forms.HiddenInput())


class BaseCaptureForm(forms.Form):
    """Base form for capture or refund"""
    ORDER = forms.CharField(widget=forms.HiddenInput())
    AMOUNT = forms.CharField(widget=forms.HiddenInput())
    CURRENCY = forms.CharField(widget=forms.HiddenInput())
    INT_REF = forms.CharField(widget=forms.HiddenInput())
    TRTYPE = forms.CharField(widget=forms.HiddenInput())
    TERMINAL = forms.CharField(widget=forms.HiddenInput())
    TIMESTAMP = forms.CharField(widget=forms.HiddenInput())
    NONCE = forms.CharField(widget=forms.HiddenInput())
    BACKREF = forms.CharField(widget=forms.HiddenInput())
    P_SIGN = forms.CharField(widget=forms.HiddenInput())


class RomcardCaptureRefundForm(BaseCaptureForm):
    """Capture or Refund form"""
    RRN = forms.CharField(widget=forms.HiddenInput())


class RomcardRecurringForm(BaseCaptureForm):
    """Recurring transactions replaces the RRN field with RECUR_REF"""
    RECUR_REF = forms.CharField(widget=forms.HiddenInput())
