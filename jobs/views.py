from django.shortcuts import render, redirect, get_object_or_404

from .forms import JobForm
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Job


def add_job(request):

    if request.method == "POST":

        form = JobForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('job_list')

    else:

        form = JobForm()

    return render(request, 'jobs/add_job.html', {

        'form': form

    })


def job_list(request):

    search = request.GET.get("search")

    job_type = request.GET.get("type")

    jobs = Job.objects.all().order_by("-id")

    if search:

        jobs = jobs.filter(

            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(location__icontains=search)

        )

    if job_type:

        jobs = jobs.filter(job_type=job_type)

    paginator = Paginator(jobs, 5)

    page = request.GET.get("page")

    jobs = paginator.get_page(page)

    return render(request, "jobs/job_list.html", {

        "jobs": jobs

    })


# ---------------- View Job ---------------- #

def view_job(request, id):

    job = get_object_or_404(Job, id=id)

    return render(request,
                  "jobs/view_job.html",
                  {"job": job})


# ---------------- Edit Job ---------------- #

def edit_job(request, id):

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":

        form = JobForm(request.POST, instance=job)

        if form.is_valid():

            form.save()

            return redirect("job_list")

    else:

        form = JobForm(instance=job)

    return render(request,
                  "jobs/edit_job.html",
                  {
                      "form": form,
                      "job": job
                  })


# ---------------- Delete Job ---------------- #

def delete_job(request, id):

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":

        job.delete()

        return redirect("job_list")

    return render(request,
                  "jobs/delete_job.html",
                  {"job": job})
