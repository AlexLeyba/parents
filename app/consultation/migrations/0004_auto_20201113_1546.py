# Generated by Django 3.1.3 on 2020-11-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0003_auto_20201026_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Район'),
        ),
        migrations.DeleteModel(
            name='District',
        ),
    ]
