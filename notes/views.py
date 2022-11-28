from django.shortcuts import render
from django.db.models import Q

from note.models import Note

def home(request, *args, **kwargs):
    context = {}
    user = request.user

    if request.user.is_authenticated:
        notes = Note.objects.filter(user=user)
        context['notes'] = notes

    if request.method == 'POST':
        query = request.POST.get('noteQuery')
        notes = Note.objects.filter(user=user).filter(Q(title__icontains=query) | Q(body__icontains=query)).distinct()

        context['notes'] = notes
        
    return render(request, 'home.html', context)

def page_not_found_view(request, *args, **kwargs):
    return render(request, '404.html', status=404)
