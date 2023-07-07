from django.db import models
from django.utils import timezone

class Users(models.Model):
  username = models.CharField(max_length=25)
  email = models.CharField(max_length=85)
  password = models.CharField(max_length=255)
  created_at = models.TimeField(default=timezone.now)
  updated_at = models.TimeField(default=timezone.now)

  def __str__(self):
    return f'{self.username}'

class Groups(models.Model):
  name = models.CharField(max_length=25)
  lider_id = models.IntegerField()
  users_id = models.ManyToManyField(to=Users, auto_created=True)
  created_at = models.TimeField(default=timezone.now)
  updated_at = models.TimeField(default=timezone.now)

  def __str__(self):
    return f'{self.name}'

class Experiments(models.Model):
  name = models.CharField(max_length=25)
  description = models.TextField(max_length=800)
  group_id = models.ForeignKey(to=Groups, on_delete=models.CASCADE)
  created_at = models.TimeField(default=timezone.now)
  updated_at = models.TimeField(default=timezone.now)

  def __str__(self):
    return f'{self.username}'

class Samples(models.Model):
  name = models.CharField(max_length=25)
  type = models.CharField(max_length=50)
  description = models.TextField(max_length=800)
  experiment_id = models.ForeignKey(to=Experiments, on_delete=models.CASCADE)
  created_at = models.TimeField(default=timezone.now)
  updated_at = models.TimeField(default=timezone.now)

  def __str__(self):
    return f'{self.username}'

class Tests(models.Model):
  name = models.CharField(max_length=25)
  sample_id = models.ForeignKey(to=Samples, on_delete=models.CASCADE)
  created_at = models.TimeField(default=timezone.now)
  updated_at = models.TimeField(default=timezone.now)

  def __str__(self):
    return f'{self.username}'

class Results(models.Model):
  value = models.CharField(max_length=255)
  test_id = models.ForeignKey(to=Tests, on_delete=models.CASCADE)
  created_at = models.TimeField(default=timezone.now)
  updated_at = models.TimeField(default=timezone.now)

  def __str__(self):
    return f'{self.username}'