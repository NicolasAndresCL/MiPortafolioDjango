from rest_framework import serializers
from .models import Project, Skill, Experience, ExperienceHighlight

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__' # O especifica ['id', 'title', 'description', ...]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class ExperienceHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceHighlight
        fields = '__all__'  # experience (FK id), text, order

class ExperienceSerializer(serializers.ModelSerializer):
    highlights = ExperienceHighlightSerializer(many=True, read_only=True)
    is_current = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company', 'role', 'location', 'start_date', 'end_date',
                  'is_current', 'summary', 'technologies', 'created_at', 'highlights']