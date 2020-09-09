from django.contrib import admin

from core.models import Company, CompanyProp, CompanyFile, CompanyRecommend, Warranty


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'inn', 'ogrn', 'competitor_short_name', 'competitor_inn', 'competitor_ogrn', )


class CompanyPropAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'bank_name', 'account_number', 'bik', 'dadata', )


class CompanyFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'file', )


class CompanyRecommendAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'competitor_full_name', 'competitor_short_name', 'competitor_growth_percent',
                    'account_number', 'total', 'published_at', 'federal_law', 'warranty_approved', 'warranty_sum', )


class WarrantyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact_name', 'phone', 'email', 'purchase_number', 'bg_type', 'bg_sum',
                    'purchase_date', 'start_date', 'end_date', )


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyProp, CompanyPropAdmin)
admin.site.register(CompanyFile, CompanyFileAdmin)
admin.site.register(CompanyRecommend, CompanyRecommendAdmin)
admin.site.register(Warranty, WarrantyAdmin)
