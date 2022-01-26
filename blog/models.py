from email.mime import text
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ) 
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    # avatar = models.ImageField(_("avatar"), upload_to='profile')
    # banner = models.ImageField(_('banner'), upload_to='banner')
    bio = models.TextField(_("bio"))
    gender = models.CharField(_("gender"), max_length=20, choices=GENDER_CHOICES)
    address = models.CharField(_("address"), max_length=150)
    
    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Publish', 'Publish'),
    ) 
    user = models.ForeignKey(Profile, verbose_name=_("user"), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), unique=True, blank=True)
    # thumnail = models.ImageField(_("thumnail"), upload_to='post')
    description = models.TextField(_("description"))
    status  = models.CharField(_("status"), max_length=20, choices=STATUS_CHOICES, default='Draft')
    view_count = models.IntegerField(_("view count"), default=0)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    class Meta:
        ordering = ['-pk']
    
    @property
    def comment_counter(self):
        return self.comments.all().count()
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(Profile, verbose_name=_("user"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(_("comment text"))
    created_at = models.DateTimeField(_("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, auto_now_add=False)
    
    class Meta:
        ordering = ['-pk']


class Contact(models.Model):
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    subject = models.CharField(_("subject"), max_length=50)
    email = models.EmailField(_("email"), max_length=254)
    detail = models.TextField(_("detail"))
    
    def __str__(self):
        return f'{self.first_name}-{self.last_name}'


def create_profile_signal(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_profile_signal, sender=User)

