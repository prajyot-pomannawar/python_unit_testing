import json
from django.test import TestCase
from ..models import User, Book
from .test_views import client, reverse, status
from ..serializer import UserSerializer, BookSerializer
from .. import views
from django.urls import resolve, reverse


class UserSampleTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            fname='virat', lname='kohli', email='virat@gmail', password='virat@123', mobile='9881726838')
        User.objects.create(
            fname='rohit', lname='sharma', email='rohit@gmail', password='rohit@123', mobile='9552566838')

    def test_get_user(self):
        first_user = User.objects.get(fname='virat')
        second_user = User.objects.get(fname='rohit')
        self.assertEqual(first_user.email, "virat@gmail")
        self.assertEqual(second_user.password, "rohit@123")


class UserTestCase(TestCase):

    def setUp(self):
        self.first_user = User.objects.create(
            fname='virat', lname='kohli', email='virat@gmail', password='virat@123', mobile='9881726838')
        self.second_user = User.objects.create(
            fname='rohit', lname='sharma', email='rohit@gmail', password='rohit@123', mobile='9552566838')
        self.third_user = User.objects.create(
            fname='shikhar', lname='dhavan', email='shikhar@gmail', password='shikhar@123', mobile='9552566838')
        self.valid_user = {
            'fname': 'akash', 'lname': 'devlekar', 'email': 'akash@gmail',
            'password': 'akash@123', 'mobile': '7276820982'
        }
        self.updated_user = {
            'fname': 'Ms', 'lname': 'Dhoni', 'email': 'dhoni@gmail',
            'password': 'dhoni@123', 'mobile': '8776547888',
        }

    def test_delete_user(self):
        response = client.delete(reverse('delete_user', kwargs={'id': self.third_user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user(self):
        response = client.put(reverse('edit_user', kwargs={'id': self.first_user.pk}),
                              data=json.dumps(self.updated_user), content_type='application/json' )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_user(self):
        response = client.post('/user', data=json.dumps(self.valid_user), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_users(self):
        response = client.get('/user')
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_user(self):
        response = client.get(reverse('view_single_user', kwargs={'id': self.first_user.pk}))
        user = User.objects.get(id=self.first_user.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookSampleTestCase(TestCase):
    def setUp(self):
        Book.objects.create(
            title='C++ in one month', author='Grady Bush', publication='Mehta',
            type='education', isbn='111', price='550')
        Book.objects.create(
            title='ASP .NET Black Book', author='Mahesh Panhale', publication='Bonaventure publications',
            type='cdac', isbn='222', price='600')

    def test_get_book(self):
        first_book = Book.objects.get(title='C++ in one month')
        second_book = Book.objects.get(title='ASP .NET Black Book')
        self.assertEqual(first_book.author, "Grady Bush")
        self.assertEqual(second_book.type, "cdac")


class BookSampleTestCase(TestCase):
    def setUp(self):
        Book.objects.create(
            title='Panipat', author='Vishwas Patil', publication='Mehta',
            type='History', isbn='111', price='550')
        Book.objects.create(
            title='Musafir', author='Achyut Godbole', publication='Saket',
            type='auto biography', isbn='222', price='800')
        Book.objects.create(
            title='Sherlock', author='Arthur Doyal', publication='UK Publish',
            type='Story', isbn='333', price='450')

    def test_get_all_books(self):
        response = client.get('/book')
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookTestCase(TestCase):
    def setUp(self):
        self.first_book = Book.objects.create(
            title='Panipat', author='Vishwas Patil', publication='Mehta',
            type='History', isbn='111', price='550')
        self.second_book = Book.objects.create(
            title='Musafir', author='Achyut Godbole', publication='Saket',
            type='auto biography', isbn='222', price='800')
        self.third_book = Book.objects.create(
            title='Sherlock', author='Arthur Doyal', publication='UK Publish',
            type='Story', isbn='333', price='450')
        self.valid_Book = {
            'title': 'Java', 'author': 'Sandeep Kulange', 'publication': 'sunbeam',
            'type': 'coding', 'isbn': '111', 'price': '1000'
        }
        self.updated_Book = {
            'title': 'Java', 'author': 'Sandeep Kulange', 'publication': 'sunbeam',
            'type': 'coding', 'isbn': '333', 'price': '1000'
        }

    def test_delete_book(self):
        response = client.delete(reverse('delete_book', kwargs={'id': self.third_book.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_book(self):
        response = client.put(reverse('edit_book', kwargs={'id': self.first_book.pk}),
                              data=json.dumps(self.updated_Book), content_type='application/json' )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_book(self):
        response = client.post('/book', data=json.dumps(self.valid_Book), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_books(self):
        response = client.get('/book')
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_book(self):
        response = client.get(reverse('view_single_book', kwargs={'id': self.first_book.pk}))
        book = Book.objects.get(id=self.first_book.pk)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class URLTestCase(TestCase):

    def test_view_all_user_url(self):
        path = reverse('view_all_users')
        self.assertEqual(resolve(path).view_name, 'view_all_users')


