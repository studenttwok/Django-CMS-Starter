from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<str:slug>/", views.page, name="page"),

    path("articles/", views.articles, name="articles"),
    path("articles/<int:id>-<str:slug>", views.article, name="article"),

    path("albums/", views.albums, name="albums"),
    path("albums/<int:id>-<str:slug>", views.album, name="album"),

    path("writers", views.writers, name="writers"),
    path("writers/<int:id>-<str:nickname>", views.writer, name="writer"),

]
