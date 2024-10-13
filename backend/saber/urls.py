from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, MunicipalityViewSet, HighschoolViewSet, CollegeViewSet

router = DefaultRouter()

router.register(r'department', DepartmentViewSet)

router.register(r'municipality', MunicipalityViewSet)

router.register(r'highschool', HighschoolViewSet)

router.register(r'college', CollegeViewSet)

urlpatterns = router.urls
