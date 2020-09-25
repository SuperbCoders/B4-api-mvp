from django.contrib import admin

from core.models import Company, CompanyProp, CompanyFile, CompanyRecommend, Warranty, CompanyUser


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_short_name', 'inn', 'ogrn', 'competitor_short_name', 'competitor_inn', 'competitor_ogrn', )


class CompanyPropAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'bank_name', 'account_number', 'bik', 'dadata', )


class CompanyFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'file', )


class CompanyRecommendAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'customer', 'tender_link',)


class WarrantyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact_name', 'phone', 'email', 'purchase_number', 'bg_type',
                    'purchase_date', 'start_date', 'end_date', )


class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'was_processed', 'created_at')
    list_filter = ('company', 'user', 'was_processed', 'created_at')


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyProp, CompanyPropAdmin)
admin.site.register(CompanyFile, CompanyFileAdmin)
admin.site.register(CompanyRecommend, CompanyRecommendAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
