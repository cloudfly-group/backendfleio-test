import json
from django import forms
from django.utils.translation import ugettext_lazy as _


class SimpleInvoicePaymentForm(forms.Form):
    invoice = forms.CharField(max_length=16, widget=forms.HiddenInput())
    token = forms.CharField(max_length=2048, widget=forms.HiddenInput())

    def clean_token(self):
        json_token = self.cleaned_data['token']
        try:
            json_token = json.loads(json_token)
        except Exception:
            raise forms.ValidationError('Invalid token')
        return json_token


class SetupRecurringPaymentsForm(forms.Form):
    invoice = forms.CharField(max_length=16, widget=forms.HiddenInput())
    payment_intent = forms.CharField(max_length=2048, widget=forms.HiddenInput())


class StripeRefundForm(forms.Form):
    REASON_CHOICES = (('duplicate', _('Duplicate')),
                      ('fraudulent', _('Fraudulent')),
                      ('requested_by_customer', _('Requested by customer')))
    transaction_id = forms.CharField(max_length=255, widget=forms.HiddenInput())
    reason = forms.ChoiceField(choices=REASON_CHOICES, required=False)
    # TODO: remove hidden input for amount when we support partial refunds
    amount = forms.DecimalField(max_digits=16, decimal_places=2, min_value=0, widget=forms.HiddenInput())
    metadata = forms.CharField(max_length=1024, widget=forms.HiddenInput(), required=False)
