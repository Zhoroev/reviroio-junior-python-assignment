
from django.urls import path
from .views import UserRequestView, user_request_result_view
urlpatterns = [
    path('', UserRequestView.as_view(), name='user_requests_url'),
    path('pull_requests', user_request_result_view, name='user_request_results_url')
]