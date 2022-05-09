from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Resume


@login_required
def main_page(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for f in files:
                Resume(file=f, user=request.user).save()
    else:
        form = DocumentForm()

    return render(request, 'resume/main_page.html', {'section': 'main_page', 'form': form})
