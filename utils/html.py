from bs4 import BeautifulSoup

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
            opening_name = get_opening_name(new_filename)
            if not os.path.exists(new_filename):
                continue
            with open(new_filename, 'r', encoding='unicode_escape') as myfile:
                new_lines = myfile.readlines()
            if opening_name == 'Unnamed Opening':
                match_str = '<span class="mw-headline"'
                for line in new_lines:
                    if match_str in line:
                        opening_name = line.split(match_str)[1].split(">")[1].split("<")[0]
    return opening_name
