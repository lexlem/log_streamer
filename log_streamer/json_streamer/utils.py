import json
import os
import random


def generate_test_jsonl(filename="logs.jsonl"):
    levels = ["DEBUG", "INFO", "WARN", "ERROR"]
    messages = [
        "Blah blah blah", "Everything is fine!", "Hmmm, wait...", "Holly $@#t!"
    ]
    with open(filename, "w") as result:
        for index in range(4):
            json.dump({"level": levels[index],
                       "message": messages[index]}, result)
            result.write('\n')


def file_lines_count(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def read_file_by_chunks(filename, offset=0):
    piece_size = 8192  # 8 Kilobytes
    with open(filename, "rb") as in_file:
        if offset:
            in_file.seek(offset)
        piece = in_file.read(piece_size)
        # TODO Add fallback in case message in piece is not finished
        closing_piece_position = piece.rfind(b'}') + 1
        result = piece[:closing_piece_position]
        next_offset = offset + closing_piece_position + 1 # We need to skip next \n char
        return result, next_offset
