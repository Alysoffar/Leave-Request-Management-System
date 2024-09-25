from rest_framework import serializers
from .models import LeaveRequest
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response 
from user.models import Employee
from rest_framework import status


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = "__all__"



    def validate(self,attrs):
        employee_id = attrs.get('employee_id')
        employee = Employee.objects.get(id=employee_id.id)
        
        if employee.leave_balance >= (attrs['end_date'] - attrs['start_date']).days + 1:
            employee_vacation_balance = LeaveRequest.objects.create(
                employee_id=employee,
                start_date=attrs['start_date'],
                end_date=attrs['end_date'] ,
                status="Pending",
            )

            if employee.manager:
                self.send_leave_notification(employee, self.validated_data)
            else:
                employee_vacation_balance.status = "Accepted"
                employee_vacation_balance.is_accepted = True
                employee_vacation_balance.save()

            return attrs
        else:
            raise ValidationError("Insufficient leave balance.")

    def send_leave_notification(self, employee,request, leave_data):
        manager = employee.manager
        subject = 'Leave Request'
        message = f"A leave request from {employee.username} from {leave_data['start_date']} to {leave_data['end_date']}"
        from_email = employee.email
        to_email = manager.email
        send_mail(subject, message, from_email, [to_email])  # Replace with actual sending mechanism

    def update(self, request, pk=None, *args, **kwargs):
        leave_request = self.get_object()
        employee = leave_request.employee
        manager = employee.manager
        serializer.is_valid(raise_exception=True)
        serializer = self.get_serializer(data=request.data)

        

        if request.data.get('action') == 'approve':
            leave_request.status = "Approved"
            leave_request.is_approved = True
            leave_request.save()
            employee.leave_balance -= (leave_request.end_date - leave_request.start_date).days + 1
            employee.save()  # Update employee leave balance

            subject = 'Leave Request Approved'
            message = f"Your leave request from {leave_request.start_date} to {leave_request.end_date} has been approved."
            from_email = manager.email  # Manager email
            to_email = leave_request.employee.email
            send_mail(subject, message, from_email, [to_email])

            return leave_request

        elif request.data.get('action') == 'reject':
            manager_reason = request.data.get('reason')
            
            if not manager_reason:
                raise ValidationError("Please provide a reason for rejection.")
            

            leave_request.status = "Rejected"
            leave_request.is_approved = False
            leave_request.reason=manager_reason
            leave_request.save()
            subject = 'Leave Request Declined'
            message = manager_reason
            from_email = manager.email 
            to_email = leave_request.employee.email
            send_mail(subject, message, from_email, [to_email])  

