# Generated by Django 2.1 on 2019-03-28 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_receitasguardadas'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientes',
            name='unidade',
            field=models.CharField(default='chavena', max_length=50),
            preserve_default=False,
        ),
    ]
