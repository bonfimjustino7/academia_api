from django_filters import rest_framework as filters

from matricula.constants import STATUS_MENSALIDADE
from matricula.models import Mensalidade


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