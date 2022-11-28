from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from note.models import Note
from note.api.serializers import NoteSerializer


class NoteListAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        notes = Note.objects.filter(user=request.user)
        serializers = NoteSerializer(notes, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            Note.objects.create(user=request.user,title=serializer.validated_data['title'],body=serializer.validated_data['body'])
            return Response({'Message': 'Note Created successfully.'})
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class NoteDetailAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object_by_id(self, id):
        try:
            note = Note.objects.get(id=id)
        except Note.DoesNotExist:
            note = None
        return note

    def get(self, request, id, format=None):
        note = self.get_object_by_id(id=id)
        if note is None:
            return Response({'Message': 'Error... No Record Found!'}, status=status.HTTP_404_NOT_FOUND)
        elif note.user != request.user:
            return Response({'Message': 'Illegal Access Attempt!'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        note = self.get_object_by_id(id=id)
        if note is None:
            return Response({'Message': 'Error... No Record Found!'}, status=status.HTTP_404_NOT_FOUND)
        elif note.user != request.user:
            return Response({'Message': 'Illegal Access Attempt!'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, id, format=None):
        note = self.get_object_by_id(id=id)
        if note is None:
            return Response({'Message': 'Error... No Record Found!'}, status=status.HTTP_404_NOT_FOUND)
        elif note.user != request.user:
            return Response({'Message': 'Illegal Access Attempt!'}, status=status.HTTP_401_UNAUTHORIZED)
        elif note is not None and note.user == request.user:
            note.delete()
            return Response({'Message': 'Note deleated successfully.'})
