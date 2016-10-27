from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _

# Create your models here.

class ResultModel(models.Model):
	mots_cles = models.CharField(max_length=200)
	