from django import forms
from .models import Athlete, RendezVous

class AthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = ['equipe','nom','prenom','date_naissance','numero_identite','telephone']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['equipe','creneau','athletes']
        widgets = {'athletes': forms.CheckboxSelectMultiple}
