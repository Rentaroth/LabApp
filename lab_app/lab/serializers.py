from rest_framework import serializers
from rest_framework import status
from .models import Users, Groups, Invitations, Experiments, Samples, Tests, Results

class UsersSerializer(serializers.ModelSerializer):
  username = serializers.CharField(max_length=25)
  email = serializers.EmailField(max_length=85)
  password = serializers.CharField(max_length=255)
  created_at = serializers.DateTimeField()
  updated_at = serializers.DateTimeField()

  class Meta:
    model = Users
    fields='__all__'
  
class GroupsSerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=25)
  lider_id = serializers.IntegerField()
  created_at = serializers.DateTimeField()
  updated_at = serializers.DateTimeField()
  
  class Meta:
    model = Groups
    fields='__all__'

class InvitationsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Invitations
    fields='__all__'

class ExperimentsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Experiments
    fields='__all__'

class SamplesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Samples
    fields='__all__'

class TestsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tests
    fields='__all__'

class ResultsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Results
    fields='__all__'
