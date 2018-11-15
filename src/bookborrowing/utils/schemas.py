# -*- coding: utf-8 -*-
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors.view import SwaggerAutoSchema

from bookborrowing.utils.inspectors import (
    ModelSerializerInspector, ResponsePaginationInspector
)


class CustomJSONAPISchema(SwaggerAutoSchema):
    field_inspectors = (
        [ModelSerializerInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS
    )

    paginator_inspectors = (
        [ResponsePaginationInspector] +
        swagger_settings.DEFAULT_PAGINATOR_INSPECTORS
    )

    def get_responses(self):
        """
        Get the possible responses for this view as a swagger
        :class:`.Responses` object.
        :return: the documented responses
        :rtype: openapi.Responses
        """
        response_serializers = self.get_response_serializers()
        response_serializers.update({"400": "BAD REQUEST"})
        response_serializers.update({"403": "FORBIDDEN"})
        response_serializers.update({"500": "INTERNAL SERVER ERROR"})
        return openapi.Responses(
            responses=self.get_response_schemas(response_serializers)
        )
