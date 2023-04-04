from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django_countries.fields import CountryField


class BlogPost(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, null=False)
    subtitle = models.CharField(max_length=250, null=False)
    date = models.DateField(auto_now_add=True)
    body = RichTextUploadingField()
    pic = models.ImageField(default='default.jpg', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blog_post"
        verbose_name_plural = 'blog_posts'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    body = RichTextUploadingField()
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.body[0:10]

    class Meta:
        db_table = "comment"
        ordering = ["date"]
        verbose_name_plural = 'comments'


class LogBook(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dive_number = models.PositiveIntegerField()
    date = models.DateField(auto_now=False)
    time = models.TimeField(auto_now=False)
    country = CountryField(blank=True)
    dive_site = models.CharField(max_length=30)
    guide = models.CharField(max_length=30, blank=True)
    buddy = models.CharField(max_length=30, blank=True)
    dive_center = models.CharField(max_length=100, default='https://www.padi.com/dive-shops/nearby/?lang=en')
    duration = models.DurationField()
    depth = models.FloatField()
    nitrox = models.BooleanField(null=True)
    air_left = models.IntegerField()
    notes = models.TextField(max_length=200, blank=True)
    log_date = models.DateField(auto_now_add=True)
    pics = models.FileField(blank=True)

    def __str__(self):
        return f'{self.date}, {self.dive_site}'

    class Meta:
        ordering = ["dive_number"]
