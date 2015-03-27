from django.contrib import admin
from .models import Blog, GiveawaySubmission

class GiveawaySubmissionAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'address', 'blockchain')

    def blockchain(self, obj):
        url = "https://blockchan.info/address/%s" % obj.address
        return "<a href='%s'>Link</a>" % url
    blockchain.allow_tags = True

class BlogAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'title', 'author')

admin.site.register(GiveawaySubmission, GiveawaySubmissionAdmin)
admin.site.register(Blog, BlogAdmin)
