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

    prefix = models.CharField(
        "Prefix",
        choices=PREFIX,
        max_length=4
    )

    middle_name = models.CharField("Middle Name", max_length=150, blank=True)
    phone = models.CharField("Mobile No.", max_length=10)
    gender = models.CharField("Gender", max_length=1, choices=GENDER)

    department = models.CharField(
        "Department",
        choices=DEPARTMENT,
        max_length=5
    )
    user_image = models.URLField(
        "User Image Path",
        default="https://firebasestorage.googleapis.com/v0/b/forum-image-storage.appspot.com/o/userImage%2Fdefault.jpeg?alt=media&token=e45a56e3-2b3e-4d8c-a905-20c8db1c2dc1"
    )

    def __str__(self):
        return self.username