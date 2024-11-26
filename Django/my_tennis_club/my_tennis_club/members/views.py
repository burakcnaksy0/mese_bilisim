from django.http import HttpResponse
from django.shortcuts import render

def members(request):
  return render(request, "index.html")