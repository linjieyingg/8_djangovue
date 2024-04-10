from django.urls import path

from . import views

app_name = "reminders"

urlpatterns = [
    path("tags/new", views.TagCreateView.as_view(), name="tag_create"),
    path("tags/update/<int:pk>", views.TagUpdateView.as_view(),
         name="tag_update"),
    path("reminders/", views.ReminderListView.as_view(), name="reminder_list"),
    path("reminders/new", views.ReminderCreateView.as_view(), name="reminder_create"),
    path("reminders/<int:pk>", views.ReminderDetailView.as_view(),
         name="reminder_detail"),
    path("reminders/update/<int:pk>", views.ReminderUpdateView.as_view(),
         name="reminder_update"),
    path("reminders/delete/<int:pk>", views.ReminderDeleteView.as_view(),
         name="reminder_delete"),
    path("reminders/update_bis/<int:pk>", views.ReminderUpdatebisView.as_view(), 
         name="reminder_update_bis",),
    path("reminders/bis/<int:pk>", views.ReminderDetailbisView.as_view(), 
         name="reminder_detail_bis",),
    path("reminders/js/<int:pk>", views.ReminderDetailJsView.as_view(),
          name="reminder_detail_js",),
]
