from django.contrib import admin
from .models import User, Equipe, Athlete, Medecin, Creneau, RendezVous, Document
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rôle', {'fields': ('role',)}),
    )

admin.site.register(Equipe)
admin.site.register(Athlete)
admin.site.register(Medecin)
admin.site.register(Creneau)
admin.site.register(RendezVous)
admin.site.register(Document)
