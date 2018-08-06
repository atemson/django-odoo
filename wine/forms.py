from django import forms

class CustomerForm(forms.Form):
    name = forms.CharField()
    city = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    #message = forms.CharField(widget=forms.Textarea)
    def save_customer(self):
    	pass