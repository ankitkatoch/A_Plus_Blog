from django.db import models
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
# Create your models here.
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from hitcount.models import HitCountMixin, HitCount
import readtime
from django.contrib.contenttypes.fields import GenericRelation


def upload_location(instance, filename):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(author_id=str(instance.author.id), title=str(instance.title), filename=filename)
    return file_path


class BlogModel(models.Model):
    title = models.CharField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    blog_image = models.ImageField(upload_to=upload_location)
    tags = TaggableManager()
    description = HTMLField()
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ('-created_on',)

    def get_readtime(self):
        result = readtime.of_text(self.description)
        return result.text

    def __str__(self):
        return self.title


class CommentModel(models.Model):
    post = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()


@receiver(post_delete, sender=BlogModel)
def submission_delete(sender, instance, **kwargs):
    instance.blog_image.delete(False)


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiver, sender=BlogModel)
