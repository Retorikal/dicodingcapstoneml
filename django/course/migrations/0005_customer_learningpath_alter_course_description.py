# Generated by Django 4.0.4 on 2022-05-29 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_course_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='learningpath',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
