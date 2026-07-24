from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import CaseStudy, ScenarioNode, ScenarioEdge, UserCaseProgress
from gamification.services import reward_user_xp

def start_case_study(user, case_study):
    """Initializes user progress for a Case Study starting at the start node."""
    start_node = ScenarioNode.objects.filter(case_study=case_study, is_start_node=True).first()
    if not start_node:
        raise ValidationError("Bu Case Study-da boshlang'ich qadam (start node) belgilanmagan!")
        
    progress, created = UserCaseProgress.objects.update_or_create(
        user=user,
        case_study=case_study,
        defaults={
            'current_node': start_node,
            'score': 0,
            'is_completed': False
        }
    )
    return progress

def submit_case_decision(user, case_study_id, edge_id):
    """Processes user decision by traversing the edge and updating progress/rewards."""
    case_study = get_object_or_404(CaseStudy, id=case_study_id)
    progress = get_object_or_404(UserCaseProgress, user=user, case_study=case_study)
    
    if progress.is_completed:
        raise ValidationError("Ushbu Case Study yakunlangan. Qayta boshlash uchun yangidan urinib ko'ring.")
        
    edge = get_object_or_404(ScenarioEdge, id=edge_id)
    
    # Validate transition
    if edge.from_node != progress.current_node:
        raise ValidationError("Noto'g'ri qadam! Tanlangan variant joriy holatga mos kelmaydi.")
        
    # Advance state
    next_node = edge.to_node
    progress.current_node = next_node
    progress.score += edge.xp_delta
    
    # Award decision XP if positive
    if edge.xp_delta > 0:
        reward_user_xp(user, f"case_decision_{case_study.id}_{edge.id}", edge.xp_delta)
        
    # Check if end/fail node
    if next_node.is_end_node or next_node.is_fail_node:
        progress.is_completed = True
        # If successfully completed (not a fail node), award completion bonus
        if next_node.is_end_node and not next_node.is_fail_node:
            reward_user_xp(user, f"case_complete_{case_study.id}", case_study.xp_reward)
            
    progress.save()
    return progress, edge.feedback_text, edge.xp_delta
