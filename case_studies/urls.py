from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CaseStudyViewSet, CaseStudyListView

app_name = 'case_studies'

router = DefaultRouter()
router.register(r'', CaseStudyViewSet, basename='case-study')

urlpatterns = [
    path('play/', CaseStudyListView.as_view(), name='play'),
] + router.urls
