from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from authy_admin.models import AuthyAdminUser

class AuthyAuthenticationForm(AuthenticationForm):

    """
    AuthenticationForm that checks Authy Tokens for enabled users
    to enable two-factor authentication for django admin

    """

    authy_token = forms.CharField(required=False, error_messages={
            'not_required': _('Authy Token is not required for this user.'),
            'required': _('Authy Token is required for this user.'),
            'invalid': _('Provided Authy Token is invalid.')})

    def clean(self):

        """
        if the user enters a valid username that corresponds to a user
        configured to use Authy, then check the token's validity
        
        """

        super(AuthyAuthenticationForm, self).clean()

        authy_token = self.cleaned_data['authy_token']
        error_messages = self.fields['authy_token'].error_messages

        if self.get_user():
            try:
                authy_user = AuthyAdminUser.objects.get(user=self.get_user())
                if not authy_token:
                    message = error_messages['required']
                    self._errors["authy_token"] = self.error_class([message])
                elif not authy_user.check_token(authy_token):
                    message = error_messages['invalid']
                    self._errors["authy_token"] = self.error_class([message])
            except AuthyAdminUser.DoesNotExist:
                if authy_token:
                    message = error_messages['not_required']
                    self._errors["authy_token"] = self.error_class([message])

        return self.cleaned_data
