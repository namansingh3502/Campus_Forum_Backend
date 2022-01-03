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
        ('',''),
        ('Dr.','Dr.'),
        ('Mr.', 'Mr.'),
        ('Ms.', 'Miss.'),
        ('Mrs.', 'Mrs.'),
    )

    DEPARTMENT = (
        ('',''),
        ('CSE', 'CSE'),
        ('ISE', 'ISE'),
        ('ECE', 'ECE'),
        ('EEE', 'EEE'),
        ('CIVIL', 'CIVIL'),
        ('MECH','MECH')
    )

    GENDER = (
        ('',''),
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )

    def path_and_rename(instance, filename):
        path = "userimage/"
        file_extension = filename.split('.')[-1]
        format = instance.username + '.' + file_extension
        return os.path.join(path, format)


    prefix = models.CharField(
        "Prefix",
        choices=PREFIX,
        max_length=4,
        blank=True
    )

    middle_name = models.CharField("Middle Name", max_length=150, blank=True)
    phone = models.CharField("Mobile No.", max_length=10, blank=True)
    gender = models.CharField("Gender", max_length=1, blank=True)

    department = models.CharField(
        "Department",
        choices=DEPARTMENT,
        max_length=5,
        blank=True
    )
    user_image = models.FileField(
        "User Image",
        upload_to=path_and_rename,
        blank=True
    )

    member_of = models.ManyToManyField(
        "Forum_App.Channel",
        verbose_name="Channel Member",
        blank=True
    )

    def __str__(self):
        return self.username