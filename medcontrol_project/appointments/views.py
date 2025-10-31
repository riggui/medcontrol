from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseForbidden
from .models import Document, Athlete, Creneau, RendezVous
from .forms import AthleteForm, ReservationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class DocumentListView(ListView):
    model = Document
    template_name = 'appointments/document_list.html'
    context_object_name = 'documents'

class AthleteListView(ListView):
    model = Athlete
    template_name = 'appointments/athlete_list.html'
    context_object_name = 'athletes'

def _creneau_to_event(c):
    start = f"{c.date.isoformat()}T{c.heure.strftime('%H:%M:%S')}"
    return {
        'id': c.id,
        'title': str(c.medecin),
        'start': start,
        'allDay': False,
    }

def creneaux_json(request):
    creneaux = Creneau.objects.filter(disponible=True)
    events = [_creneau_to_event(c) for c in creneaux]
    return JsonResponse(events, safe=False)

def calendar_view(request):
    return render(request, 'appointments/calendar.html', {'user_authenticated': request.user.is_authenticated})

@login_required
def reserver_creneau(request, creneau_id):
    c = get_object_or_404(Creneau, id=creneau_id)
    if not c.disponible:
        return redirect('appointments:calendar_view')
    equipes = request.user.equipes.all()
    if not equipes.exists():
        return HttpResponseForbidden('Utilisateur sans équipe associée.')
    equipe = equipes.first()
    rdv = RendezVous.objects.create(equipe=equipe, creneau=c, statut='confirme')
    c.disponible = False
    c.save()
    return redirect('appointments:calendar_view')

@login_required
@require_POST
def api_reserver(request, creneau_id):
    c = get_object_or_404(Creneau, id=creneau_id)
    if not c.disponible:
        return JsonResponse({'success': False, 'message': 'Ce créneau est déjà réservé.'}, status=400)
    equipes = request.user.equipes.all()
    if not equipes.exists():
        return JsonResponse({'success': False, 'message': "Vous n'êtes pas lié(e) à une équipe."}, status=403)
    equipe = equipes.first()
    rdv = RendezVous.objects.create(equipe=equipe, creneau=c, statut='confirme')
    c.disponible = False
    c.save()
    return JsonResponse({'success': True, 'message': 'Créneau réservé avec succès.', 'event_id': c.id})
