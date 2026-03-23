from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page),
    path("register/", views.register_page),
    path("dashboard/", views.dashboard_page),
    path("check/", views.check_page),
    path("generate/", views.generate_page),
    path("mypasswords/", views.mypasswords_page),
    path("delete/<int:id>/", views.delete_password),
    path("logout/", views.logout_page),
]
