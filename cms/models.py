from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver

# get the MEDIA_ROOT from settings.py
MEDIA_URL = settings.MEDIA_URL
STATIC_URL = settings.STATIC_URL


### Models
class Page(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    published = models.BooleanField(default=False)
    slug = models.CharField(max_length=50, blank=True, unique=True) # Use CharField instead of SlugField to allow non ascii characters
    parent_page = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_pages', null=True, blank=True)

    created_at = models.DateTimeField(default=now)
    modified_at = models.DateTimeField(default=now)
    def __str__(self):
        return self.title

class ArticleCategory(models.Model):
    name = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='articlecategory/', null=True, blank=True)
    description = models.TextField(blank=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)
    articles = models.ManyToManyField('Article', related_name='categories', blank=True)
    def __str__(self):
        return self.name
    def get_cover_image_url(self):
        return f"{MEDIA_URL}{self.cover_image}"
    
    class Meta:
        verbose_name_plural = "Article Categories"
    
class Article(models.Model):
    title = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='Article/', null=True, blank=True)
    summary = models.CharField(max_length=200, blank=True)
    content = models.TextField()

    reference_url = models.CharField(max_length=200, blank=True)
    youtube_video_id = models.CharField(max_length=100, blank=True)
    
    slug = models.CharField(max_length=50, blank=True, unique=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    modified_at = models.DateTimeField(default=now)
    
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    def get_cover_image_url(self):
        return f"{MEDIA_URL}{self.cover_image}"

    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    articles = models.ManyToManyField(Article, related_name='tags', through='ArticleTag', blank=True)
    def __str__(self):
        return self.name

    
class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('article', 'tag')


class Album(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, blank=True, unique=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='album/', null=True, blank=True)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    def get_cover_image_url(self):
        return f"{MEDIA_URL}{self.cover_image}"

class Image(models.Model):
    image = models.ImageField(upload_to='image/')
    caption = models.CharField(max_length=200)
    published = models.BooleanField(default=False)
    articles = models.ManyToManyField(Article, related_name='images', through='ArticleImage', blank=True)
    pages = models.ManyToManyField(Page, related_name='images', through='PageImage', blank=True)
    def __str__(self):
        return f"{self.image} {self.caption}"
    def get_image_url(self):
        return f"{MEDIA_URL}{self.image}"
    def image_tag(self):
        if (self.image == None or self.image == ""):
            return mark_safe(f"<img src=\"{STATIC_URL}images/no_image.png\" width=\"150\" height=\"150\" />")
        return mark_safe(f"<img src=\"{MEDIA_URL}{self.image}\" style=\"max-width: 150px; max-height: 150px\" />")
    image_tag.allow_tags = True
    image_tag.short_description = 'Image Preview'
    def get_absolute_url(self):
        return f"{MEDIA_URL}{self.image}"
    
# Extend from Image(Treat it like a sub type of Image)
class AlbumImage(models.Model):
    image = models.OneToOneField(Image, on_delete=models.CASCADE, primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_images')
    display_order = models.IntegerField(default=0)
    class Meta:
        unique_together = ('image', 'album')
        ordering = ['display_order']

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    display_order = models.IntegerField(default=0)
    def image_tag(self):
        return mark_safe(f"<img src=\"{MEDIA_URL}{self.image.image}\" width=\"150\" height=\"150\" />")
    image_tag.allow_tags = True
    class Meta:
        unique_together = ('article', 'image')

class PageImage(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    display_order = models.IntegerField(default=0)
    def image_tag(self):
        return mark_safe(f"<img src=\"{MEDIA_URL}{self.image.image}\" width=\"150\" height=\"150\" />")
    image_tag.allow_tags = True

    class Meta:
        unique_together = ('page', 'image')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, blank=False, unique=True)
    title = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def get_image_url(self):
        return f"{MEDIA_URL}{self.avatar}"
    def image_tag(self):
        if (self.avatar == None or self.avatar == ""):
            return mark_safe(f"<img src=\"{STATIC_URL}images/no_image.png\" width=\"150\" height=\"150\" />")
        return mark_safe(f"<img src=\"{MEDIA_URL}{self.avatar}\" style=\"max-width: 150px; max-height: 150px\" />")    
    image_tag.allow_tags = True


### Create a Profile when a User is created, using signal
@receiver(post_save, weak=False, sender = settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    print("create_user_profile")
    if created:
        try:
            # seee if the profile object exists
            # profile object can exists, if user is creatred from admin panel and form is valid
            # At this case, the profile is actually created automatically by the admin panel
            profile = instance.profile
        except Profile.DoesNotExist as e:
            # if not, create one manually
            # that can be the case when user is created in manager.py, or user types onthing in the admin panel
            instance.profile = Profile.objects.create(user=instance, nickname=instance.username)
            instance.save()



