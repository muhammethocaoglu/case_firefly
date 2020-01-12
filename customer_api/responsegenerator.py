from rest_framework.response import Response


class ResponseGenerator:
    def generate(status_code, message, result):
        response = {"status_code": status_code,
                    "message": message,
                    "body": result}
        return Response(response)

    def generate_without_body(status_code, message):
        response = {"status_code": status_code,
                    "message": message}
        return Response(response)
