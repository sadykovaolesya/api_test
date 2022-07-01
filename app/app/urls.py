from django.contrib import admin
from django.urls import path

from api.views import BillViews, ClientViews, FileUploadView

urlpatterns = [
    path("api/upload/", FileUploadView.as_view()),
    path("api/clients/", ClientViews.as_view()),
    path("api/bills", BillViews.as_view()),
    path("admin/", admin.site.urls),
]