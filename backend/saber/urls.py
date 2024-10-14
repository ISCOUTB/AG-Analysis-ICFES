from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, MunicipalityViewSet, HighschoolViewSet, CollegeViewSet, PeriodViewSet

router = DefaultRouter()

router.register(r'department', DepartmentViewSet)

router.register(r'municipality', MunicipalityViewSet)

router.register(r'highschool', HighschoolViewSet)

router.register(r'college', CollegeViewSet)

router.register(r'period', PeriodViewSet)

urlpatterns = router.urls
