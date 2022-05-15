from django import forms
from .models import Resume
import os


class DocumentForm(forms.ModelForm):
    __ALLOWED_TYPES = ('PDF', 'DOCX')
    file_field = forms.FileField(label='',
                                 widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))

    class Meta:
        model = Resume
        fields = ('file_field',)

    def clean_file_field(self):
        for file in self.files.getlist('file_field'):
            extension = os.path.splitext(file.name)[1][1:].upper()
            if extension not in self.__ALLOWED_TYPES or not extension:
                raise forms.ValidationError(f'Разрешены файлы форматов PDF и DOCX.')
        return self.files.getlist('file_field')
