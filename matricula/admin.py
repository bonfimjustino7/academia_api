from django.contrib import admin
from matricula.models import Matricula, Mensalidade


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dt_matricula')


@admin.register(Mensalidade)
class MensalidadeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'mes_referente', 'status')