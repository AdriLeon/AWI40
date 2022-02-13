import json

texto = '''{
    "error": {
        "code": 400,
        "message": "INVALID_PASSWORD",
        "errors": [
            {
                "message": "INVALID_PASSWORD",
                "domain": "global",
                "reason": "invalid"
            }
        ]
    }
}'''

formato = json.loads(texto)
error = formato['error']
print(error['message'])