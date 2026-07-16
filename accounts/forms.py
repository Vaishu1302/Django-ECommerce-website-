from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
# from .models import Product
from .models import UserProfile


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:

        model = User

        fields = [

            'username',

            'email',

            'password1',

            'password2'

        ]


class ProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = '__all__'

        exclude = ['user']



# class ProductForm(forms.ModelForm):

#     class Meta:
#         model = Product
#         fields = "__all__"
class ProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            "phone",
            "profile_picture",
            "address",
            "city",
            "state",
            "country",
            "pincode",
        ]

        widgets = {

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "pincode": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }