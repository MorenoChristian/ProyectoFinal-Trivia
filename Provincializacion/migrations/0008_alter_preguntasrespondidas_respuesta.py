# Generated by Django 3.2.6 on 2021-09-04 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Provincializacion', '0007_auto_20210904_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntasrespondidas',
            name='respuesta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Provincializacion.elegirrespuesta'),
        ),
    ]