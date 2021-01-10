from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.utils.text import slugify
from django_editorjs import EditorJsField
from allauth import socialaccount
from taggit.managers import TaggableManager
# socialaccount.providers.google.provider.OAuth2Provider.extract_extra_data
# Create your models here.


# class PersonManager(models.Manager):
#     def get_by_natural_key(self, title):
#         return self.get(title=title)
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=True)
    body = EditorJsField(editorjs_config={
        "tools": {
            "config": {
                "placeholder": 'Write your post content here...'
            },
            "Image": {
                "config": {
                    "endpoints": {
                        "byFile": '/imageUPload/',
                        "byUrl": '/imageUPload/'
                    },
                    "additionalRequestHeaders": [{"Content-Type": 'multipart/form-data'}]
                }
            },
            "Attaches": {
                "config": {
                    "endpoint": '/fileUPload/',
                },
            },
        }
    }, blank=True)
    slug = models.SlugField()
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    header = models.ImageField(upload_to='uploads', blank=True)
    snippet = models.CharField(max_length=250, blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    draft = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    # objects = PersonManager()

    def natural_key(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.slug = slugify(self.title)
        self.modified = timezone.now()

        # img = Image.open(self.header.path)
        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)

        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.slug])

    class Meta:
        ordering = ['-created']
        unique_together = ['title']


class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, related_name="post_read")

    def __str__(self):
        return f'{self.user} reading list'


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,  related_name='profile_img')
    profile = models.ImageField('Profile_image',
                                default='/profile/default.jpg', upload_to='profile')
    bio = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=250, blank=True)
    following = models.ManyToManyField(
        User, related_name='profile_following', blank=True)
    follower = models.ManyToManyField(
        User, related_name='profile_follower', blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile.path)
        if img.height > 96 or img.width > 96:
            output_size = (96, 96)
            img.thumbnail(output_size)
            img.save(self.profile.path)


class Comment(models.Model):
    comment = models.CharField(max_length=500)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comment_post")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user")
    created = models.DateTimeField()

    # def save(self, *args, **kwargs):
    #     super().save()
    #     if not self.id:
    #         self.created = timezone.now()
    #     self.created = timezone.now()

    def __str__(self):
        return f'{self.user.username} comment'
