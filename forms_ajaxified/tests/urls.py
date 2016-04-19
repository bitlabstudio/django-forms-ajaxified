"""URLs to run the tests."""
from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^', include('forms_ajaxified.tests.test_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
