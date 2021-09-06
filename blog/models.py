from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import reverse, redirect

from ckeditor.fields import RichTextField

from PIL import Image

from MyBlog.util import unique_slug_generator


class BlogModel(models.Model):

    LANGUAGES_CHOICES = (
        ('Eng', 'English'),
        ('Hin', 'Hindi'),
    )

    blog_title = models.CharField( max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    blog_short_desc = models.CharField(max_length=1000, blank=False, null=False)
    blog_author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted_on = models.DateTimeField(auto_now_add=True)
    blog_image = models.ImageField(upload_to='blog_pics', blank=False, null=False,)
    blog_complete_desc = RichTextField(blank=False, null=False)
    blog_language = models.CharField(max_length=3, choices=LANGUAGES_CHOICES)

    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def __str__(self):
        return self.blog_title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def save(self):
        super().save()

        img = Image.open(self.blog_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.blog_image.path)


@receiver(pre_save, sender=BlogModel)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class CommentModel(models.Model):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated_on = models.DateTimeField(auto_now_add=True)
    comment = RichTextField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return f'{self.comment} - {self.comment_author}'


class AddBlogModel(models.Model):
    blog    = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=1000, blank=False, null=False)
    image   = models.ImageField(upload_to='blog_pics', null=True, blank=True,)
    body    = RichTextField(null=False, blank=False)

    def __str__(self):
        return f'{self.title} - {self.blog}'

    def get_absolute_url(self):
        return redirect(f'/blog/{self.blog.id}')

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# class LikesModel(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
#     like = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.like}/{self.blog} - {self.user}'