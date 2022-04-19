# Generated by Django 4.0.1 on 2022-01-26 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_tag_slug'),
        ('course', '0003_remove_course_tag_remove_course_user_course_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='courses', to='cms.Tag'),
        ),
    ]
