from django.urls import path
from note.api.views import NoteListAPIView, NoteDetailAPIView

app_name = 'note_api'


urlpatterns = [
    path('notes/', NoteListAPIView.as_view(), name='note-list-api'),
    path('note/<id>/', NoteDetailAPIView.as_view(), name='note-detail-api'),
]
