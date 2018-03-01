from push_notifications.signals import user_was_followed

from .models import Follow


def follow(from_user, to_user):
    user_was_followed.send(follower=from_user, followee=to_user)
    Follow.objects.create(from_user=from_user, to_user=to_user)


def unfollow(from_user, to_user):
    Follow.objects.filter(from_user=from_user, to_user=to_user).delete()