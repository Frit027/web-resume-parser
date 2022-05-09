from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Resume
from django.core.files.base import ContentFile
from .json_creator import JSONCreator
from .file_converter import FileConverter
from .utilities import get_json_filename
import json


@login_required
def main_page(request):
    is_files_loaded = False

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            converter = FileConverter()
            json_creator = JSONCreator()

            for file in request.FILES.getlist('file_field'):
                resume = Resume(file=file, user=request.user)
                resume.save()
                json_str = json_creator.create_json(converter.get_text(resume.file.path))
                resume.json.save(get_json_filename(resume.file.name), ContentFile(json_str))

                with open(resume.json.path, 'r', encoding='utf-8') as f:
                    print(json.load(f))

            is_files_loaded = True
    else:
        form = DocumentForm()

    return render(
        request,
        'resume/main_page.html',
        {'section': 'main_page', 'form': form, 'is_files_loaded': is_files_loaded}
    )
