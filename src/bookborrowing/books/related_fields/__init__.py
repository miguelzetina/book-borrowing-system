from collections import OrderedDict

from rest_framework_json_api.relations import ResourceRelatedField


class ResourceRelatedGenreField(ResourceRelatedField):

    def to_representation(self, value):
        return OrderedDict([
            ('id', str(value.pk)),
            ('name', value.name)
        ])


class ResourceRelatedAuthorField(ResourceRelatedField):

    def to_representation(self, value):
        return OrderedDict([
            ('id', str(value.pk)),
            ('first_name', value.first_name),
            ('second_name', value.first_name),
            ('date_of_birth', value.date_of_birth),
            ('date_of_death', value.date_of_death)
        ])