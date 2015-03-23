from django.conf.urls import patterns, include, url
from django.contrib import admin
from autotip_io import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^blog/', views.blog),
    url(r'^giveaway/submission', views.giveaway_submission),
    url(r'^giveaway/info', views.giveaway_rules),
    url(r'^docs/chrome_extension', views.chrome_extension_docs),
    url(r'^admin/', include(admin.site.urls)),
)
