from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from job.models import Job


@login_required(login_url="login")
def index(request):
    jobs = Job.objects.filter(status="Active").order_by("-created_at")[:3]

    return render(
        request,
        "home/index.html",
        {
            "jobs": jobs
        }
    )


@login_required(login_url="login")
def user_section(request):
    return render(request, "home/user_section.html")


def companies(request):
    companies = Job.objects.values(
        "company",
        "location"
    ).distinct()

#     return render(request, "company/companies.html", {
#         "companies": companies
#     })


# def company_detail(request, company_name):
#     jobs = Job.objects.filter(company=company_name)
#     company = jobs.first()
#     return render(request, "company/company_detail.html", {
#         "company": company,
#         "jobs": jobs,
#     })
