# Generated by Django 4.0.4 on 2022-06-05 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_remove_customer_profile_cv_customer_user_cv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user_cv',
        ),
    ]
