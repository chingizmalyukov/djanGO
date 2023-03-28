from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=40)
    age = forms.IntegerField(label='age', min_value=1, max_value=99)
    bio = forms.CharField(label='your biography', widget=forms.Textarea)


def validae_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('File name should not contain "virus:')


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validae_file_name])
