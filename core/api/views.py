from dadata import Dadata
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from drf_firebase_auth.authentication import FirebaseAuthentication
from rest_framework import permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.api.serializers import CompanyPropSerializer, CompanyFileSerializer, CompanyRecommendSerializer, \
    CompanySerializer, WarrantySerializer, UserSerializer
from core.models import CompanyProp, CompanyFile, CompanyRecommend, Company, Warranty


class CompanyPropViewSet(ModelViewSet):
    queryset = CompanyProp.objects.all()
    serializer_class = CompanyPropSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None

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
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyRecommendViewSet(ModelViewSet):
    queryset = CompanyRecommend.objects.all()
    serializer_class = CompanyRecommendSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (FirebaseAuthentication, )
    pagination_class = None


class WarrantyViewSet(ModelViewSet):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (FirebaseAuthentication, )
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    @action(methods=['get'], detail=False)
    def me(self, *args, **kwargs):
        try:
            instance = self.get_queryset().get(id=self.request.user.id)
        except User.DoesNotExist:
            raise Http404
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CompanyViewSet(GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.AllowAny, )
    authentication_classes = []
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.first()
        if not obj:
            return Response(status=404)
        if request.user.is_authenticated:
            obj.users.add(request.user)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_queryset(self):
        inn = self.kwargs['inn']
        return super().get_queryset().filter(inn=inn)
