from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"New user created with username: {instance.username}")
    else:
        print(f"User with username: {instance.username} was updated!")


post_save.connect(post_user_created_signal, sender=User)


def make_email_lowercase(sender, instance, **kwargs):
    print("at the pre save receiver")
    instance.email = instance.email.lower()


pre_save.connect(make_email_lowercase, sender=User)

