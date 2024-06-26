# Generated by Django 4.1.8 on 2023-05-06 10:14

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('blog', '0023_linkpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloglistingpage',
            name='featured_articles',
            field=wagtail.fields.StreamField([('featured_article', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('image', wagtail.blocks.StructBlock([('image', wagtail.blocks.PageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False))], required=True)), ('content', wagtail.blocks.RichTextBlock(required=True))], icon='doc-full-inverse'))], blank=True, use_json_field=None),
        ),
        migrations.CreateModel(
            name='FeaturedArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
        ),
    ]
