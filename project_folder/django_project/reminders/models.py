from django.db import models

# Create your models here.

class Tag(models.Model):
    # PK id created by default id (bigint), you may override that with th e
    # following line
    # id = models.SmallIntegerField(auto_increment=True, primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
    		return self.name

class Reminder(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    homework = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField()

    class Meta:
        ordering = ['date']
        
        
