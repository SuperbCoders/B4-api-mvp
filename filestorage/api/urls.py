from rest_framework import routers

from filestorage.api.views import APIFileViewSet

urlpatterns = []

router = routers.DefaultRouter(trailing_slash=True)
router.register('api_files', APIFileViewSet, basename='api_files')

urlpatterns += router.urls
