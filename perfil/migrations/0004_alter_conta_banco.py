# Generated by Django 4.2.3 on 2023-07-08 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0003_rename_esencial_categoria_essencial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='banco',
            field=models.CharField(choices=[('NU', 'Nubank'), ('CE', 'Caixa economica'), ('BB', 'Banco do brasil'), ('IN', 'Inter'), ('SA', 'Santander')], max_length=2),
        ),
    ]
