# Generated by Django 4.0.1 on 2022-01-24 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(db_index=True, default=None, editable=False, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('main_mage', models.ImageField(blank=True, null=True, upload_to='')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('is_free', models.BooleanField(default=False)),
                ('has_discount', models.BooleanField(default=False)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('pre_sale', models.BooleanField(default=False)),
                ('published_date', models.DateTimeField(null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='categories.category')),
                ('tag', models.ManyToManyField(related_name='tags', to='cms.Tag')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructed_courses', to=settings.AUTH_USER_MODEL)),
                ('user', models.ManyToManyField(null=True, related_name='bought_courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='CourseEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(db_index=True, default=None, editable=False, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=500)),
                ('video', models.FileField(upload_to='')),
                ('video_poster', models.ImageField(blank=True, null=True, upload_to='')),
                ('duration', models.DurationField()),
                ('is_free', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='course.course')),
            ],
            options={
                'verbose_name': 'course Episode',
                'verbose_name_plural': 'course Episodes',
                'ordering': ['number'],
            },
        ),
    ]
