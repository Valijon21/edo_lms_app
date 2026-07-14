"""Umumiy sahifalar (bosh sahifa)."""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"
