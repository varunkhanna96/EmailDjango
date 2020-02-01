from django import forms
from django.core.validators import EMPTY_VALUES, validate_email


class MultipleEmailField(forms.Field):
    """
    field to get multiple emails
    """
    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("token", ",")
        super(MultipleEmailField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(self.token) if item.strip()]

        return list(set(value))

    def clean(self, value):
        """
        Check that the field contains one or more 'comma-separated' emails
        and normalizes the data to a list of the email strings.
        """
        value = self.to_python(value)

        if value in EMPTY_VALUES and self.required:
            raise forms.ValidationError(_(u"This field is required."))

        for email in value:
            validate_email(email)

        return value


class EmailForm(forms.Form):
    """
    This defines the fields used to send email
    """
    to = MultipleEmailField(required=True)
    bcc = MultipleEmailField(required=False)
    cc = MultipleEmailField(required=False)
    subject = forms.CharField(required=False)
    body = forms.CharField(required=False)
    # file = forms.FileField()
