from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    """
    Only required columns are added.
    Already Present
        username, password, first_name, last_name, email, is_active,
        is_staff, is_superuser, last_login, date_joined
    Additional Details
        prefix, middle_name, phone
    """

    DEPARTMENT = (
        ('CSE', 'Computer Science and Engineering'),
        ('ISE', 'Information Science and Engineering'),
        ('ECE', 'Electronics and Communications Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('CIVIL', 'Civil'),
        ('MECH', 'Mechanical')
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
        default="default/user_image.jpeg"
    )
    cover_photo = models.URLField(
        _("Cover Photo"),
        default="default/bg.jpeg"
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
