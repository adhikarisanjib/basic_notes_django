from turtle import title
from django.shortcuts import redirect, render
from django.contrib import messages

from note.models import Note
from note.forms import NoteForm


def get_note_by_id(id):
    try:
        note = Note.objects.get(id=id)
        return note
    except Note.DoesNotExist:
        return None


def note_view(request, *arga, **kwargs):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'You must login to create or update notes.')
        return redirect('home')

    context = {}
    if request.method == 'POST':
        note_id = kwargs.get('note_id')
        if note_id:
            note = Note.objects.get(id=note_id)
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                messages.success(request, 'Note updated Successfully!!')
                return redirect('home')
        else:
            form = NoteForm(request.POST)
            if form.is_valid():
                note = Note.objects.create(
                    user=request.user, title=request.POST.get('title'), body=request.POST.get('body'))
                note.save()
                messages.success(request, 'Note Added Successfully.')
                return redirect('home')

    if request.method == 'GET':
        note_id = kwargs.get('note_id')
        if note_id:
            note = Note.objects.get(id=note_id)
            form = NoteForm(instance=note)
            context['action'] = 'Update'
            context['note'] = note
            context['form'] = form
            context['can_delete'] = True
        else:
            form = NoteForm()
            context['action'] = 'Add'
            context['form'] = form

    return render(request, 'note/note.html', context)


def note_delete_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'You must login to create or update notes.')
        return redirect('home')

    note_id = kwargs.get('note_id')
    note = get_note_by_id(id=note_id)
    if note:
        context['note'] = note
        if not note.user == user:
            messages.warning(request, 'You are not allowed to operate on other persons note.')

        if request.method == 'POST':
            note.delete()
            messages.success(request, 'Note deleted successfully.')
            return redirect('home')

    return render(request, 'note/note_delete.html', context)