from django.shortcuts import render
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import DocumentForm
from .models import Resume
from .json_creator import JSONCreator
from .file_converter import FileConverter
from .utilities import get_json_filename
from django.http import JsonResponse


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
    if request.method == 'POST':
        skills = ('operating_system', 'stylesheet_lang', 'version_control',
                  'program_lang', 'markup_lang', 'sys_admin', 'frontend',
                  'android', 'testing', 'gamedev', 'backend', 'devops',
                  'ios', 'db', 'ml')
        levels = request.POST.getlist('levels[]')
        age = request.POST['age']
        experience = request.POST['experience']
        skills_dict = {}
        for skill in skills:
            skills_dict[skill] = request.POST.getlist(f'skills[{skill}][]')

        resumes = Resume.get_resumes_by_filters(request.user, age, experience, levels, skills_dict)
        [print(r.data) for r in resumes]
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        return JsonResponse({'resumes': [resume.file.name for resume in resumes]})
    else:
        pass
    return render(request, 'resume/analysis.html', {'data': data})
