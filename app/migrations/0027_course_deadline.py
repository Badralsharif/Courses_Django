# Generated by Django 4.0.6 on 2022-11-30 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_remove_course_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Deadline',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
