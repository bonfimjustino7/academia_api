from django.contrib import admin
from core.models import Academia, TokenAcademia


@admin.register(Academia)
class AcademiaAdmin(admin.ModelAdmin):
    pass

@admin.register(TokenAcademia)
class TokenAcademia(admin.ModelAdmin):
    pass