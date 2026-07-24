import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import SimulationScenario, SimulationSession
from .services import process_simulator_action


@login_required
def simulator_list(request):
    """Barcha faol simulyatsiya ssenariylari ro'yxati."""
    scenarios = SimulationScenario.objects.filter(is_active=True)
    
    # Foydalanuvchi sessiyalarini dict shaklida olish
    user_sessions = {
        s.scenario_id: s
        for s in SimulationSession.objects.filter(user=request.user)
    }

    scenarios_data = []
    for sc in scenarios:
        session = user_sessions.get(sc.id)
        scenarios_data.append({
            'scenario': sc,
            'session': session,
            'is_completed': session.is_completed if session else False,
            'current_step': session.current_step_index if session else 0,
            'total_steps': len(sc.expected_steps),
        })

    return render(request, "simulator/list.html", {
        "scenarios_data": scenarios_data
    })


@login_required
def simulator_detail(request, pk):
    """Virtual Edo.ijro.uz interaktiv simulyator sahifasi."""
    scenario = get_object_or_404(SimulationScenario, pk=pk, is_active=True)
    session, _ = SimulationSession.objects.get_or_create(
        user=request.user,
        scenario=scenario
    )

    steps = scenario.expected_steps
    curr_idx = session.current_step_index
    current_step_info = steps[curr_idx] if curr_idx < len(steps) else None

    return render(request, "simulator/sandbox.html", {
        "scenario": scenario,
        "session": session,
        "current_step_info": current_step_info,
        "steps_json": json.dumps(steps),
        "initial_doc_json": json.dumps(scenario.initial_doc_data),
    })


@login_required
@require_POST
def simulator_action_api(request, pk):
    """Foydalanuvchi harakatlarini tekshiruvchi REST API endpoint."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Noto'g'ri JSON formati."}, status=400)

    action_type = data.get("action_type")
    payload = data.get("payload", {})

    if not action_type:
        return JsonResponse({"success": False, "message": "Harakat turi (action_type) kiritilmadi."}, status=400)

    result = process_simulator_action(
        user=request.user,
        scenario_id=pk,
        action_type=action_type,
        payload=payload
    )

    return JsonResponse(result)


@login_required
@require_POST
def simulator_reset(request, pk):
    """Ssenariy sessiyasini qayta boshlash."""
    scenario = get_object_or_404(SimulationScenario, pk=pk)
    SimulationSession.objects.filter(user=request.user, scenario=scenario).delete()
    return redirect("simulator:detail", pk=pk)
