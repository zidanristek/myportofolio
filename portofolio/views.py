from django.shortcuts import render


def landing_page(request):
    """Render the portfolio landing page."""
    return render(request, "index.html")
