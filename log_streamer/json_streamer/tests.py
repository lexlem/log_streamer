# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.test import TestCase, Client
from django.http import JsonResponse

# Create your tests here.


class RequestTestCase(TestCase):
    def setUp(self):
        pass

    def test_failure_empty_request(self):
        c = Client()
        response = c.post(
            '/read_log', {}, content_type="application/json; charset=utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             b'{"ok": false, "reason": "offset not supplied"}')

    def test_failure_file_not_found(self):
        c = Client()
        response = c.post(
            '/read_log', json.dumps({"offset": 20}), content_type="application/json; charset=utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             b'{"ok": false, "reason": "file not found"}')

    # def test_failure_wrong_encoding(self):
    #     c = Client()
    #     response = c.post('/read_log', {"offset": 0}, content_type="application/json; charset=utf-8")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(
    #         response.content, b'{"ok": false, "reason": "file should be encoded with UTF-8"}')

    def test_failure_incorrect_offset(self):
        c = Client()
        response = c.post(
            '/read_log', json.dumps({"offset": "sfsdfsf"}), content_type="application/json; charset=utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             b'{"ok": false, "reason": "incorrect offset"}')

    # def test_success_request(self):
    #     c = Client()
    #     response = c.post(
    #         '/read_log', json.dumps({"offset": 0}), content_type="application/json; charset=utf-8")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(response.content, b'''{
    #         "ok": true, 
    #         "next_offset": 100,
    #         "total_size": 1000,
    #         "messages": [
    #             {"level": "INFO", "message": "Everything is fine!"}
    #             {"level": "WARN", "message": "Hmmm, wait... It looks like..."}
    #             {"level": "ERROR","message": "Holly $@#t!"}
    #         ]}''')
