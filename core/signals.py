from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from urllib import request
from os import path
from django.dispatch import receiver
from allauth import account
from .models import Profile
from PIL import Image


# @receiver(user_signed_up)
# def social_login_fname_lname_profilepic(sociallogin, user):
#     preferred_avatar_size_pixels = 256

#     picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
#         hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
#         preferred_avatar_size_pixels
#     )

#     if sociallogin:
#         # Extract first / last names from social nets and store on User record
#         # if sociallogin.account.provider == 'twitter':
#         #     name = sociallogin.account.extra_data['name']
#         #     user.first_name = name.split()[0]
#         #     user.last_name = name.split()[1]

#         # if sociallogin.account.provider == 'facebook':
#         #     f_name = sociallogin.account.extra_data['first_name']
#         #     l_name = sociallogin.account.extra_data['last_name']
#         #     if f_name:
#         #         user.first_name = f_name
#         #     if l_name:
#         #         user.last_name = l_name

#         #     #verified = sociallogin.account.extra_data['verified']
#         #     picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
#         #         sociallogin.account.uid, preferred_avatar_size_pixels)

#         if sociallogin.account.provider == 'google':
#             # f_name = sociallogin.account.extra_data['given_name']
#             # l_name = sociallogin.account.extra_data['family_name']
#             # if f_name:
#             #     user.first_name = f_name
#             # if l_name:
#             #     user.last_name = l_name
#             #verified = sociallogin.account.extra_data['verified_email']
#             picture_url = sociallogin.account.extra_data['picture']

#     user.save()
#     profile = Profile(user=user, profile=picture_url)
#     profile.save()

# @receiver(social_account_added)
# def social_account_added(request, social_login, **kwargs):
#     pass

@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):

    # profile = Profile.objects.get(user=user)

    if sociallogin.account.provider == 'facebook':
        user_data = user.socialaccount_set.filter(
            provider='facebook')[0].extra_data
        picture_url = "http://graph.facebook.com/" + \
            sociallogin.account.uid + "/picture?type=large"
        email = user_data['email']
        full_name = user_data['name']

    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(
            provider='google')[0].extra_data
        picture_url = user_data['picture']
        email = user_data['email']
        full_name = user_data['name']
    # user.profile.profile_img = picture_url
    profile = request.urlretrieve(
        picture_url, f'{settings.BASE_DIR}\\media\\profile\\{email.split("@")[0]}.jpg')
    p = Profile.objects.create(user=user, profile=profile[0])
    p.save()




@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not account.signals.user_logged_in:
        if created:
            Profile.objects.create(user=instance)
    else:
        if created:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if not account.signals.user_logged_in:
        instance.profile_img.save()
    else:
        instance.profile_img.save()
