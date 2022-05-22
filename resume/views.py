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
from web_resume_parser.settings import SKILLS


@login_required
def main_page(request):
    if request.method == 'POST':
        if request.POST.get('is_remove_files'):
            Resume.remove_files(request.user)
            return JsonResponse({'is_removed': True})

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            converter = FileConverter()
            json_creator = JSONCreator()

            for file in request.FILES.getlist('file_field'):
                resume = Resume(filename=file.name, file=file, user=request.user)
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
            'section': 'main',
            'form': form,
            'resumes': Resume.get_filenames(request.user)
        }
    )


@login_required
def analysis(request):
    selectors = Resume.get_selectors(request.user)
    if request.method == 'POST':
        levels = request.POST.getlist('levels[]')
        age = request.POST['age']
        experience = request.POST['experience']
        skills_dict = {skill: request.POST.getlist(f'skills[{skill}][]') for skill in SKILLS}

        resumes = Resume.get_resumes_by_filters(request.user, age, experience, levels, skills_dict)
        return JsonResponse({
            'resumes': Resume.get_json_response(resumes)
        })
    return render(request, 'resume/analysis.html', {'section': 'analysis', 'data': selectors})
