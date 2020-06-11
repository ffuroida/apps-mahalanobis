from django import forms

class MahalanobisCreateForm(forms.Form):
    class Meta:
        fields = '__all__'

    nama = forms.FileField(
        widget = forms.FileInput(
            attrs = {'placeholder' : 'harus dimasukkan'}
        ),
        label = 'Nama', 
        required = False
    )        