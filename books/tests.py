from django.test import TestCase
from django.urls import reverse 
from django.contrib.auth import get_user_model
from .models import Book, Review 



class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'reviewuser',
            email = 'reviewuser@email.com',
            password = 'testpass123'
        )

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
    

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, "This is a list")
        self.assertTemplateUsed(response, 'books/book_list.html')
    
    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/2314/')
        self.assertTrue(response.status_code, 200)
        self.assertTrue(no_response.status_code, 404)
        self.assertContains(response, "Price:")
        self.assertContains(response, "This is a test review")
        self.assertNotContains(response, "This is a NOT a test review")
        self.assertTemplateUsed(response, 'books/book_detail.html')

    


