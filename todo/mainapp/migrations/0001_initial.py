# Generated by Django 4.0.2 on 2022-03-29 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='наименование проекта')),
                ('description', models.TextField(verbose_name='описание проекта')),
                ('href_repo', models.URLField(verbose_name='ccылка на репозиторий')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления проекта в БД')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='дата последнего изменния')),
                ('initiator_project', models.ForeignKey(on_delete=models.SET('n/a'), to=settings.AUTH_USER_MODEL, verbose_name='uid инициатор проекта')),
            ],
        ),
        migrations.CreateModel(
            name='UserOnProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления проекта в БД')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='дата последнего изменния')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.project')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='не определен', max_length=64, verbose_name='заголовок заметки')),
                ('description', models.TextField(default='не определен', verbose_name='текст заметки')),
                ('is_active', models.BooleanField(default=True, verbose_name='статус заметки')),
                ('is_close', models.BooleanField(default=False, verbose_name='закрыто')),
                ('scheduled_date', models.DateTimeField(null=True, verbose_name='плановая дата завершения')),
                ('actual_date', models.DateTimeField(null=True, verbose_name='фактическая дата завершения')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления проекта в БД')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='дата последнего изменния')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.project')),
            ],
        ),
        migrations.CreateModel(
            name='Executor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления проекта в БД')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='дата последнего изменния')),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.todo')),
                ('user_on_project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.useronproject')),
            ],
        ),
    ]