from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaseStudyViewSet, CaseStudyListView, CaseStudyPlayView

app_name = 'case_studies'

router = DefaultRouter()
router.register(r'', CaseStudyViewSet, basename='case-study')

urlpatterns = [
    path('', CaseStudyListView.as_view(), name='list'),
    path('<int:pk>/play/', CaseStudyPlayView.as_view(), name='play'),
    path('api/', include(router.urls)),
]
