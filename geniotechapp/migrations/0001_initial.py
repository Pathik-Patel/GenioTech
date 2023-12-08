# Generated by Django 4.0.6 on 2023-11-24 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('full_name', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField()),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('gender', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_instructor', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('price_individual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_group', models.DecimalField(decimal_places=2, max_digits=10)),
                ('from_age', models.PositiveIntegerField()),
                ('to_age', models.PositiveIntegerField()),
                ('enrolled_students', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('course_taught', models.CharField(blank=True, max_length=255, null=True)),
                ('students_taught', models.JSONField(default=dict)),
                ('availability', models.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructors',
            },
            bases=('geniotechapp.customuser',),
        ),
        migrations.CreateModel(
            name='TimeSlotAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zoom_link', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geniotechapp.course')),
                ('timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geniotechapp.timeslot')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geniotechapp.instructor')),
            ],
        ),
    ]
