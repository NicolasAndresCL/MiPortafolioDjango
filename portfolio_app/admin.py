from django.contrib import admin
from .models import Project, Skill, Experience, ExperienceHighlight


class ExperienceHighlightInline(admin.TabularInline):
    model = ExperienceHighlight
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date')
    inlines = [ExperienceHighlightInline]


admin.site.register(Project)
admin.site.register(Skill)