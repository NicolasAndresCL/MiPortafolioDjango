from rest_framework import serializers
from .models import Project, Skill

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__' # O especifica ['id', 'title', 'description', ...]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'