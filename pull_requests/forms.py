from django import forms


class UserRequestForm(forms.Form):
    link_github = forms.CharField(widget=forms.TextInput())