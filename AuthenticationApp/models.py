import os
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    """
    Only required columns are added.
    Already Present
        username, password, first_name, last_name, email, is_active,
        is_staff, is_superuser, last_login, date_joined
    Additional Details
        prefix, middle_name, phone, address, id
    """

    PREFIX = (
        ('Dr.','Dr.'),
        ('Mr.', 'Mr.'),
        ('Miss.', 'Miss.'),
        ('Mrs.', 'Mrs.'),
    )

    def path_and_rename(instance, filename):
        path = "userimage/"
        file_extension = filename.split('.')[-1]
        format = instance.username + '.' + file_extension
        return os.path.join(path, format)


    prefix = models.CharField(
        "Prefix",
        choices=PREFIX,
        max_length=5,
        default="Mr."
    )
    middle_name = models.CharField(
        "Middle Name",
        max_length=20,
        blank=True,
        null=True
    )
    phone = models.CharField(
        "Mobile No.",
        max_length=10,
        default=""
    )
    user_id = models.CharField(
        "USN/Staff-Id",
        max_length=10,
        default=""
    )
    address = models.CharField(
        "Address",
        max_length=100,
        default=""
    )
    user_image = models.FileField(
        "User Image",
        upload_to=path_and_rename,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username + " " + self.user_id

class ChannelDetails(models.Model):

    Channel_name = models.CharField(
        max_length=20,
        null=False,
        blank=True
    )
    Channel_admin_1 = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name="Admin_1"
    )
    Channel_admin_2 = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
        related_name="Admin_2"
    )

    def __str__(self):
        return self.Channel_name
