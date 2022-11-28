from django.contrib import admin

from note.models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_created', 'date_updated')
