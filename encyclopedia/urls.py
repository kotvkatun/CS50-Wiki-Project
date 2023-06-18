from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random_view, name="random"),
    path("search/", views.search_results, name="search_results"),
    path("new_page/", views.make_new_page, name="make_new_page"),
    path("edit_page/<str:title>/", views.edit_page, name="edit_page"),
    path("save_changes/<str:title>/", views.save_changes, name="save_changes_page"),
    path("save_page/", views.save_page, name="save_page"),
    path("<str:title>/", views.wiki_page, name="wiki_page"),
]
