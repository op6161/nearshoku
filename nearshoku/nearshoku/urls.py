from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import handler400, handler403, handler404, handler500


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('apps.result.urls')),
    # path("result/",include('apps.result.urls'), name='result'),
]
# handler400='nearshoku.views.bad_request_page'
# handler403='nearshoku.views.permission_denied_page'
# handler404='nearshoku.views.page+not_found_page'
# handler500='nearshoku.views.server_error_page'

from . import settings
from django.conf.urls.static import static
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)