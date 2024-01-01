import requests
import tempfile
import os
import re


def parse_lua_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as lua_file:
        lines = lua_file.readlines()

    # Define regex pattern for function definitions
    function_pattern = re.compile(r'function\s(\w+)([.:]\w+\(.*?\))')

    functions = []

    for line in lines:
        function_match = function_pattern.search(line)
        if function_match:  # Found a function definition
            function_name = function_match.group(1) + function_match.group(2)
            functions.append(function_name)

    return functions

def update_from_url(url):
    response = requests.get(url)

    # Get the temp directory path
    temp_dir = tempfile.gettempdir()

    # Create a full file path
    file_path = os.path.join(temp_dir, "downloaded_file.lua")

    with open(file_path, "wb") as file:
        file.write(response.content)

    lines = parse_lua_file(file_path)

    return lines