from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("testing/", views.testing),
    path("my_view/", views.my_view),
    path("my_view/", views.my_view),
    path("my_numbers/", views.my_numbers),
    path("my_names/", views.my_names),
    path("my_rules/", views.extends),
    path("my_image/", views.image),
    path("add-book/", views.add_book),
    # path("books/", views.list_books),
    path("add-book1/", views.add_book1),
    path("testing1/", views.testing1),
    path("books/", views.book_list),
    path("users/", views.user_list),
    path("computers/", views.computer_list),
    path("author-books/", views.author_books_view),
    path("employee/", views.employee_list),
    path("courses/", views.course_list),
    path("child/", views.child_list),
    path("ceo/", views.ceo_list),
    path("contact/", views.contact_view, name="contact"),
    path("success/", views.success_view, name="success"),
    path("loginuser/", views.login_view, name="loginuser"),
    path("register/", views.register_view, name="register"),
    path("applogin/", views.AppLogin, name="applogin"),
    path("appregister/", views.AppRegister, name="appregister"),
    
    path("movielogin/", views.movie_app, name="movielogin"),
    path("movie_register/", views.movie_register, name="movie_register"),
    path("movielist/", views.movielist, name="movielist"),
    path("movies/", views.movie_list, name="movie_list"),
    path("movie/update/<int:movie_id>/", views.update_movie, name="update_movie"),
    path("movies/delete/<int:movie_id>/", views.delete_movie, name="delete"),
    path("movies/detail/<int:movie_id>/", views.detail_movie, name="detail"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
