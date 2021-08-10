from django.db.models import Q
from django_filters import rest_framework as filters

from matricula.constants import STATUS_MENSALIDADE, STATUS_MATRICULA
from matricula.models import Mensalidade, Matricula


class MatriculaFilters(filters.FilterSet):
    status = filters.ChoiceFilter(
        field_name='status',
        choices=STATUS_MATRICULA,
        lookup_expr="iexact",
        label="Status",
    )
    search = filters.CharFilter(
        method='search_method',
        label='search'
    )

    def search_method(self, queryset, name, value):
        return queryset.filter(
            Q(aluno__user__username__icontains=value) | Q(id__iexact=value)
        )

    class Meta:
        model = Matricula
        fields = ('status', 'search')


class MensalidadeFilters(filters.FilterSet):
    status = filters.ChoiceFilter(
        field_name='status',
        choices=STATUS_MENSALIDADE,
        lookup_expr="iexact",
        label="Status",
    )
    dt_vencimento_after = filters.DateFilter(
        field_name="dt_vencimento", lookup_expr="gte", label="Data de vencimento inicial"
    )
    dt_vencimento_before = filters.DateFilter(
        field_name="dt_vencimento", lookup_expr="lte", label="Data de vencimento final"
    )

    ordernar_por = filters.OrderingFilter(
        fields=(("dt_vencimento", "dt_vencimento"), ),
        label="Ordernar por"
    )

    class Meta:
        model = Mensalidade
        fields = ('status', 'dt_vencimento_after', 'dt_vencimento_before', 'ordernar_por',)