from django.contrib import admin

from matricula.models import Matricula, Mensalidade


class MensalidadeAdmin(admin.TabularInline):
    model = Mensalidade
    fields = ('ano', 'mes_referente', 'status', 'dt_vencimento')
    # can_delete = False
    extra = 0
    readonly_fields = ('ano', 'mes_referente', 'dt_vencimento')

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj):
        return False


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dt_matricula')
    inlines = [MensalidadeAdmin]
