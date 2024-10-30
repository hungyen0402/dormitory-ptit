
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from app_core.views import *
from app_core.admin_views import *


urlpatterns = [

    path("admin/", admin.site.urls),
    path("", welcome_page, name="welcome-page"),
    path("admin_home", admin_home, name="admin-welcome-page"),
    path("login", login_page, name="login-page"),
    path("login_user", login_user, name="login-user"),
    path("logout_user", logout_page, name="logout-user"),
    path("register", register_page, name="register-user"),
    path("rooms", view_rooms, name="view-rooms"),
    path("app/", include("app_core.urls", namespace="app")),
<<<<<<< HEAD
=======
    path('ajax/check-username/', check_username, name='check_username'),
>>>>>>> 63aa1846705c4820b6c7138338646fed33c9eb31

]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)