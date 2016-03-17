from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['question_text']
        }),
        ('Date information', {
            'fields': ['created'],
            'classes': ['collapse']
        }),
    ]
    inlines = [ChoiceInline]
    list_display = ['question_text', 'created', 'was_created_recently']
    list_filter = ['created']
    readonly_fields = ['created']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
