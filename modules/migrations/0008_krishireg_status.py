# Generated by Django 4.0.4 on 2022-06-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0007_remove_krishireg_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='krishireg',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
