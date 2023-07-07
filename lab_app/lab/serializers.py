from rest_framework import serializers
from .models import Users, Groups, Experiments, Samples, Tests, Results

class UsersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields='__all__'
  
class GroupsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Groups
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
