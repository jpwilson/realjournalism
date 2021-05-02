from django.test import Client, TestCase
from django.urls import reverse 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from .models import Book, Review 



class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'reviewuser',
            email = 'reviewuser@email.com',
            password = 'testpass123'
        )

        self.special_permission = Permission.objects.get(codename='special_status')

        self.book = Book.objects.create(
            title="How to get Rich",
            author="Felix Dennis",
            price="34.00",
        )

        self.review = Review.objects.create(
            author = self.user,
            book = self.book,
            review = 'This is a test review',
        )
    
    def test_book_listing(self):
        self.assertEqual(self.book.title, "How to get Rich")
        self.assertEqual(self.book.author, "Felix Dennis")
        self.assertEqual(self.book.price, "34.00")
    

    def test_logged_in_book_list_view(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        response = self.client.get(reverse('book_list'))
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, "This is a list")
        self.assertTemplateUsed(response, 'books/book_list.html')
    
    def test_logged_out_book_list_view(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/books/' % reverse('account_login'))
        response = self.client.get(
            '%s?next=/books/' % (reverse('account_login')))
        self.assertContains(response, "Log In")
        self.assertTemplateUsed(response, 'account/login.html')
    
    def test_book_detail_view_with_permissions(self):
        self.client.login(
            email = 'reviewuser@email.com',
            password = 'testpass123'
        )
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/2314/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Price:")
        self.assertContains(response, "This is a test review")
        self.assertNotContains(response, "This is a NOT a test review")
        self.assertTemplateUsed(response, 'books/book_detail.html')

    # def test_book_detail_view_without_permission(self):
    #     response = self.client.get(self.book.get_absolute_url())
    #     no_response = self.client.get('/books/2314/')
    #     self.assertTrue(response.status_code, 200)
    #     self.assertTrue(no_response.status_code, 404)
    #     self.assertContains(response, "Price:")
    #     self.assertContains(response, "This is a test review")
    #     self.assertNotContains(response, "This is a NOT a test review")
    #     self.assertTemplateUsed(response, 'books/book_detail.html')
    


