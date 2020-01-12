from rest_framework.response import Response
import hashlib


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


class HashStringGenerator:
    def generate(hash_input):
        encryptor = hashlib.md5()
        encryptor.update(hash_input.encode("utf-8"))
        return encryptor.hexdigest()
