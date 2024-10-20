from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.messages import MessageFailure


class regisCliente(forms.ModelForm):
    correo= forms.EmailField(required=True)
    contraseña = forms.CharField(widget=forms.PasswordInput, label='password', required=True)

    class Meta:
        model = User
        fields= ['correo','contraseña']

    def clean_correo(self):
        correo= self.cleaned_data.get("correo")
        if User.objects.filter(email=correo).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return correo
    
    def save(self,commit=True):
        usuario = User(
            username=self.cleaned_data['correo'],
            email=self.cleaned_data['correo'],
        )
        usuario.set_password(self.cleaned_data['contraseña'])
        if commit:
            usuario.save()
        return usuario

