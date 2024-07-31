from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('track_requests/', views.track_requests_list, name='track_requests_list'),
    path('track_request/<int:request_id>/', views.track_request, name='track_request'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('update-request/<int:request_id>/', views.update_request, name='update_request'),
    path('account-info/', views.account_info, name='account_info'),
]
