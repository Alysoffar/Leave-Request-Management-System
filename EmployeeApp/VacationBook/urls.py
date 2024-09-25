from django.urls import path, include # type: ignore
from rest_framework.routers import DefaultRouter 
from . views import LeaveRequstViewSet

router = DefaultRouter()
router.register(r'leave_request', LeaveRequstViewSet, basename='leave_request')

urlpatterns = [
]+router.urls