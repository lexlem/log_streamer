# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from utils import file_lines_count, read_file_by_chunks

# Create your views here.

OFFSET_NOT_SUPPLIED = "OFFSET_NOT_SUPPLIED"
FILE_NOT_FOUND = "FILE_NOT_FOUND"
WRONG_JSON_FORMAT = "WRONG_JSON_FORMAT"
INCORRECT_OFFSET_FORMAT = "INCORRECT_OFFSET_FORMAT"
END_OF_FILE = "END_OF_FILE"

EXCEPTIONS = {
    OFFSET_NOT_SUPPLIED: "offset not supplied",
    FILE_NOT_FOUND: "file not found",
    WRONG_JSON_FORMAT: "wrong json format",
    INCORRECT_OFFSET_FORMAT: "incorrect offset format",
    END_OF_FILE: "offset reached end of file"
}


@method_decorator(csrf_exempt, name='dispatch')
class JSONStreamer(View):
    def post(self, request, *args, **kwargs):
        try:
            json_data = json.loads(request.body)
            if json_data == {}:
                response_body = {"ok": False,
                                 "reason": EXCEPTIONS.get(OFFSET_NOT_SUPPLIED)}
            elif not isinstance(json_data.get("offset"), int):
                response_body = {"ok": False,
                                 "reason": EXCEPTIONS.get(INCORRECT_OFFSET_FORMAT)}
            else:
                try:
                    offset = json_data.get("offset")
                    file_length = os.path.getsize(
                        os.environ.get("LOG_FILE_PATH"))
                    if offset >= file_length:
                        response_body = {
                            "ok": False,
                            "reason": EXCEPTIONS.get(END_OF_FILE)
                        }
                    else:
                        message, next_offset = read_file_by_chunks(
                            os.environ.get("LOG_FILE_PATH"), json_data.get("offset"))
                        response_body = {
                            "ok": True,
                            "next_offset": next_offset,
                            "total_size": file_length,
                            "messages": [json.loads(jline) for jline in message.split('\n')]
                        }
                except IOError:
                    response_body = {"ok": False,
                                     "reason": EXCEPTIONS.get(FILE_NOT_FOUND)}
        except ValueError:
            response_body = {"ok": False,
                             "reason": EXCEPTIONS.get(WRONG_JSON_FORMAT)}
        return JsonResponse(response_body, status=200)
