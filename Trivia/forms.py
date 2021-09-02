from django import forms 
# este import incluye los formularios de django, el modelo de usuario predeterminado y el formulario de creacion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model

class UsuarioLoginFormulario(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Este usuario no existe")
            if not user.check_password(password):
                raise forms.ValidationError("Contraseña Incorrecta")
            if not user.is_active:
                raise forms.ValidationError("Este Usuario no está activo")
                
            return super(UsuarioLoginFormulario, self).clean(*args, **kwargs)


class UserRegisterForm(UserCreationForm): #Agregamos los fields que creamos necesarios, ya que 'UserCreationForm' ya posee user, pass1 y pass2
    email= forms.EmailField()
    password1= forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2= forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        #orden en el que van a aparecer los Fields
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:'' for k in fields}