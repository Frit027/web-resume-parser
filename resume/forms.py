from django import forms
from .models import Resume
import os


class DocumentForm(forms.ModelForm):
    __ALLOWED_TYPES = ('PDF', 'DOCX')
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Resume
        fields = ('file_field',)

    def clean(self):
        for file in self.files.getlist('file_field'):
            extension = os.path.splitext(file.name)[1][1:].upper()
            if extension in self.__ALLOWED_TYPES:
                return file
            else:
                raise forms.ValidationError(f"Разрешены файлы форматов {', '.join(self.__ALLOWED_TYPES)}.")
