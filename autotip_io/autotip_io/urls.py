from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autotip_io.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^giveaway_submission', 'autotip_io.views.giveaway_submission')
    url(r'^admin/', include(admin.site.urls)),
)
