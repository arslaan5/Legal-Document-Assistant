# Generated by Django 5.1.3 on 2024-12-01 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0002_userinfo_groups_userinfo_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]