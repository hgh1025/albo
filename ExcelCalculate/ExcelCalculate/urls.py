from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from main.views import index, blog, posting

urlpatterns = [
    path("email/", include('sendEmail.urls'), name='email'),
    path("calculate/", include('calculate.urls'), name='calculate'),
    path("", include('main.urls'), name='main'),
    path("admin/", admin.site.urls),
    # path('blog/', blog, name='blog'),
    # path('blog/<int:pk>/', posting, name='posting'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)