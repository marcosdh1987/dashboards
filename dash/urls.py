from django.urls import path
from .views import fsfdataView,HomeView, dashboardView,realtimeView,analyticsView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('fsfdata/', fsfdataView.as_view(), name='fsfdata'),
    path('analytics/', analyticsView.as_view(), name='analytics'),
    path('dashboard/', dashboardView.as_view(), name='dashboard'),
    path('realtime/', realtimeView.as_view(), name='realtime'),
]