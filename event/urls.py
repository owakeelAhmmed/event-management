from django.urls import path
from event.views import home
from .import views

urlpatterns = [
    path('', home),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),


    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/update/<int:pk>/', views.update_event, name='update_event'),
    path('events/delete/<int:pk>/', views.delete_event, name='delete_event'),


    path('participants/', views.participant_list, name='participant_list'),
    path('participants/create/', views.create_participant, name='create_participant'),
    path('participants/update/<int:pk>/', views.update_participant, name='update_participant'),
    path('participants/delete/<int:pk>/', views.delete_participant, name='delete_participant'),
    

    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/events/<str:filter_type>/", views.event_filter_api, name="event_filter_api"),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

    path('rsvp/<int:event_id>/', views.rsvp_event, name='rsvp_event'),

    path('dashboard/', views.participant_dashboard, name='participant_dashboard'),

]