from django.urls import path

from note.views import note_delete_view, note_view, note_delete_view

app_name = 'note'

urlpatterns = [
    path('note/', note_view, name='note'),
    path('note/<note_id>/', note_view, name='note'),
    path('note_delete/<note_id>/', note_delete_view, name='note-delete'),
]
