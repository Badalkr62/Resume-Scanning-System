from django.shortcuts import render

def home(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def features(request):
    return render(request, 'home/features.html')

def how_it_works(request):
    return render(request, 'home/howitworks.html')

def contact(request):
    return render(request, 'home/contact.html')
def user(request):
    return render(request, 'user.html')