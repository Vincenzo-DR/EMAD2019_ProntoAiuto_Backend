# Generated by Django 3.0.2 on 2020-02-04 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vetture_service', '0008_auto_20200130_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='vettura',
            name='forza_ordine',
            field=models.CharField(choices=[('Polizia', 'Polizia'), ('Carabinieri', 'Carabinieri'), ('Paramedici', 'Paramedici'), ('Pompieri', 'Pompieri')], max_length=100, null=True),
        ),
    ]
