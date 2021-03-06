from django.contrib import admin
from .models import Blog, GiveawaySubmission, Article

class GiveawaySubmissionAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'address', 'blockchain')

    def blockchain(self, obj):
        url = "https://blockchain.info/address/%s" % obj.address
        return "<a href='%s' target='_blank'>Link</a>" % url
    blockchain.allow_tags = True

class BlogAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'title', 'author')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'title', 'tagline', 'author')

admin.site.register(GiveawaySubmission, GiveawaySubmissionAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Article, ArticleAdmin)
