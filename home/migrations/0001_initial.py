# Generated by Django 4.0.3 on 2022-10-13 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('building_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('admin', models.CharField(max_length=100)),
                ('rooms', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_id', models.IntegerField(primary_key=True, serialize=False)),
                ('class_no', models.IntegerField()),
                ('year', models.IntegerField()),
                ('person_max', models.IntegerField()),
                ('opened', models.IntegerField()),
                ('enrolled', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('credit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('lecturer_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('major_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('time_id', models.IntegerField(primary_key=True, serialize=False)),
                ('period', models.IntegerField()),
                ('day', models.IntegerField()),
                ('begin', models.TimeField()),
                ('end', models.TimeField()),
                ('classInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.class')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('sex', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.lecturer')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.major')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.IntegerField(primary_key=True, serialize=False)),
                ('occupancy', models.IntegerField()),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.building')),
            ],
        ),
        migrations.AddField(
            model_name='lecturer',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.major'),
        ),
        migrations.CreateModel(
            name='Credits',
            fields=[
                ('credits_id', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('grade', models.CharField(max_length=2)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.course'),
        ),
        migrations.AddField(
            model_name='class',
            name='lecturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.lecturer'),
        ),
        migrations.AddField(
            model_name='class',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.major'),
        ),
        migrations.AddField(
            model_name='class',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.room'),
        ),
    ]
