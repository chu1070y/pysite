from django.db import models


# Create your models here.

class Guestbook(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    content = models.CharField(max_length=1000)
    regdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User({self.name}, {self.content}, {self.regdate})'
