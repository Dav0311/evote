from django.db import models

# Create your models here.
class FingerprintData(models.Model):
    fingerprint_template = models.BinaryField()
    fingerprint_image = models.ImageField(upload_to='images/')

class Candidate(models.Model):
    firstname= models.CharField(max_length = 150)
    lastname= models.CharField(max_length = 150)
    post = models.CharField(max_length = 150)
    registrationNo= models.CharField(max_length = 150)
    image= models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Student(models.Model):
    firstname= models.CharField(max_length = 150)
    lastname= models.CharField(max_length = 150)
    registrationNo= models.CharField(max_length = 150)
    image= models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voter_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Vote for {self.candidate} by {self.voter_name}"



