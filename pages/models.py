from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class minipage(models.Model):
		
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.TextField()
	image = models.TextField()
	content = models.TextField()
	
	class Meta:
		db_table = 'minipage'
    
    