from django.conf.urls import patterns, include, url
from django.contrib import admin
from autotip_io import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^blog/', views.blog),
    url(r'^giveaway/submission', views.giveaway_submission),
    url(r'^giveaway/info', views.giveaway_rules),
    url(r'^docs/(?P<doc_name>[\w-]+)', views.docs,name="docs"),
    url(r'^getting-started/(?P<guide_name>[\w-]+)$', views.getting_started, name="getting-started"),
    url(r'^admin/', include(admin.site.urls)),
)
