import requests
from dadata import Dadata
from django.conf import settings
from core.models import User
from django.http import Http404
from rest_framework import permissions, mixins
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.api.filters import CompanyRecommendFilter
from core.api.serializers import CompanyPropSerializer, CompanyFileSerializer, CompanyRecommendSerializer, \
    CompanySerializer, WarrantySerializer, UserSerializer, UserCompany
from core.models import CompanyProp, CompanyFile, CompanyRecommend, Company, Warranty


class CompanyPropViewSet(ListModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
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


class CompanyFileViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = CompanyFile.objects.all()
    serializer_class = CompanyFileSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyRecommendViewSet(ListModelMixin, GenericViewSet):
    queryset = CompanyRecommend.objects.all()
    serializer_class = CompanyRecommendSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    filter_class = CompanyRecommendFilter

    def get_company(self):
        return Company.objects.get(inn=self.request.GET['company'])

    def get_queryset(self):
        if 'company' in self.request.GET:
            return super().get_queryset().filter(company=self.get_company())
        else:
            return super().get_queryset().filter(company__isnull=True)


class WarrantyViewSet(CreateModelMixin, GenericViewSet):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        warranty = serializer.save(user=self.request.user)

        data = {
            "inn": warranty.company.inn,
            "contactName": warranty.contact_name,
            "phone": warranty.phone,
            "email": warranty.email,
            "purchaseNumber": warranty.purchase_number,
            "bgType": warranty.bg_type,
            "bgSum": warranty.bg_sum,
            "purchaseDate": warranty.purchase_date,
            "startDate": warranty.start_date,
            "endDate": warranty.end_date
        }

        requests.post("https://crm.farzoom.ru/api/leads/bg", data=data, headers={
            'API-KEY': 'h67p31tzytziy40zp6m4z0fhj1acee9j'
        })


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'add_company':
            return UserCompany
        else:
            return super().get_serializer_class()

    @action(methods=['get'], detail=False)
    def me(self, *args, **kwargs):
        try:
            instance = self.get_queryset().get(id=self.request.user.id)
        except User.DoesNotExist:
            raise Http404
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['patch'], detail=False)
    def add_company(self, *args, **kwargs):
        company_inn = self.request.data['inn']
        company = Company.objects.get(inn=company_inn)
        self.request.user.companies.add(company)
        return Response(status=204)


class CompanyViewSet(GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.first()
        if not obj:
            return Response(status=404)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def get_queryset(self):
        inn = self.kwargs['inn']
        return super().get_queryset().filter(inn=inn)
