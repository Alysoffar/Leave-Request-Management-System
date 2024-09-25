from django.urls import path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from .views import EmployeeViewSet,Logout
from rest_framework_simplejwt.views import ( # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'Employee_Profile', EmployeeViewSet, basename='Employee_Profile')

urlpatterns = [
     path('logout/',Logout.as_view(),name='logout'),
     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+router.urls