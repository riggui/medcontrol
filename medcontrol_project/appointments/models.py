from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ('admin', 'Administrateur'),
    ('medecin', 'Médecin'),
    ('equipe', 'Équipe'),
)

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='equipe')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Equipe(models.Model):
    nom = models.CharField(max_length=150)
    sport = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    responsable = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='equipes')

    def __str__(self):
        return self.nom

class Athlete(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='athletes')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    numero_identite = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Medecin(models.Model):
    nom = models.CharField(max_length=150)
    specialite = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.nom

class Creneau(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='creneaux')
    date = models.DateField()
    heure = models.TimeField()
    disponible = models.BooleanField(default=True)

    class Meta:
        unique_together = ('medecin', 'date', 'heure')
        ordering = ['date', 'heure']

    def __str__(self):
        return f"{self.date} {self.heure} - {self.medecin}"

STATUS_CHOICES = (
    ('reserve', 'Réservé'),
    ('confirme', 'Confirmé'),
    ('annule', 'Annulé'),
)

class RendezVous(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='rendezvous')
    creneau = models.ForeignKey(Creneau, on_delete=models.CASCADE, related_name='rendezvous')
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserve')
    date_reservation = models.DateTimeField(auto_now_add=True)
    athletes = models.ManyToManyField(Athlete, blank=True)

    def __str__(self):
        return f"RDV {self.equipe} - {self.creneau} ({self.get_statut_display()})"

class Document(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to='documents/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
