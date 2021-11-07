from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserProfile(models.Model):
    PREFIX = (
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
        ('Mrs.', 'Mrs.'),
    )

    BRANCH = (
        ('CSE', 'CSE'),
        ('ISE', 'ISE'),
        ('ME', 'ME'),
        ('EEE', 'EEE'),
        ('ECE', 'ECE'),
        ('CIVIL', 'CIVIL'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prefix = models.CharField(null=True, max_length=4, choices=PREFIX, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    usn = models.CharField(max_length=10, blank=True)
    branch = models.CharField(max_length=5, choices=BRANCH)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=30, blank=True)

    user_image = models.ImageField(upload_to='user_images', null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

@receiver(post_save, sender=User)
def createUserProfile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
