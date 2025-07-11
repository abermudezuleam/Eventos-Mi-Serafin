import re

from django import forms
from django.core.exceptions import ValidationError

from apps.clientes.models import Cliente


class ClienteRegistroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['identificacion', 'nombres', 'apellidos',
                  'correo', 'nacionalidad', 'telefono', 'genero']
        widgets = {
            'identificacion': forms.TextInput(attrs={'placeholder': 'Ej: 1234567890'}),
            'nombres': forms.TextInput(attrs={'placeholder': 'Ej: Juan Carlos'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Ej: Pérez García'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Ej: ejemplo@correo.com'}),
            'nacionalidad': forms.TextInput(attrs={'placeholder': 'Ej: Ecuatoriana'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: 0987654321'}),
        }

    GENERO_CHOICES = [
        ('', 'Selecciona tu género'),
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    genero = forms.ChoiceField(choices=GENERO_CHOICES, required=True)

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        if not identificacion:
            raise ValidationError("Este campo es obligatorio.")

        # Validar que contenga solo dígitos
        if not identificacion.isdigit():
            raise ValidationError(
                "La identificación debe contener solo números.")

        # Validar longitud
        if len(identificacion) != 10:
            raise ValidationError(
                "La identificación debe contener exactamente 10 dígitos.")

        return identificacion

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if not nombres:
            raise ValidationError("Este campo es obligatorio.")

        # Validar que contenga solo letras y espacios
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nombres):
            raise ValidationError(
                "El nombre solo debe contener letras y espacios.")

        # Validar que contenga al menos dos palabras
        palabras = nombres.strip().split()
        if len(palabras) < 2:
            raise ValidationError("Debes ingresar al menos dos nombres.")

        return nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos:
            raise ValidationError("Este campo es obligatorio.")

        # Validar que contenga solo letras y espacios
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', apellidos):
            raise ValidationError(
                "El apellido solo debe contener letras y espacios.")

        # Validar que contenga al menos dos palabras
        palabras = apellidos.strip().split()
        if len(palabras) < 2:
            raise ValidationError("Debes ingresar al menos dos apellidos.")

        return apellidos

    def clean_nacionalidad(self):
        nacionalidad = self.cleaned_data.get('nacionalidad')
        if nacionalidad and not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nacionalidad):
            raise ValidationError(
                "La nacionalidad solo debe contener letras y espacios.")
        return nacionalidad

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:  # El teléfono es opcional
            if not telefono.isdigit():
                raise ValidationError(
                    "El teléfono debe contener solo números.")
            if len(telefono) != 10:
                raise ValidationError(
                    "El teléfono debe contener exactamente 10 dígitos.")
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if correo and not re.match(email_regex, correo):
            raise ValidationError("Ingrese un correo electrónico válido.")
        return correo
