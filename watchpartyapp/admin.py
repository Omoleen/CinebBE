from django.contrib import admin
from .models import PartyGroupMessage, PartyGroup

# Register your models here.
admin.site.register(PartyGroupMessage)
admin.site.register(PartyGroup)