import chess
import os
import random
from bs4 import BeautifulSoup
from footer import get_footer


def filename_to_uci_line(filename):
    #'chessopeningtheory_formatted\1._a3'
    filename = filename.replace('chessopeningtheory_formatted\\','')
    filename = filename.replace('/home/jimmyrustles/mysite/chessopeningtheory_formatted/', '')
    filename = filename.replace('https://en.wikibooks.org/wiki/Chess_Opening_Theory/','')
    filename = filename.replace('\\index.html','')
    filename = filename.replace('/index.html','')
    print(filename)
    moves = []
    if "\\" in filename:
        moves = filename.split("\\")
    else:
        moves = filename.split("/")
    board = chess.Board()
    outstring = ''
    for move in moves:
        if "..." in move:
            move = move.split("...")[1]
        elif "._" in move:
            move = move.split("._")[1]
        else:
            continue
        move = move.replace("%3F","")
        move = move.replace("!","").replace("+","").replace("?","").replace("#","")
        move = move.replace("_", "")
        uci_move = str(board.parse_san(move))
        if outstring != '': outstring += '_'
        outstring += uci_move
        board.push_san(move)
        print(move)
    return outstring

def find_random_index_html(root_directory):
    index_files = []

    # Traverse the directory tree
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == "index.html":
                # Collect the full path to the index.html file
                index_files.append(os.path.join(dirpath, filename))

    # Check if there are any index.html files found
    if not index_files:
        return None

    # Select a random index.html file
    return random.choice(index_files)

def get_opening_name(file):
    if not os.path.exists(file): return 'Unnamed Opening'
    myfile = open(file,'r',encoding='unicode_escape')
    lines = []
    try:
        lines = myfile.readlines()
    except:
        lines = []
    myfile.close()
    for line in lines:
        match_string = 'Opening name:'
        if match_string in line:
            opening_name = line.split("</b>")[0].split("<b>")[1].replace("Opening name: ","")
            if opening_name == 'Unnamed': opening_name = 'Unnamed Opening'
            #return opening_name
    if opening_name == 'Unnamed' or opening_name == 'Unnamed Opening' or opening_name == '':
        pass
    return opening_name
    return 'Unnamed Opening'

def opening_line_to_filename(opening_line):
    filename = ''
    i = 0
    movenum = 1
    for move in opening_line.split(" "):
        if move == '': continue
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

