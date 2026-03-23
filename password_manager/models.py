from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class SavedPassword(models.Model):
    text = models.CharField(max_length=200)
    note = models.CharField(max_length=200)

    def __str__(self):
        return self.note
