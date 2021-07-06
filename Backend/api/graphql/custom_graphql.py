from flask_graphql import GraphQLView

# https://stackoverflow.com/a/58129591


class CustomGraphqlView(GraphQLView):
    """
    tweak the implementation of `format_error`
    to support custom errors.

    to utilize this you must provide `context` attribute with your
    custom exceptions:
        class APIException(Exception):

            def __init__(self, message, status=None):
                self.context = {}
                if status:
                    self.context['status'] = status
                super().__init__(message)
    """

    @staticmethod
    def format_error(error):
        formatted_error = super(
            CustomGraphqlView, CustomGraphqlView
        ).format_error(error)
        try:
            # This will look for the context attribute in any exceptions raised.
            # If it exists, it'll populate the error with this data.
            formatted_error["context"] = error.original_error.context
        except AttributeError:
            pass
        return formatted_error
