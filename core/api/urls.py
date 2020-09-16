from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from core.api.views import CompanyPropViewSet, CompanyFileViewSet, CompanyRecommendViewSet, CompanyViewSet, \
    WarrantyViewSet, UserViewSet

urlpatterns = []

router = routers.DefaultRouter(trailing_slash=True)
router.register('company_props', CompanyPropViewSet, basename='company_props')
router.register('company_files', CompanyFileViewSet, basename='company_files')
router.register('company_recommends', CompanyRecommendViewSet, basename='company_recommends')
router.register('warranties', WarrantyViewSet, basename='warranties')
router.register('companies/(?P<inn>[0-9]+)', CompanyViewSet, basename='companies')
router.register('me', UserViewSet, basename='users')

urlpatterns += router.urls

schema_view = get_schema_view(
    openapi.Info(title="API", default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json', ),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui', ),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc', ),
]
