# Generated by Django 3.2.12 on 2022-07-10 05:32

from django.db import migrations
import mirage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogdetailpage_header_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogdetailpage',
            name='intro',
            field=mirage.fields.EncryptedCharField(max_length=255),
        ),
    ]
