from django.forms import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.template import loader
from .models import *
from .forms import *


def add_photo(request):
    print("add_photo")
    # movie = get_object_or_404(MovieApp, id=movie_id)
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)  # MovieForm kullan
        if form.is_valid():
            form.save()
            return redirect("movielist")  # Güncelleme sonrası yönlendirme
    else:
        form = MovieForm()

    return render(request, "addphoto.html", {"form": form})


def detail_movie(request, movie_id):
    movie = get_object_or_404(MovieApp, id=movie_id)
    if request.method == "POST":
        movie.objects.get(id=movie_id)
        return redirect("movielist")

    return render(request, "detail.html", {"movie": movie})


def delete_movie(request, movie_id):
    # MovieApp modelinden silmek istediğiniz nesneyi al
    movie = get_object_or_404(MovieApp, id=movie_id)

    if request.method == "POST":
        # Nesneyi sil
        movie.delete()
        return redirect("movielist")  # Silme sonrası yönlendirme

    # Eğer POST değilse, silme onay sayfasını göster
    return render(request, "delete.html", {"movie": movie})


def update_movie(request, movie_id):
    movie = get_object_or_404(MovieApp, id=movie_id)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES ,instance=movie)  # MovieForm kullan
        if form.is_valid():
            form.save()
            return redirect("movielist")  # Güncelleme sonrası yönlendirme
    else:
        form = MovieForm(instance=movie)  # MovieForm kullan

    return render(request, "update_movie.html", {"form": form, "movie": movie})


def movie_list(request):
    movie_list = MovieApp.objects.all()
    return render(request, "movielist1.html", {"movie_list": movie_list})


def movie_app(request):

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            year = form.cleaned_data["year"]
            topic = form.cleaned_data["topic"]
            message = form.cleaned_data["message"]
            image = form.cleaned_data["image"]  

            movie = MovieApp(
                name=name, year=year, topic=topic, message=message, image=image
            )
            movie.save()
            return redirect("movie_register")
        else:
            return render(request, "invalıd.html", {"form": form})

    else:
        form = MovieForm()
    return render(request, "movielogin.html", {"form": form})


def movie_register(request):
    movie_list = MovieApp.objects.all()
    number = len(movie_list)
    return render(
        request, "movieregister.html", {"movie_list": movie_list, "number": number}
    )


def movielist(request):
    movie_list = MovieApp.objects.all()
    number = len(movie_list)
    return render(
        request, "movielist.html", {"movie_list": movie_list, "number": number}
    )


def AppRegister(request):
    app_list = App.objects.all()
    return render(request, "appregister.html", {"app_list": app_list})


def AppLogin(request):
    if request.method == "POST":
        form = İnstagram(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

            app1 = App(
                name=name,
                surname=surname,
                username=username,
                password=password,
                email=email,
            )
            app1.save()
            return redirect("appregister")
    else:
        form = İnstagram()
    return render(request, "applogin.html", {"form": form})


def register_view(request):  # submitten sonra gelecek sayfa
    return render(request, "register.html")


def login_view(request):  # bizi ilk karşılayan sayfa
    if request.method == "POST":
        form = LoginUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            surname = form.cleaned_data["surname"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            login = Login(
                username=username,
                surname=surname,
                password=password,
                email=email,
                message=message,
            )
            login.save()

            return redirect("register")
    else:
        form = LoginUser()
    return render(request, "loginuser.html", {"form": form})


def success_view(request):
    contact_list = Contact.objects.all()
    return render(request, "success.html", {"contact_list": contact_list})


def contact_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)  # olusturdugumuz form
        if form.is_valid():
            # Form verilerini al
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # Yeni Contact nesnesi oluştur ve kaydet
            contact = Contact(
                name=name, email=email, message=message
            )  # model olusturup formumuz veritabanında saklıyoruz.
            contact.save()

            # Başarılı işlem sonrası yönlendirme
            return redirect("success")  # 'success' URL'sini tanımlaman gerekiyor
    else:
        form = MyForm()
    return render(request, "contact.html", {"form": form})


def ceo_list(request):
    ceo_list = Ceo.objects.prefetch_related("car").all()
    return render(request, "ceos.html", {"ceo_list": ceo_list})


def child_list(request):
    children = Child.objects.prefetch_related("parents").all()
    return render(request, "child.html", {"children": children})


def course_list(request):
    courses = Course.objects.prefetch_related("students").all()
    return render(request, "course.html", {"courses": courses})


def employee_list(request):
    employee = Employee.objects.select_related("department").all()
    return render(request, "employee.html", {"employee": employee})


def author_books_view(request):
    books = Books.objects.select_related(
        "author"
    ).all()  # Yazar bilgileriyle birlikte tüm kitapları al
    return render(request, "author_books.html", {"books": books})


def computer_list(request):
    computers = Computer.objects.all()  # Değişken adını 'computers' yapıyoruz.
    return render(
        request, "comp_list.html", {"Computer": computers}
    )  # Anahtar 'Computer' olarak kalıyor.


def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})


def book_list(request):
    # Book modelinden verileri çek
    books = Book.objects.all()  # Tüm kitapları al
    return render(request, "book_list.html", {"books": books})


data = {"phone": "+90", "name": "John", "surname": "Mıke"}


def testing1(request):
    mydata = Book.objects.all().values()
    template = loader.get_template("template.html")
    context = {
        "mybooks": mydata,
    }
    return HttpResponse(template.render(context, request))


def my_numbers(
    request,
):  # render fonksiyonunu çağırırken context'i bir sözlük olarak geçiyorsun ama zaten bir sözlük içinde context var.
    context = {"myvar": 2}
    return render(request, "number.html", context)


def my_names(request):
    name_list = (
        data.items()
    )  # sözlüğü listeye dönüştürme( Eğer sözlükteki verileri for döngüsü kullanarak yazdırmak istiyorsan,
    # sözlüğü bir listeye dönüştürüp o listeyi döngü ile geçebilirsin. İşte nasıl yapabileceğin:)

    return render(request, "forloop.html", {"name_list": name_list})


def my_view(request):
    name_list = ["Alice", "Bob", "Charlie"]  # Örnek liste
    return render(request, "ty.html", {"name_list": name_list})


def testing(request):

    return render(request, "childtemplate.html")


def extends(request):
    return render(request, ("extends.html"))


def image(request):
    return render(request, ("image.html"))


def add_book(request):
    new_book = Book(
        title="Django Unleashed",
        author="Andrew P. Trask",
        published_date="2021-05-15",
        isbn_number="9876543210123",
    )
    new_book.save()
    return HttpResponse("<h1> Book added successfully! </h1>")


def add_book1(request):
    new_book = Book(
        title="gold dog",
        author="john snow",
        published_date="2023-04-27",
        isbn_number="2660303105",
    )
    new_book.save()
    return HttpResponse("<h1> Book added successfully! new command !</h1>")


def list_books(request):
    all_books = Book.objects.all()
    return render(request, "myapp/book_list.html", {"books": all_books})
