from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Category(models.Model):
	name = models.CharField(max_length=100,
							unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	

	def __str__(self):
		return self.name


class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=120)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __str__(self):
		#pass
		return self.title


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)

	def __str__(self):
		return self.user.username




