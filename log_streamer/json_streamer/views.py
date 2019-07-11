# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import JsonResponse
from django.views import View

# Create your views here.

OFFSET_NOT_SUPPLIED = "OFFSET_NOT_SUPPLIED"
FILE_NOT_FOUND = "FILE_NOT_FOUND"
WRONG_ENCODING = "WRONG_ENCODING"
INCORRECT_OFFSET = "INCORRECT_OFFSET"

EXCEPTIONS = {
    OFFSET_NOT_SUPPLIED: "offset not supplied",
    FILE_NOT_FOUND: "file not found",
    WRONG_ENCODING: "file should be encoded with UTF-8",
    INCORRECT_OFFSET: "incorrect offset",
}


class JSONStreamer(View):
    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)
        if json_data == {}:
            response_body = {"ok": False,
                             "reason": EXCEPTIONS.get(OFFSET_NOT_SUPPLIED)}
        elif not isinstance(json_data.get("offset"), int):
            response_body = {"ok": False,
                             "reason": EXCEPTIONS.get(INCORRECT_OFFSET)}
        else:
            response_body = {"ok": False,
                             "reason": EXCEPTIONS.get(FILE_NOT_FOUND)}
        return JsonResponse(response_body, status=200)
