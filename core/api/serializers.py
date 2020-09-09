from rest_framework import serializers

from core.models import Company, CompanyProp, CompanyFile, CompanyRecommend, Warranty


class CompanyPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProp
        fields = ('id', 'company', 'bank_name', 'account_number', 'bik', 'dadata', )


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
    class Meta:
        model = Company
        fields = ('id', 'full_name', 'short_name', 'inn', 'ogrn', 'revenue_2019', 'revenue_2018', 'revenue_growth',
                  'revenue_growth_percent', 'purchases_wins', 'purchases_total', 'purchases_lost', 'revenue_lost',
                  'bg_overpayment_percent', 'bg_sum', 'competitor_inn', 'competitor_ogrn', 'competitor_full_name',
                  'competitor_short_name', 'competitor_growth_percent', 'competitor_purchases_wins',
                  'competitor_purchases_total', 'competitor_bg_saving_economy', )
