from rest_framework_json_api import serializers

from bookborrowing.books.models import Author, Book, Genre
from bookborrowing.books.related_fields import (
    ResourceRelatedGenreField, ResourceRelatedAuthorField
)


class BookSerializer(serializers.ModelSerializer):

    genre = ResourceRelatedGenreField(queryset=Genre.objects, many=True)
    author = ResourceRelatedAuthorField(queryset=Author.objects, many=True)

    class Meta:
        model = Book
        fields = (
            'id',
            'name',
            'isbn',
            'summary',
            'author',
            'genre'
        )