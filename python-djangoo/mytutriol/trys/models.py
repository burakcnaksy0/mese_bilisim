from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField(auto_now=True)
    isbn_number = models.CharField(max_length=13, default="")
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Computer(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.model


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Department(models.Model):
    dep_name = models.CharField(max_length=50)
    dep_number = models.IntegerField()

    def __str__(self):
        return self.dep_name


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    age = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name="courses")

    def __str__(self):
        return self.title


#    parents
#    children


class Parents(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Child(models.Model):
    name = models.CharField(max_length=50)
    parents = models.ManyToManyField(Parents)

    def __str__(self) -> str:
        return self.name


#  car
#  ceo


class Carr(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ceo(models.Model):
    car = models.OneToOneField(Carr, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Login(models.Model):
    username = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class App(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MovieApp(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateField(max_length=100)
    topic = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name
