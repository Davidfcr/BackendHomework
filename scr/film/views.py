from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import FilmSerializer
from .models import Film
from user.authjwt import AuthenticationJWT


class FilmUserAPIView(ListCreateAPIView):
    authentication_classes = [AuthenticationJWT]
    permission_classes = (IsAuthenticated,)
    serializer_class = FilmSerializer

    def perform_create(self, serializer):
        return serializer.save(added_by=self.request.user)

    def get_queryset(self):
        return Film.objects.filter(added_by=self.request.user)


class FilmListAllAPIView(ListAPIView):
    authentication_classes = [AuthenticationJWT]
    permission_classes = (IsAuthenticated,)
    serializer_class = FilmSerializer
    queryset = Film.objects.filter(is_private=False)


class FilmUpdateAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [AuthenticationJWT]
    permission_classes = (IsAuthenticated,)
    serializer_class = FilmSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Film.objects.filter(added_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            film = self.get_object()
            serializer = self.get_serializer(film)
            return Response(serializer.data)
        except:
            return Response({'message': "The current user doesn't have permission to view this item"},
                            status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        try:
            film = self.get_object()
            serializer = self.serializer_class(film, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': "The current user doesn't have permission to edit this item"},
                            status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            film = self.get_object()
            if film.added_by == self.request.user:
                return self.destroy(request, *args, **kwargs)
        except:
            return Response({'message': "The current user doesn't have permission to edit this item"},
                            status=status.HTTP_401_UNAUTHORIZED)
