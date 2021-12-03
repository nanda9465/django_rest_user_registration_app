from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        sender = args[0].request.data.get("sender", "")
        receipient = args[0].request.data.get("receipient", "")
        if not sender and not receipient:
            return Response(
                data={
                    "message": "Both title and artist are required to add a song"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated
