from django.urls import path
from .views import comparisonView,HomeView, dashboardView,realtimeView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('comparison/', comparisonView.as_view(), name='comparison'),
    path('dashboard/', dashboardView.as_view(), name='dashboard'),
    path('realtime/', realtimeView.as_view(), name='realtime'),
]