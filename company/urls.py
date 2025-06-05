from rest_framework.routers import SimpleRouter

from company.apps import CompanyConfig

from company.views import CompanyViewSet, ItemViewSet

app_name = CompanyConfig.name

router = SimpleRouter()

router.register(r"company", CompanyViewSet, basename="company")
router.register(r"item", ItemViewSet, basename="item")

urlpatterns = []

urlpatterns += router.urls
