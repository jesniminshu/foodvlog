from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=10)