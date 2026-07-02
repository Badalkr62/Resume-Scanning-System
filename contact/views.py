from django.shortcuts import render, redirect
from django.contrib import messages
from contact.forms import ContactForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "home/contact.html", {"form": form})