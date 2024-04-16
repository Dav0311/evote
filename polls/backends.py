
# polls/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Student

class StudentBackend(BaseBackend):
    def authenticate(self, request, firstname=None, registrationNo=None):
        try:
            student = Student.objects.get(firstname=firstname, registrationNo=registrationNo)
            # Create a user instance based on the student
            user, created = User.objects.get_or_create(
                username=student.registrationNo,
                first_name=student.firstname,
                last_name=student.lastname
            )
            return user
        except Student.DoesNotExist:
            return None
