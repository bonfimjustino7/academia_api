# meses
JANEIRO = 1
FEVEREIRO = 2
MARCO = 3
ABRIL = 4
MAIO = 5
JUNHO = 6
JULHO = 7
AGOSTO = 8
SETEMBRO = 9
OUTUBRO = 10
NOVEMBRO = 11
DEZEMBRO = 12

MESES = (
    (JANEIRO, 'JANEIRO'),
    (FEVEREIRO, 'FEVEREIRO'),
    (MARCO, 'MARÇO'),
    (ABRIL, 'ABRIL'),
    (MAIO, 'MAIO'),
    (JUNHO, 'JUNHO'),
    (JULHO, 'JULHO'),
    (AGOSTO, 'AGOSTO'),
    (SETEMBRO, 'SETEMBRO'),
    (OUTUBRO, 'OUTUBRO'),
    (NOVEMBRO, 'NOVEMBRO'),
    (DEZEMBRO, 'DEZEMBRO')
)

# status matricula
ATIVA = 'A'
INATIVA = 'I'

STATUS_MATRICULA = (
    (ATIVA, 'ATIVA'),
    (INATIVA, 'INATIVA')
)

# mesalidade
PAGO = 'P'
NAO_PAGO = 'D'
NULA = 'N'

STATUS_MENSALIDADE = (
    ('P', 'PAGO'),
    ('D', 'NÃO PAGO'),
    ('N', 'NULA'),
)

# meios de pagamento
CARTAO_CREDITO = 'CR'
CARTAO_DEBITO = 'CD'
PIX = 'PIX'
BOLETO_BANCARIO = 'BB'
DINHEIRO = 'D'

MEIOS_PAGAMENTO = (
    (CARTAO_CREDITO, 'CARTÃO DE CRÉDITO'),
    (CARTAO_DEBITO, 'CARTÃO DE DÉBITO'),
    (PIX, 'PIX'),
    (BOLETO_BANCARIO, 'BOLETO BANCÁRIO'),
    (DINHEIRO, 'DINHEIRO'),
)

# mensagens de razão para anular mensalidade
ESTORNO = 'ESTORNO'
ERRO_CONTABIL = 'ERRO_CONTABIL'

RAZOES = (
    (ESTORNO, 'A mensalidade foi estornada pelo gerente da academia.'),
    (ERRO_CONTABIL, 'A mensalidade foi nula por erro contabil do gerente.'),
)