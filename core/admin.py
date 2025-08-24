from django.contrib import admin
from .models import Party, County, Constituency, Candidate
# Register your models here.

admin.site.register(Party)
admin.site.register(County)
admin.site.register(Constituency)
admin.site.register(Candidate)
