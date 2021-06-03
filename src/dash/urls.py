from django.urls import path
from .views import comparisonView,HomeView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('comparison/', comparisonView.as_view(), name='comparison'),

]