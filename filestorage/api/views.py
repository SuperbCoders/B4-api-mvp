from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from filestorage.api.serializers import APIFileSerializer

from filestorage.models import APIFile


class APIFileViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = APIFile.objects.all()
    serializer_class = APIFileSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
