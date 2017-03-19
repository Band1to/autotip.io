from django.conf.urls import include, url
from django.contrib import admin
from autotip_io import views

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^giveaway/submission', views.giveaway_submission),
    url(r'^giveaway/info', views.giveaway_rules),
    url(r'^blog/(?P<pk>[\w-]+)', views.single_blog, name="single-blog"),
    url(r'^article/(?P<pk>[\w-]+)', views.single_article, name="single-article"),
    url(r'^articles/', views.article_index, name="article-index"),
    url(r'^docs/(?P<doc_name>[\w-]+)', views.docs, name="docs"),
    url(r'^getting-started/(?P<guide_name>[\w-]+)$', views.getting_started, name="getting-started"),
    url(r'^admin/', include(admin.site.urls)),
]
