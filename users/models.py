from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.


# auto_now:
#
# Usage: This option is generally used for fields that need to record the timestamp of the last time an object was
# modified. Behavior: Whenever you save the object, Django will automatically set the field to the current date and
# time. Typical Use Case: A last_modified field in a model that needs to record the timestamp of the last update.
# Example: last_modified = models.DateTimeField(auto_now=True)

# auto_now_add:
#
# Usage: This is used for fields that should record the timestamp when an object was created. Behavior: The field is
# automatically set to the current date and time when the object is first created. It is not updated on subsequent
# saves. Typical Use Case: A created_at field in a model that records when a record was initially created. Example:
# created_at = models.DateTimeField(auto_now_add=True)

# **
# In the UserProfile model, get_user_model() is used to refer to the custom user model.
# This is a best practice to ensure compatibility with the custom user model defined in your Django settings.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    blank=True, unique=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')  # **
    bio = models.TextField(_("Biography"), blank=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='profile_pics/', blank=True, null=True)
    birth_date = models.DateField(_("Birth Date"), blank=True, null=True)
    location = models.CharField(_("Location"), max_length=100, blank=True)

    def __str__(self):
        return self.user.username
