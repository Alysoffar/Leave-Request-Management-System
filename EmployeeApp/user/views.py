
from .models import Employee
from django.contrib.auth import logout # type: ignore
from .serializers import EmployeeSerializer,MyTokenObtainPairSerializer
from rest_framework.response import Response 
from rest_framework import status, viewsets , mixins 
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import generics 
from rest_framework.decorators import permission_classes 
from rest_framework_simplejwt.views import TokenObtainPairView


class MyObtainTokenPairView(TokenObtainPairView):
    #permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


@permission_classes([IsAuthenticated])    
class Logout(generics.GenericAPIView):
    def logout(request):
        serializer = EmployeeSerializer
        logout(request)
        return Response('Logged out!') 


class EmployeeViewSet(viewsets.GenericViewSet, 
                      mixins.CreateModelMixin, 
                      mixins.ListModelMixin, 
                      mixins.RetrieveModelMixin):
    
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action == 'create':
            if self.request.user.is_superuser:
                return []  # Allow superusers (no explicit permissions needed)
            return super().get_permissions()
        return super().get_permissions()


    def get_queryset(self):
        """
        Filters the queryset to return only the object for the currently authenticated user.
        """
        if self.action in ['retrieve', 'update', 'list']:
            # Return the employee object associated with the currently authenticated user
            return Employee.objects.filter(user=self.request.user)
        return Employee.objects.all()


