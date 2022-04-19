from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from account.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# @receiver(m2m_changed, sender=Image.users_like.through)     here we have Image model with total_likes and user_likes as fields
# def users_like_changed(sender, instance, **kwargs):
#      instance.total_likes = instance.users_like.count()
#      instance.save()
