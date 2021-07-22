from auth_api.managers import UserManager


class AlunoManagers(UserManager):
    def create_user(self, **fields):
        from matricula.models import Matricula
        academia = fields.pop('academia')
        aluno = super(AlunoManagers, self).create_user(**fields)

        Matricula.objects.get_or_create(aluno=aluno, academia=academia)

        return aluno
