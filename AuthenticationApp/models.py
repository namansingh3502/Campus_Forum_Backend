import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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

    DEPARTMENT = (
        ('CSE', 'CSE'),
        ('ISE', 'ISE'),
        ('ECE', 'ECE'),
        ('EEE', 'EEE'),
        ('CIVIL', 'CIVIL'),
        ('MECH', 'MECH')
    )

    GENDER = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )

    middle_name = models.CharField(
        _("Middle Name"),
        max_length=150,
        blank=True
    )
    phone = models.CharField(
        _("Mobile No."),
        max_length=10
    )
    gender = models.CharField(
        _("Gender"),
        max_length=1,
        choices=GENDER,
    )
    department = models.CharField(
        _("Department"),
        choices=DEPARTMENT,
        max_length=5
    )
    user_image = models.URLField(
        _("Profile Picture"),
        default="https://firebasestorage.googleapis.com/v0/b/forum-image-storage.appspot.com/o/default.jpeg?alt=media"
                "&token=1c3af8d5-0028-417a-bc64-8f817c39a0c0"
    )
    cover_photo = models.URLField(
        _("Cover Photo"),
        default="https://firebasestorage.googleapis.com/v0/b/forum-image-storage.appspot.com/o/bg.jpeg?alt=media"
                "&token=6e277919-54af-4c40-b0eb-32b3226facde"
    )

    AbstractUser._meta.get_field('first_name').blank = False
    AbstractUser._meta.get_field('first_name').null = False
    AbstractUser._meta.get_field('last_name').blank = False
    AbstractUser._meta.get_field('last_name').null = False
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('email').null = False

    class Meta:
        db_table = "User_Profile"

    def __str__(self):
        return self.username
