from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.NoteListView.as_view(), name="note_list"),
    path("new/", views.NoteCreateView.as_view(), name="note_create"),
    path("<int:pk>/", views.NoteDetailView.as_view(), name="note_detail"),
    path("<int:pk>/edit/", views.NoteUpdateView.as_view(), name="note_update"),
    path("<int:pk>/delete/", views.NoteDeleteView.as_view(), name="note_delete"),
    path("accounts/login/", views.NoteLoginView.as_view(), name="login"),
    path("accounts/register/", views.NoteRegisterView.as_view(), name="register"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
]
