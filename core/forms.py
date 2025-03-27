from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}))
    email = forms.EmailField(label='Correo', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo electrónico'}))
    subject = forms.CharField(label='Asunto', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    message = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje', 'rows': 6}))
