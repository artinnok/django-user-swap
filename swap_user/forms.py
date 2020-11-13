from django import forms


class BaseUserForm(forms.ModelForm):
    password_1 = forms.CharField(
        label="Enter a new password.", widget=forms.PasswordInput, required=False,
    )
    password_2 = forms.CharField(
        label="Repeat a new password.", widget=forms.PasswordInput, required=False,
    )

    class Meta:
        exclude = ["password"]

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data["password_1"]
        password_2 = cleaned_data["password_2"]

        password_list = [password_1, password_2]
        not_empty_password_list = [item for item in password_list if item]

        # if one of passwords not filled - we are raising exception
        if len(not_empty_password_list) == 1:
            raise forms.ValidationError(
                message="Provide both of passwords",
                code="provide_both_passwords",
            )

        # if passwords doesn't match - we are raising exception
        if password_1 != password_2:
            raise forms.ValidationError(
                message="Passwords should be same", code="password_should_be_same",
            )

        return cleaned_data

    def save(self, commit=False):
        instance = super().save(commit)
        password_1 = self.cleaned_data["password_1"]

        if password_1:
            instance.set_password(password_1)

        instance.save()

        return instance
