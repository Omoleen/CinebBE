from django.db import models
from userapp.models import User
from userapp.utils import generate_code


class PartyGroup(models.Model):
    adminUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='party_group')
    id = models.CharField(max_length=128, unique=True, primary_key=True)
    url = models.URLField(null=True, blank=True)
    num_of_users = models.IntegerField(default=1)
    is_playing = models.BooleanField(default=False)
    current_time = models.DecimalField(max_digits=100, decimal_places=6, default=0.00)
    new_member = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        if not (self.pk and self.id):
            self.id = generate_code(12)
        return super().save(*args, **kwargs)


class PartyGroupMessage(models.Model):
    partyGroup = models.ForeignKey(PartyGroup, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    message_from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    message_from_machine = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.partyGroup} - Messages'

    @property
    def message_from(self):
        return self.message_from_user.name if self.message_from_user else 'Anonymous User'
