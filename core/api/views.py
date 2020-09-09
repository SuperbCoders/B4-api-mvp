from drf_firebase_auth.authentication import FirebaseAuthentication
from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from core.api.serializers import CompanyPropSerializer, CompanyFileSerializer, CompanyRecommendSerializer, \
    CompanySerializer, WarrantySerializer
from core.models import CompanyProp, CompanyFile, CompanyRecommend, Company, Warranty


class CompanyPropViewSet(ModelViewSet):
    queryset = CompanyProp.objects.all()
    serializer_class = CompanyPropSerializer
    permission_classes = (permissions.IsAuthenticated, )


class CompanyFileViewSet(ModelViewSet):
    queryset = CompanyFile.objects.all()
    serializer_class = CompanyFileSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (FirebaseAuthentication, )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyRecommendViewSet(ModelViewSet):
    queryset = CompanyRecommend.objects.all()
    serializer_class = CompanyRecommendSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (FirebaseAuthentication, )


class WarrantyViewSet(ModelViewSet):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (FirebaseAuthentication, )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.AllowAny, )
    authentication_classes = (FirebaseAuthentication, )

    def get_queryset(self):
        inn = self.kwargs['inn']
        return super().get_queryset().filter(inn=inn)
