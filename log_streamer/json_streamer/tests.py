# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.test import TestCase, Client
from django.http import JsonResponse

from utils import generate_test_jsonl

# Create your tests here.


class RequestTestCase(TestCase):
    def setUp(self):
        generate_test_jsonl()
        self.client = Client()

    def test_failure_empty_request(self):
        response = self.client.post(
            '/read_log', {}, content_type="application/json; charset=utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             b'{"ok": false, "reason": "offset not supplied"}')

    def test_failure_incorrect_offset(self):
        response = self.client.post(
            '/read_log', json.dumps({"offset": "sfsdfsf"}), content_type="application/json; charset=utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             b'{"ok": false, "reason": "incorrect offset format"}')

    def test_success_request(self):
        response = self.client.post(
            '/read_log', json.dumps({"offset": 0}), content_type="application/json; charset=utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, b'''{
            "ok": true, 
            "next_offset": 191,
            "total_size": 191,
            "messages": [
                {"level": "DEBUG", "message": "Blah blah blah"},
                {"level": "INFO", "message": "Everything is fine!"},
                {"level": "WARN","message": "Hmmm, wait..."},
                {"level": "ERROR","message": "Holly $@#t!"}
            ]}''')


    def test_failure_file_not_found(self):
        os.remove(os.environ.get("LOG_FILE_PATH"))
        response = self.client.post(
            '/read_log', json.dumps({"offset": 20}), content_type="application/json; charset=utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             b'{"ok": false, "reason": "file not found"}')