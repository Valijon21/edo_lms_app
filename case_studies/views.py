from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CaseStudy, UserCaseProgress
from .serializers import CaseStudySerializer, ScenarioNodeSerializer, UserCaseProgressSerializer
from .services import start_case_study, submit_case_decision

class CaseStudyListView(LoginRequiredMixin, ListView):
    """Frontend view for case studies list"""
    model = CaseStudy
    template_name = "case_studies/case_list.html"
    context_object_name = "cases"
    
    def get_queryset(self):
        return CaseStudy.objects.filter(is_active=True)

class CaseStudyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CaseStudy.objects.filter(is_active=True)
    serializer_class = CaseStudySerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        case_study = self.get_object()
        try:
            progress = start_case_study(request.user, case_study)
            serializer = UserCaseProgressSerializer(progress)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def choose(self, request, pk=None):
        case_study = self.get_object()
        edge_id = request.data.get('edge_id')
        if not edge_id:
            return Response({"error": "edge_id talab qilinadi."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            progress, feedback_text, xp_delta = submit_case_decision(request.user, case_study.id, edge_id)
            node_serializer = ScenarioNodeSerializer(progress.current_node)
            return Response({
                "status": "success",
                "earned_xp": xp_delta,
                "feedback": feedback_text,
                "next_node": node_serializer.data,
                "is_completed": progress.is_completed,
                "total_score": progress.score
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
