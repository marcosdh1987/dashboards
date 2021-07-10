from django.urls import path
from .views import fsfdataView,HomeView, dashboardView,realtimeView,analyticsView,sepdataView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('fsfdata/', fsfdataView.as_view(), name='fsfdata'),
    path('sepdata/', sepdataView.as_view(), name='sepdata'),
    path('analytics/', analyticsView.as_view(), name='analytics'),
    path('dashboard/', dashboardView.as_view(), name='dashboard'),
    path('realtime/', realtimeView.as_view(), name='realtime'),
]