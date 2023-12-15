from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserProfile


# This decorator is used to register a function as a signal handler. When you decorate a function with @receiver,
# you're telling Django: "Call this function when the specified signal is sent."
# The post_save signal is sent by Django after a model's save method is called.
# This is true for both creating a new record and updating an existing one.


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# def save_user_profile(sender, instance, **kwargs): This function is triggered after a User instance is saved.
# instance.profile.save(): This line saves the UserProfile instance related to the User instance.
# The profile here is assumed to be the related name of the UserProfile instance that is connected to the User instance.
