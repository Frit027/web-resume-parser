from functools import reduce

from django.shortcuts import render
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import DocumentForm
from .models import Resume
from .json_creator import JSONCreator
from .file_converter import FileConverter
from .utilities import get_json_filename


@login_required
def main_page(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            converter = FileConverter()
            json_creator = JSONCreator()

            for file in request.FILES.getlist('file_field'):
                resume = Resume(file=file, user=request.user)
                resume.save()
                json_str = json_creator.get_json(converter.get_text(resume.file.path))
                resume.json.save(get_json_filename(resume.file.name), ContentFile(json_str))
            return HttpResponseRedirect('/analysis/')
    else:
        form = DocumentForm()

    return render(
        request,
        'resume/main_page.html',
        {
            'section': 'main_page',
            'form': form
        }
    )

@login_required
def analysis(request):
    data = Resume.get_data(request.user)
    resumes = []
    if request.method == 'POST':
        levels = request.POST.getlist('levels')
        age = request.POST['age']
        experience = request.POST['experience']

        skills = {
            'program_lang': request.POST.getlist('program_lang'),
            'stylesheet_lang': request.POST.getlist('stylesheet_lang'),
            'markup_lang': request.POST.getlist('markup_lang'),
            'db': request.POST.getlist('db'),
            'operating_system': request.POST.getlist('operating_system'),
            'version_control': request.POST.getlist('version_control'),
            'ios': request.POST.getlist('ios'),
            'android': request.POST.getlist('android'),
            'ml': request.POST.getlist('ml'),
            'gamedev': request.POST.getlist('gamedev'),
            'testing': request.POST.getlist('testing'),
            'sys_admin': request.POST.getlist('sys_admin'),
            'devops': request.POST.getlist('devops'),
            'frontend': request.POST.getlist('frontend'),
            'backend': request.POST.getlist('backend')
        }

        resumes = Resume.get_resumes_by_filters(request.user, age, experience, levels, skills)
        print(levels, reduce(lambda d, el: d.extend(el) or d, skills.values(), []))
        [print(r.data) for r in resumes]
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    else:
        pass
    return render(request, 'resume/analysis.html', {'data': data, 'resumes': resumes})
