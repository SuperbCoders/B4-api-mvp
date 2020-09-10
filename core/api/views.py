from dadata import Dadata
from django.conf import settings
from drf_firebase_auth.authentication import FirebaseAuthentication
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.api.serializers import CompanyPropSerializer, CompanyFileSerializer, CompanyRecommendSerializer, \
    CompanySerializer, WarrantySerializer
from core.models import CompanyProp, CompanyFile, CompanyRecommend, Company, Warranty


class CompanyPropViewSet(ModelViewSet):
    queryset = CompanyProp.objects.all()
    serializer_class = CompanyPropSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        dadata = Dadata(settings.DADATA_API_KEY)
        result = dadata.find_by_id("bank", serializer.validated_data['bik'])

        serializer.save(
            user=self.request.user,
            dadata={'result': result},
        )


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
    authentication_classes = []
    pagination_class = None

    def get_queryset(self):
        inn = self.kwargs['inn']
        return super().get_queryset().filter(inn=inn)