def chessopeningtheory_page(request):
    position = ''
    new_move_list = ''
    flipped_flag = 'false'
    if request.args.get('flipped') != None:
        flipped_flag = str(request.args.get('flipped'))
    highlight_wiki_moves_flag = 'false'
    if request.args.get('highlight_wiki_moves') != None:
        highlight_wiki_moves_flag = str(request.args.get('highlight_wiki_moves'))
    move_list = request.args.get('move_list')
    if move_list == None: move_list = ''
    full_move_list = request.args.get('full_move_list')
    if full_move_list == None: full_move_list = ''
    if request.args.get("random") == "random":
        wiki_filename = find_random_index_html('/home/jimmyrustles/mysite/chessopeningtheory_formatted')
        move_list = filename_to_uci_line(wiki_filename)
        full_move_list = move_list
    if len(move_list) > len(full_move_list) and len(move_list) > 0:
        full_move_list = move_list
    board = chess.Board()
    outtext = ''
    san_move_list = ''
    for move in move_list.split("_"):
   #     outtext += str(move) + ":" + str(len(move)) + "<br>"
        if len(move) != 4: continue
        if move[0] + move[1] == move[2] + move[3]: break
        if chess.Move.from_uci(move) in list(board.legal_moves):
            san_move_list += board.san(chess.Move.from_uci(move))

            board.push_uci(move)
            if new_move_list != '': new_move_list += '_'
            if san_move_list != '': san_move_list += ' '
            new_move_list += move
        else:
            break
    new_full_move_list = ''
    myboard = chess.Board()
    for move in full_move_list.split("_"):
   #     outtext += str(move) + ":" + str(len(move)) + "<br>"
        if len(move) != 4: continue
        if move[0] + move[1] == move[2] + move[3]: break
        if chess.Move.from_uci(move) in list(myboard.legal_moves):
            myboard.push_uci(move)
            if new_full_move_list != '': new_full_move_list += '_'
            new_full_move_list += move
        else:
            break
    full_move_list = new_full_move_list
    #return outtext
    move_list = str(new_move_list)
    position = board.fen()
    wiki_filename = '/home/jimmyrustles/mysite/chessopeningtheory_formatted/' + opening_line_to_filename(san_move_list).replace("\\","/")
    wiki_filename = wiki_filename.replace("+","").replace("?","").replace("!","").replace("#","")
    lines = []
    if os.path.exists(wiki_filename):
        myfile = open(wiki_filename,'r',encoding='unicode_escape')
        lines = myfile.readlines()
        myfile.close()
    opening_name = get_opening_name(wiki_filename)
    if opening_name == 'Unnamed Opening':
        match_str = '<span class="mw-headline"'
        for line in lines:
            if match_str in line:
                opening_name = line.split(match_str)[1].split(">")[1].split("<")[0]
                break
    if opening_name == '' or opening_name == 'Unnamed' or opening_name == 'Unnamed Opening':
        new_filename = wiki_filename.replace("/index.html","")
        done = False
        while not done:
            print(new_filename + ":::")
            if "._" not in new_filename:
                done = True
                break
            if opening_name != '' and opening_name != 'Unnamed' and opening_name != 'Unnamed Opening':
                break
            # Find the position of the last '/'
            new_filename = new_filename.replace("/index.html","")
            last_slash_index = new_filename.rfind('/')
            # Remove the part after the last '/'
            if last_slash_index != -1:
                new_filename = new_filename[:last_slash_index]
            else:
                new_filename = new_filename  # No '/' found, so the filename remains the same
                done = True
            new_filename += '/index.html'
            opening_name = get_opening_name(new_filename)
            if not os.path.exists(new_filename):
                continue
            myfile = open(new_filename, 'r', encoding='unicode_escape')
            new_lines = myfile.readlines()
            myfile.close()
            if opening_name == 'Unnamed Opening':
                match_str = '<span class="mw-headline"'
                for line in new_lines:
                    if match_str in line:
                        opening_name = line.split(match_str)[1].split(">")[1].split("<")[0]
    outtext = '''
        <!DOCTYPE html>
        <html>
      <head>'''
    outtext += f'<title>{opening_name} - Chess Openings Explorer</title>'
    outtext += '''
    <style>
        .container {
            justify-content: center;
            display: flex;
        }
        .left-div {
            min-height: 800px;
            position: sticky;
            top: 0;
            width: 400px;
            height: 400px;
        }
        .left-div-header {
            background-color: lightblue;
            padding-top: 1px;
            padding-bottom: 1px;
        }
        .right-div {
            min-height: 600px;
            display: inline-block;
            background-color: #f0f0f0;
            text-align: left;
            margin-left: 15px;
            width:1200px;
        }
/* General page styling */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

/* Navigation section styling */
.navigation {

}

.navigation h2 {
    margin-top: 0;
}

.navigation ul {
    list-style-type: none;
    padding: 0;
}

.navigation li {
    margin-bottom: 10px;
}

.navigation a {
    text-decoration: none;
    color: #007BFF; /* Set link color to blue */
    font-weight: bold;
}

.navigation a:hover {
    color: #0056b3; /* Set hover color to a darker blue */
}

/* Page content styling */
.content {
    padding: 20px;
}

.section {
    margin: 20px 0;
}

.section h2 {
    margin-top: 0;
}
        </style>
        <link rel="stylesheet" href="css/chessboard-1.0.0.min.css">
        <script src="https://code.jquery.com/jquery-3.5.1.min.js"
            integrity="sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/6Z/hRTt8+pR6L4N2"
            crossorigin="anonymous"></script>
        <script src="js/chessboard-1.0.0.min.js"></script>
        <script src="js/chess.ts"></script>
      </head>
      <body>
    <center><h1>Chess Opening Explorer</h1>
    A chess opening explorer tool and study guide. Play a chess opening on the board and see the related article and stats for that opening.<br><br>
    <div class="container">
    <div class="left-div"><div class="left-div-header">'''
    wiki_html = ''
    for line in lines:
        line = line.replace("<!--","").replace("--!>","")
        if 'Lichess board:' in line:
            link = line.split('href="')[1].split('"')[0]
            line = f'<br><b><a href="{link}">Lichess Board</a></b>'
        if 'Wikibooks page:' in line:
            link = line.split('href="')[1].split('"')[0]
            line = f'<br><b><a href="{link}">Wikibooks Page</a></b>'
        wiki_html += line.replace("Opening name: Unnamed", "Opening name: " + opening_name).replace("Opening name: </b>", "Opening name: " + opening_name + "</b>")
    wiki_html = wiki_html.replace("percenatages:", "percentages")
    outtext += '<h2>' + opening_name + '</h2></div>'
    outtext += '''<div class="board-div" id="myBoard" onmouseleave="mouseoutBoard()"></div>'''
    outtext += '<input type="button" style="width:100px" onclick="backToStart()" value="<<">'
    outtext += '<input type="button" style="width:100px" onclick="backOne()" value="<">'
    outtext += '<input type="button" style="width:100px" onclick="forwardOne()" value=">">'
    outtext += '<input type="button" style="width:100px" onclick="forwardAll()" value=">>"><br>'
    outtext += '<input type="checkbox" name="highlight_wiki_check" onclick="clickHWcheckbox()" id="highlight_wiki_check"'
    if highlight_wiki_moves_flag == 'true': outtext += ' checked'
    outtext += '><label for="highlight_wiki_check">Highlight Wiki Moves</label><br>'
    outtext += '<input type="checkbox" name="flip_board_check" onclick="clickFBcheckbox()" id="flip_board_check"'''
    if flipped_flag == 'true': outtext += ' checked'
    outtext += '><label for="flip_board_check">Flip Board (Black\'s perspective)</label><br>'
    outtext += '<a href="/chessopeningtheory?random=random">Random Page</a><br>'
    outtext += '<a href="/chessopeningtheory">Restart</a><br><br>'
    soup = BeautifulSoup(wiki_html, 'html5lib')
    for span_tag in soup.find_all('span'):
        if 'mw-headline' in str(span_tag):
            span_tag['id'] = 'Main_Page'
            break
    page_sections = []
    for span_tag in soup.find_all('span'):
        if 'mw-headline' in str(span_tag):
            if 'Main_Page' in span_tag['id']: continue
            page_sections.append((span_tag['id'], span_tag.string))
    outtext += '''
        <div class="navigation">
        <h2>Page Navigation</h2>
        <ul>
            <li><a href="#wiki_text">Top</a></li>
            <li><a href="#Winning_percentages">Winning Percentages</a></li>
            <li><a href="#Main_Page">'''
    outtext += opening_name
    outtext += ''' (Main Article)</a></li>'''
    i = 0
    for section in page_sections:
        tag_id = section[0]
        tag_string = section[1]
        outtext += '<li>* <a href="#' + tag_id + '">' + tag_string + '</a></li>'
        i += 1
        if i > 3: break
    outtext += '''
            <li><a href="#Most_popular_responses">Most Popular Responses</a></li>
            <li><a href="#Engine_Evaluation">Engine Evaluation</a></li>
            <li><a href="#Historical_games">Historical Games</a></li>
        </ul>
    </div>
    '''
    outtext += '<a href="/">Back to Main Site</a><br><br>'
    outtext += '''</div>
    <div class="right-div" id="wiki_text">'''
    # parse <a> tags
    # Parse the HTML content
    # Find all <a> tags and replace their content

    for a_tag in soup.find_all('a'):
        #a_tag['href'] = "test"
        href = a_tag['href']
        #'https://en.wikibooks.org/w/index.php?title=Chess_Opening_Theory/1._e4/1...d5/2._c3&action=edit&redlink=1
        href = href.replace('https://en.wikibooks.org/w/index.php?title=Chess_Opening_Theory/', 'https://en.wikibooks.org/wiki/Chess_Opening_Theory/')
        href = href.replace('/w/index.php?title=Chess_Opening_Theory/', 'https://en.wikibooks.org/wiki/Chess_Opening_Theory/')
        if 'https://en.wikibooks.org/wiki/Chess_Opening_Theory/' in href:
            colour = 'green'
            if 'action=edit' in href or 'Conventions for organization.' in a_tag.string:
                colour = 'red'
                href = href.replace('&action=edit&redlink=1','')
            line = filename_to_uci_line(href)
            if 'Wikibooks' in a_tag.string: continue
            a_tag['href'] = '/chessopeningtheory?move_list=' + line + '&full_move_list=' + line
            a_tag['style'] = 'color: ' + colour

            pass
        pass

    for b_tag in soup.find_all('b'):
        match_sections = ['Winning percentages', 'Most popular responses', 'Engine Evaluation', 'Historical games']
        for match in match_sections:
            if b_tag is None: continue
            if b_tag.string is None: continue
            if match in b_tag.string:
                orig_b_string = b_tag.string
                new_id = orig_b_string.replace(" ","_")
                if 'Historical_games' in new_id: new_id = 'Historical_games'
                b_tag['id'] = new_id

    # add <a> tags to moves in popular responses

    modified_html = str(soup)
    in_section = False
    for line in modified_html.split("<br/>"):
        #outtext += line
        if "Most popular responses" in line:
            in_section = True
            continue
        if in_section:
            if "<hr/>" in line:
                in_section = False
            if "<li>" in line: line = line.split("<li>")[1]
            line = line.strip()
            #outtext += line + "<br><br>"
            move = ''
            to_replace = ''
            uci_move = ''
            if '...' in line.split(" ")[0]:
                move = line.split("...")[1].split(" ")[0]
                uci_move = str(board.parse_san(move))
                to_replace = line.split(" ")[0]
            elif "." in line.split(" ")[0]:
                move = line.split(" ")[1]
                uci_move = str(board.parse_san(move))
                to_replace = line.split(" ")[0] + " " + line.split(" ")[1]
            new_move_list = move_list
            if new_move_list != '': new_move_list += '_'
            new_move_list = new_move_list + uci_move
            url = f'/chessopeningtheory?move_list={new_move_list}&full_move_list={new_move_list}'
            new_string = f'<a href="{url}" style="color: green">{to_replace}</a>'
            if 'lichess' in line:
                first_part = line.split('<a href="https://lichess.org')[0]
                second_part = '<a href="https://lichess.org' + line.split('<a href="https://lichess.org')[1]
                new_line = first_part.replace(to_replace, new_string)
                modified_html = modified_html.replace(first_part, new_line)
    #outtext += line
    outtext += modified_html
    #outtext += wiki_html
    outtext += '''</div>
    </div>
    <form action="/chessopeningtheory" id="my_form" method="GET">
    <input type="hidden" name="flipped" id="flipped" value="'''
    outtext += str(flipped_flag)
    outtext += '''">
    <input type="hidden" name="highlight_wiki_moves" id="highlight_wiki_moves" value="'''
    outtext += str(highlight_wiki_moves_flag)
    outtext += '''">
    <input type="hidden" id="move_list" name="move_list" value="'''
    new_full_move_list = ''
    ml_split = move_list.split("_")
    fml_split = full_move_list.split("_")
    for i, move in enumerate(fml_split):
        if i + 1 <= len(ml_split):
            if move != ml_split[i]:
                break
        if new_full_move_list != '': new_full_move_list += '_'
        new_full_move_list += move
    if move_list != '': full_move_list = new_full_move_list
    outtext += move_list
    outtext += '''"><input type="hidden" id="full_move_list" name="full_move_list" value ="'''
    outtext += full_move_list
    outtext += '''">
    <input type="submit" id="submit_button" hidden="hidden">
    </form>
    <script>

    var whiteSquareGrey = '#a9a9a9'
    var blackSquareGrey = '#696969'
    var whiteSquareGreen = '#00d900'
    var blackSquareGreen = '#009900'
    '''
    wiki_moves = []
    #wiki_files = []
    for move in board.legal_moves:
        san = str(board.san(move))
        wiki_dir = '/home/jimmyrustles/mysite/chessopeningtheory_formatted/'
        wiki_path = opening_line_to_filename(san_move_list).replace("\\","/").replace("/index.html","").replace("index.html","")
        halfmove_num = wiki_path.count("/")
        movenum = int(((wiki_path.count("/") - 1) / 2) + 2)
        dotstring = '._'
        if halfmove_num % 2 == 0:
            dotstring = '...'
        if wiki_path == '':
            movenum = 1
            dotstring = '._'
        wiki_filename = wiki_dir + wiki_path + "/" + str(movenum) + dotstring + san
        full_wiki_filename = wiki_filename + '/index.html'
        #full_wiki_filename += ":::" + str(os.path.exists(full_wiki_filename)) + "::"
        outtext += '// ' + full_wiki_filename + ':' + str(halfmove_num) + '::' + str(os.path.exists(full_wiki_filename)) + '\n'
        if os.path.exists(full_wiki_filename):
            wiki_moves.append(str(move))
     #   wiki_files.append(full_wiki_filename)
    #wiki_files_str = str(wiki_files)
    wiki_moves_str = str(wiki_moves)
    outtext += f'''
    wiki_moves = {wiki_moves};'''
    outtext += '''
    function removeGreySquares () {
        $('#myBoard .square-55d63').css('background', '')
    }

    function greySquare (square) {
        var $square = $('#myBoard .square-' + square);
        var background = whiteSquareGrey;
        if ($square.hasClass('black-3c85d')) {;
            background = blackSquareGrey;
        };

        $square.css('background', background);
    }
    function greenSquare (square) {
        var $square = $('#myBoard .square-' + square);
        var background = whiteSquareGreen;
        if ($square.hasClass('black-3c85d')) {;
            background = blackSquareGreen;
        };
        $square.css('background', background);
    }
    function highlightWikiMoves() {
        for (var i = 0; i < wiki_moves.length; i++) {
            greenSquare(wiki_moves[i][2] + wiki_moves[i][3]);
            greySquare(wiki_moves[i][0] + wiki_moves[i][1]);
        }
    }
    function onMouseoverSquare (square, piece) {
        //alert(square);
        // highlight the square they moused over
        legal_moves = '''
    legal_moves = []
    for move in board.legal_moves:
        legal_moves.append(str(move))
    outtext += str(legal_moves) + ';'
    # highlight legal moves
    outtext += '''
        for (var i = 0; i < legal_moves.length; i++) {
            if (legal_moves[i][0] == square[0] && legal_moves[i][1] == square[1]) {
                greySquare(legal_moves[i][2] + legal_moves[i][3]);
                greySquare(square);
            }
        }
    '''
    outtext += '''
        for (var i = 0; i < wiki_moves.length; i++) {
            if (wiki_moves[i][0] == square[0] && wiki_moves[i][1] == square[1]) {
                greenSquare(wiki_moves[i][2] + wiki_moves[i][3]);
                //greySquare(square);
            }
        }
        wiki_move = false
        for (var i = 0;i < wiki_moves.length;i++) {
            if (wiki_moves[i][0] + wiki_moves[i][1] == square) wiki_move = true;
        }
        if (wiki_move == false && document.getElementById("highlight_wiki_check").checked.toString() == 'true') highlightWikiMoves();
    }
    function onMouseoutSquare (square, piece) {
        removeGreySquares();

    }
    function mouseoutBoard() {
        if (document.getElementById("highlight_wiki_check").checked.toString() == 'true') highlightWikiMoves();
    }
    function backToStart() {
        document.getElementById("move_list").value = '';
        document.getElementById("my_form").submit();
    }
    function backOne() {
    '''
    new_move_list = move_list.split("_")
    new_move_list.pop()
    new_move_list = '_'.join(new_move_list)
    if move_list != '':
        outtext += f'''
        document.getElementById("move_list").value = '{new_move_list}';
        document.getElementById("my_form").submit();
        '''
    outtext += '''
    }
    function clickFBcheckbox() {
    '''
    outtext += '''
        document.getElementById("flipped").value = document.getElementById("flip_board_check").checked.toString();
        document.getElementById("my_form").submit();'''
    outtext += '''
    }
    function clickHWcheckbox() {
    '''
    outtext += '''
        document.getElementById("highlight_wiki_moves").value = document.getElementById("highlight_wiki_check").checked.toString();
        document.getElementById("my_form").submit();'''
    outtext += '''
    }
    function forwardOne() {
    '''
    if len(full_move_list) > len(move_list):
        replaced_move_list = full_move_list
        if move_list != '': replaced_move_list = full_move_list.replace(move_list + "_", "")
        next_move = replaced_move_list.split("_")[0]
        new_move_list = move_list
        if move_list != '': new_move_list += '_'
        new_move_list += next_move
        outtext += f'''document.getElementById("move_list").value = '{new_move_list}';
        document.getElementById("my_form").submit();'''
    outtext += '''
    }
    function forwardAll() {
    '''
    outtext += f'''document.getElementById("move_list").value = '{full_move_list}';
        document.getElementById("my_form").submit();'''
    outtext += '''
    }
    function onDrop (source, target, piece, newPos, oldPos, orientation) {
                    if (document.getElementById("move_list").value != "") document.getElementById("move_list").value += "_"
                    document.getElementById("move_list").value += source + target;
                    if (document.getElementById("full_move_list").value != "") document.getElementById("full_move_list").value += "_"
                    document.getElementById("full_move_list").value += source + target;
                    document.getElementById("my_form").submit();
    }
    var config = {
      draggable: true,
      position: \''''
    if move_list == '': outtext += 'start'
    else: outtext += position
    outtext += '''\',
    onDrop: onDrop,
    onMouseoverSquare: onMouseoverSquare,
    onMouseoutSquare: onMouseoutSquare,
    orientation: '''
    if flipped_flag == 'false':
        outtext += '\'white\''
    else:
        outtext += '\'black\''
    outtext += '''
    }
    board = Chessboard('myBoard', config)
    if (document.getElementById("highlight_wiki_check").checked.toString() == 'true') highlightWikiMoves()
    </script>'''
    outtext += get_footer().replace("<hr>","")
    outtext += '''
    </body>
    </html>
    '''
    return outtext