from django_filters import rest_framework as filters
from .models import Medicao


class MedicaoFilter(filters.FilterSet):
    dt_after = filters.DateFilter(
        field_name="data_criacao", lookup_expr="gte", label="Data inicial"
    )
    dt_before = filters.DateFilter(
        field_name="data_criacao", lookup_expr="lte", label="Data final"
    )
    ordering = filters.OrderingFilter(
        fields=(("data_criacao", "data_criacao"),),
        label="Ordernar por"
    )

    class Meta:
        model = Medicao
        fields = ('dt_after', 'dt_before', 'aluno', 'ordering')
