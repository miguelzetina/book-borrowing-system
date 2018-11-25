import uuid
from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _

from isbn_field import ISBNField

from bookborrowing.users.models import User
from bookborrowing.core.db.models import CatalogueMixin, TimeStampedMixin


class Genre(CatalogueMixin):
    """
    Model representing a book genre.
    """
    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Author(TimeStampedMixin):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField('Birth', null=True, blank=True)

    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} ({1})'.format(self.first_name, self.last_name)


class Book(CatalogueMixin):
    """
    Model representing a book (but not a specific copy of a book).
    """
    author = models.ManyToManyField(
        Author,
        related_name='books',
        related_query_name='book',
    )

    summary = models.TextField(max_length=1000)
    
    isbn = ISBNField(unique=True)

    # ManyToManyField used because genre can contain many books.
    # Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre,
        related_name='books',
        related_query_name='book'
    )

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book
    (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='books',
        related_query_name='book'
    )

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1, choices=LOAN_STATUS, blank=True, default='a'
    )

    class Meta:
        verbose_name = _('book instance')
        verbose_name_plural = _('book instances')

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} ({1})'.format(self.id, self.book.title)