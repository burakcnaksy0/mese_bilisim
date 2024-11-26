from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)

# Create your views here.
data = {
    "computer": ["asus","lenovo","hp","monster"],
    "phone": ["ıphone15","ıphone16","samsung s21"],  
    "laptop": ["laptop1","laptop2","laptop3"],
    "electronics": [],
}

def indeks(request):
    category_list = list(data.keys())
    
    return render(request,'myapp/index.html',{
        
        'category_list': category_list
    })
    
    
    
    
def home(request):
    return render(request,'myapp/index.html')


def index(request):
    list_items = ""
    category_list = list(data.keys())

    for category in category_list:
        redirect_path = reverse("products_by_category", args=[category])
        list_items += f'<li><a href="{redirect_path}">{category}</a></li>'

    html = f"<ul>{list_items}</ul>"
    return HttpResponse(html)


def details(request):
    return HttpResponse("details")


def getProductsCategoryId(request, category_id):
    redirect_text = None
    category_lists = list(data.keys())
    if category_id > len(category_lists):
        return HttpResponseNotFound("category not found")
    if category_id > 0:
        redirect_text = category_lists[category_id - 1]

        redirect_path = reverse("products_by_category", args=[redirect_text])

        return redirect(redirect_path)
    else:
        return HttpResponseNotFound("category not found")


def getProductsCategory(request, category):
    try:
        products = data[category]
#       return HttpResponse(f"<h1>{category_text}</h1>")
        return render(request,"myapp/product.html" , 
        {
            "category": category,
            "products": products
            
        })
    except:
        HttpResponseNotFound(f"<h1>category not found</h1>")
