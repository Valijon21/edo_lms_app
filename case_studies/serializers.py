from rest_framework import serializers
from .models import CaseStudy, ScenarioNode, ScenarioEdge, UserCaseProgress

class CaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = ('id', 'title', 'description', 'xp_reward', 'is_active', 'created_at')

class ScenarioEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioEdge
        fields = ('id', 'option_text')

class ScenarioNodeSerializer(serializers.ModelSerializer):
    options = ScenarioEdgeSerializer(source='edges', many=True, read_only=True)
    
    class Meta:
        model = ScenarioNode
        fields = ('id', 'title', 'content', 'is_start_node', 'is_end_node', 'is_fail_node', 'options')

class UserCaseProgressSerializer(serializers.ModelSerializer):
    current_node = ScenarioNodeSerializer(read_only=True)
    
    class Meta:
        model = UserCaseProgress
        fields = ('id', 'case_study', 'current_node', 'score', 'is_completed')
