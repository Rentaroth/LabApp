from django.db import models
from django.utils import timezone

class Users(models.Model):
  username = models.CharField(max_length=25, unique=True)
  email = models.CharField(max_length=85, unique=True)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.username}'

class Groups(models.Model):
  name = models.CharField(max_length=25,unique=True)
  lider_id = models.IntegerField()
  users_id = models.ManyToManyField(to=Users, null=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.name}'

class Invitations(models.Model):
  _from = models.IntegerField()
  _to = models.ForeignKey(to=Users, on_delete=models.CASCADE)
  token = models.TextField()
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.token}'

class Experiments(models.Model):
  name = models.CharField(max_length=25, unique=True)
  description = models.TextField(max_length=800)
  group_id = models.ForeignKey(to=Groups, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.name}'

class Samples(models.Model):
  name = models.CharField(max_length=25, unique=True)
  type = models.CharField(max_length=50)
  description = models.TextField(max_length=800)
  experiment_id = models.ForeignKey(to=Experiments, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.name}'

class Tests(models.Model):
  name = models.CharField(max_length=25, unique=True)
  sample_id = models.ForeignKey(to=Samples, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.name}'

class Results(models.Model):
  value = models.CharField(max_length=255)
  test_id = models.ForeignKey(to=Tests, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.name}'