from django.db import models


class Court(models.Model):
    name = models.TextField(unique=True)
    name_short = models.TextField(unique=True)
    web_adress = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Decision(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    file_number = models.TextField(unique=True)
    file_name = models.TextField()
    file_type = models.TextField()
    file_theme = models.TextField()
    file = models.TextField()
    date_pron = models.DateField()
    date_created = models.DateField()
    date_published = models.DateField()
