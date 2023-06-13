# Generated by Django 4.2.1 on 2023-06-13 11:17

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
            name='PartyGroup',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('num_of_users', models.IntegerField(default=0)),
                ('is_playing', models.BooleanField(default=False)),
                ('current_time', models.DecimalField(decimal_places=6, default=0.0, max_digits=100)),
                ('new_member', models.BooleanField(default=False)),
                ('adminUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='party_group', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartyGroupMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('message_from_machine', models.BooleanField(default=False)),
                ('message_from_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('partyGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='watchpartyapp.partygroup')),
            ],
        ),
    ]
