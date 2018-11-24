from django.test import TestCase

from bookborrowing.books.models import Author, Book, BookInstance, Genre


class GenreModelsTestCase(TestCase):
    """
    Tests for the bookborrowing.books.models.Genre class.
    """

    fixtures = [
        'genres'
    ]

    def test_genre_model(self):
        genre = Genre.objects.first()
        self.assertEqual(genre.name, 'Genre 1')

    def test_genre_model_no_books(self):
        genre = Genre.objects.first()
        self.assertEqual(genre.books.count(), 0)

    def test_string_representation(self):
        genre = Genre.objects.first()
        self.assertEqual(str(genre), genre.name)


class AuthorModelsTestCase(TestCase):
    """
    Tests for the bookborrowing.books.models.Author class.
    """

    fixtures = [
        'authors'
    ]

    def test_author_model(self):
        author = Author.objects.first()
        self.assertEqual(author.first_name, 'First name')
        self.assertEqual(author.last_name, 'Last name')

    def test_author_model_no_books(self):
        author = Author.objects.first()
        self.assertEqual(author.books.count(), 0)

    def test_string_representation(self):
        author = Author.objects.first()
        self.assertEqual(
            str(author),
            '{0} ({1})'.format(author.first_name, author.last_name)
        )


class BookModelsTestCase(TestCase):
    """
    Tests for the bookborrowing.books.models.Book class.
    """

    fixtures = [
        'authors',
        'genres',
        'books'
    ]

    def test_book_model(self):
        book = Book.objects.first()
        author = Author.objects.first()
        self.assertEqual(book.name, 'Book name')
        self.assertEqual(book.author.first().first_name, author.first_name)
        self.assertEqual(
            str(book.author.first()),
            '{0} ({1})'.format(author.first_name, author.last_name)
        )

    def test_author_model_books(self):
        author = Author.objects.first()
        self.assertEqual(author.books.count(), 1)

    def test_genre_model_books(self):
        genre = Genre.objects.first()
        self.assertEqual(genre.books.count(), 1)

    def test_string_representation(self):
        book = Book.objects.first()
        self.assertEqual(str(book), book.name)