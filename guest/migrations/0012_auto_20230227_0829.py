# Generated by Django 3.2.4 on 2023-02-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0011_order_establishment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_login',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='establishment',
            name='image',
            field=models.FileField(upload_to='guest/static/guest/images'),
        ),
        migrations.AlterField(
            model_name='plate',
            name='image',
            field=models.FileField(upload_to='guest/static/guest/images'),
        ),
    ]