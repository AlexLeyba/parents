# Generated by Django 3.1.3 on 2020-11-24 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alphabet', '0011_article_step_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='number',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='поредковый номер шага'),
        ),
        migrations.AlterField(
            model_name='steptag',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_tags', to='alphabet.step', verbose_name='Шаг'),
        ),
    ]
