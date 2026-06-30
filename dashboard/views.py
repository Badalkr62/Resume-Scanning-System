from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):

    context = {
        "jobs": 10,
        "resumes": 45,
        "shortlisted": 15,
        "pending": 30
    }

    return render(request,
                  "dashboard/dashboard.html",
                  context)
