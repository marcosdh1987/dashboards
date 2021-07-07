from django.urls import path
from .views import comparisonView,HomeView, dashboardView,realtimeView,analyticsView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('comparison/', comparisonView.as_view(), name='comparison'),
    path('analytics/', analyticsView.as_view(), name='analytics'),
    path('dashboard/', dashboardView.as_view(), name='dashboard'),
    path('realtime/', realtimeView.as_view(), name='realtime'),
]