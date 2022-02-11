from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


class GetOTPForm(forms.Form):
    """
    Unfortunately we can't check User exist or not at this screen by the
    security reasons - if we will show error when User doesn't exist,
    attacker can just check all the emails.
    """

    email = forms.EmailField(label=_("Email"))


class CheckOTPForm(GetOTPForm):
    """
    Here we are checking User presence among with OPT check.
    """

    otp = forms.CharField(label=_("OTP"), widget=forms.PasswordInput)

    def clean(self):
        """
        Method that allows to us pass through few validation checks:
            - User DB presence
            - OTP password validity
        """

        username_field = UserModel.USERNAME_FIELD
        username = self.cleaned_data[username_field]
        otp = self.cleaned_data["otp"]

        user = self._get_user(username)
        self._check_password(user, otp)

    def _get_user(self, username: str) -> UserModel:
        """
        Check User presence in our DB or not.
        """

        username_field = UserModel.USERNAME_FIELD
        query_data = {username_field: username}

        try:
            user = UserModel.objects.get(**query_data)
        except UserModel.DoesNotExist:
            message = _("Invalid credentials.")
            code = "invalid_credentials"
            raise forms.ValidationError(message, code)

        return user

    def _check_password(self, user: UserModel, otp: str):
        """
        Check backend cached OTP with user provided OTP.
        """

        if not user.check_password(otp):
            message = _("Invalid credentials.")
            code = "invalid_credentials"
            raise forms.ValidationError(message, code)
