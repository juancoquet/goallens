from django.contrib import admin # type: ignore

from .models import Team, Fixture


# add search for fixture
class FixtureAdmin(admin.ModelAdmin):
    search_fields = ['id']

admin.site.register(Team)
admin.site.register(Fixture, FixtureAdmin)