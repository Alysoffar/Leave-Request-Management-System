from .models import LeaveRequest
from .serializers import VacationSerializer
from rest_framework import viewsets , mixins 
from rest_framework.permissions import IsAuthenticated , AllowAny


class LeaveRequstViewSet(viewsets.GenericViewSet,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin):
    

    queryset = LeaveRequest.objects.all()
    serializer_class = VacationSerializer
    permission_classes = [IsAuthenticated]