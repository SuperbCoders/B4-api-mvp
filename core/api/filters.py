from django_filters import rest_framework as filters

from core.models import CompanyRecommend


class CompanyRecommendFilter(filters.FilterSet):

    class Meta:
        model = CompanyRecommend
        fields = ('company', )
