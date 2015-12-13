from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
	"""Custom user class"""

	username = models.CharField('username', max_length=10, unique=True, db_index=True)
	email = models.EmailField('email_adress', unique=True)
	joined = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	
	USERNAME_FIELD = 'username'
	def __unicode__(self):
		return self.username
