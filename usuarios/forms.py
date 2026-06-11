from django import forms
from django.contrib.auth.models import User
from .models import CodigoAcceso
from .models import Video

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    codigo = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')

        try:
            codigo_obj = CodigoAcceso.objects.get(codigo=codigo, usado=False)
        except CodigoAcceso.DoesNotExist:
            raise forms.ValidationError("Código inválido o ya utilizado")

        return codigo
    

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['titulo', 'descripcion', 'archivo']    
