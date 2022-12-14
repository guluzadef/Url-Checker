from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate

from PIL import Image
from django.core.validators import RegexValidator

# get custom user

domain_validator = RegexValidator(
    regex='@gmail.com',
    message='Domain not valid',
    code='invalid_domain',
)

User = get_user_model()


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        # if len(password2) < 8:
        #     raise forms.ValidationError("Your password should be at least 8 Characters")

        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField(label=_("Password"),
    #                                      help_text=_(
    #                                          "Raw ??ifr??l??r bazada saxlanm??r, onlar?? he?? c??r?? g??rm??k m??mk??n deyil "
    #                                          "bu istifad????inin ??ifr??sidir, lakin siz onu d??yi???? bil??rsiziniz "
    #                                          " <a href=\"../password/\">bu form</a>. vasit??sil??"))

    class Meta:
        model = User
        fields = ("first_name", "last_name",)
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": ""
            }),
            "first_name": forms.TextInput(attrs={
                "class": ""
            }),
            "last_name": forms.TextInput(attrs={
                "class": ""
            }),
            "profile_photo": forms.FileInput(attrs={
                "class": "dropify"
            }),
            "backgroundphoto": forms.FileInput(attrs={
                "class": "dropify"
            }),
            "location": forms.TextInput(attrs={
                "class": ""
            }),
            "headline": forms.TextInput(attrs={
                "class": ""
            }),

        }

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput)


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())
    verify_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        verify_password = self.cleaned_data.get("verify_password")
        if new_password != verify_password:
            raise forms.ValidationError("Not equal")


class ForgetPassword(forms.Form):
    email = forms.EmailField()
