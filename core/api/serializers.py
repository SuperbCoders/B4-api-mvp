from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Company, CompanyProp, CompanyFile, CompanyRecommend, Warranty


class CompanyPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProp
        fields = ('id', 'company', 'bank_name', 'account_number', 'bik', 'dadata', )
        read_only_fields = ['dadata']


class CompanyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFile
        fields = ('id', 'company', 'file', )


class CompanyRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRecommend
        fields = ('id', 'company', 'competitor_full_name', 'competitor_short_name', 'competitor_growth_percent',
                  'account_number', 'total', 'published_at', 'federal_law', 'warranty_approved', 'warranty_sum', )


class WarrantySerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranty
        fields = ('id', 'user', 'contact_name', 'phone', 'email', 'purchase_number', 'bg_type', 'bg_sum',
                  'purchase_date', 'start_date', 'end_date', )


class CompanySerializer(serializers.ModelSerializer):
    competitor = serializers.SerializerMethodField(method_name='get_competitor_dict')

    class Meta:
        model = Company
        fields = (
            'inn', 'ogrn', 'company_name', 'company_short_name', 'revenue_2019', 'revenue_2018', 'revenue_growth',
            'revenue_growth_perc', 'purchases_wins', 'purchases_total', 'purchases_lost', 'revenue_lost',
            'bg_overpayment_perc', 'bg_sum', 'competitor',
        )

    def get_competitor_dict(self, obj):
        return {
            "inn": obj.competitor_inn,
            "ogrn": obj.competitor_ogrn,
            "companyName": obj.competitor_full_name,
            "companyShortName": obj.competitor_short_name,
            "revenueGrowthPerc": obj.competitor_growth_percent,
            "purchasesWins": obj.competitor_purchases_wins,
            "purchasesTotal": obj.competitor_purchases_total,
            "bgSavingEconomy": obj.competitor_bg_saving_economy
        }


class UserSerializer(serializers.ModelSerializer):
    companies = CompanySerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'companies',)
