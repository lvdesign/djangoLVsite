from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

# Create your models here.

#custom manager
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')
	
	
	
	
class Post(models.Model):
	STATUS_CHOICES= (
		('draft', 'Draft'),
		('published', 'Published'),
		)
	author = models.ForeignKey(User, related_name='blog_posts')
	
	title=models.CharField(max_length=250)
	slug=models.SlugField(max_length=250, unique_for_date='publish')
	body=models.TextField()
	image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
	
	publish=models.DateTimeField(default=timezone.now)
	created =models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')
	
	class Meta:
		ordering=('-publish',)
	
	def __str__(self):
		return self.title
	
	
	#
	objects = models.Manager()
	published = PublishedManager()
	#
	tags = TaggableManager()
	
	def get_absolute_url(self):
		return reverse('blog:post_detail',args=[self.publish.year,
												self.publish.strftime('%m'),
												self.publish.strftime('%d'),
												self.slug])