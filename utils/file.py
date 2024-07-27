import os
import random

def find_random_index_html(root_directory):
    index_files = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == "index.html":
                index_files.append(os.path.join(dirpath, filename))
    if not index_files:
        return None
    return random.choice(index_files)

def get_opening_name(file, lines):
    if not os.path.exists(file):
        return 'Unnamed Opening'
    for line in lines:
        match_string = 'Opening name:'
        if match_string in line:
            opening_name = line.split("</b>")[0].split("<b>")[1].replace("Opening name: ", "")
            if opening_name == 'Unnamed':
                opening_name = 'Unnamed Opening'
            return opening_name
    return 'Unnamed Opening'

def opening_line_to_filename(opening_line):
    filename = ''
    i = 0
    movenum = 1
    for move in opening_line.split(" "):
        if move == '':
            continue
        if move[0].isnumeric():
            movenum = int(move.replace(".", ""))
        else:
            i += 1
            if i % 2 == 0:
                filename += str(movenum) + "..." + move + "\\"
                movenum += 1
            elif i % 2 == 1:
                filename += str(movenum) + "._" + move + "\\"
    filename += "index.html"
    return filename

def sanitize_wiki_filename(filename):
    return filename.replace("+", "").replace("?", "").replace("!", "").replace("#", "")

def read_file_lines(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='unicode_escape') as myfile:
            return myfile.readlines()
    return []

def resolve_opening_name(opening_name, lines, wiki_filename):
    if opening_name in ('Unnamed Opening', 'Unnamed', ''):
        match_str = '<span class="mw-headline"'
        for line in lines:
            if match_str in line:
                opening_name = line.split(match_str)[1].split(">")[1].split("<")[0]
                break
    if opening_name in ('', 'Unnamed', 'Unnamed Opening'):
        new_filename = wiki_filename.replace("/index.html", "")
        done = False
        while not done:
            if "._" not in new_filename:
                done = True
                break
            if opening_name not in ('', 'Unnamed', 'Unnamed Opening'):
                break
            last_slash_index = new_filename.rfind('/')
            if last_slash_index != -1:
                new_filename = new_filename[:last_slash_index]
            else:
                new_filename = new_filename
                done = True
            new_filename += '/index.html'
            opening_name = get_opening_name(new_filename, read_file_lines(new_filename))
    return opening_name