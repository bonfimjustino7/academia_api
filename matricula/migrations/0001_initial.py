# Generated by Django 3.2.4 on 2021-07-18 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academia', '0002_academia_user'),
        ('aluno', '0002_aluno_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'ATIVA'), ('I', 'INATIVA')], max_length=2)),
                ('dt_matricula', models.DateTimeField(auto_now_add=True)),
                ('academia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.academia')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aluno.aluno')),
            ],
        ),
    ]
