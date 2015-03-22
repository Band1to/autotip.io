from django.contrib import admin
from .models import Blog, GiveawaySubmission

class GiveawaySubmissionAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'address')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'title', 'author')

admin.site.register(GiveawaySubmission, GiveawaySubmissionAdmin)
admin.site.register(Blog, BlogAdmin)
