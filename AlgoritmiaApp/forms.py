from django import forms

class TableroForm(forms.Form):
    n = forms.IntegerField(label='Tamaño del tablero', min_value=1, max_value=20)

class ArchivoForm(forms.Form):
    archivo = forms.FileField(label='Selecciona el archivo de tarjetas (.in)')
