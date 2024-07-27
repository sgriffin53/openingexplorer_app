from flask import Flask, request, render_template
from utils.file import find_random_index_html, get_opening_name, opening_line_to_filename, sanitize_wiki_filename, read_file_lines, resolve_opening_name
from utils.chess import filename_to_uci_line, update_board, update_full_move_list
from footer import get_footer
import json

app = Flask(__name__)

@app.route('/chessopeningtheory')
def chessopeningtheory_page():
    # Initialize variables
    position = ''
    new_move_list = ''
    flipped_flag = 'false'

    # Check if the board should be flipped
    if request.args.get('flipped') is not None:
        flipped_flag = str(request.args.get('flipped'))

    # Check if wiki moves should be highlighted
    highlight_wiki_moves_flag = 'false'
    if request.args.get('highlight_wiki_moves') is not None:
        highlight_wiki_moves_flag = str(request.args.get('highlight_wiki_moves'))

    # Get the current move list and full move list from the request
    move_list = request.args.get('move_list', '')
    full_move_list = request.args.get('full_move_list', '')

    # If a random opening is requested, find a random index.html file
    if request.args.get("random") == "random":
        wiki_filename = find_random_index_html('/home/jimmyrustles/mysite/chessopeningtheory_formatted')
        move_list = filename_to_uci_line(wiki_filename)
        full_move_list = move_list

    # Update the full move list if necessary
    if len(move_list) > len(full_move_list) and len(move_list) > 0:
        full_move_list = move_list

    # Update the board and move lists based on the current move list
    board, new_move_list, san_move_list = update_board(move_list)
    print('board')
    print(board)
    new_full_move_list = update_full_move_list(full_move_list)

    # Get the board position in FEN notation
    position = board.fen()

    # Generate the filename for the current position's wiki page
    wiki_filename = '/home/jimmyrustles/mysite/chessopeningtheory_formatted/' + opening_line_to_filename(san_move_list).replace("\\", "/")
    wiki_filename = sanitize_wiki_filename(wiki_filename)
    
    # Read the content of the wiki file
    lines = read_file_lines(wiki_filename)

    # Get the opening name from the wiki file
    opening_name = get_opening_name(wiki_filename, lines)
    
    # Resolve the opening name if it is unnamed
    opening_name = resolve_opening_name(opening_name, lines, wiki_filename)
    
    # Get the list of legal moves
    legal_moves = json.dumps([str(move) for move in board.legal_moves])
    print(legal_moves)
    
    # Render the template with the necessary variables
    outtext = render_template(
        'chessopeningtheory.html', 
        opening_name=opening_name, 
        flipped_flag=flipped_flag,
        highlight_wiki_moves_flag=highlight_wiki_moves_flag, 
        move_list=move_list,
        full_move_list=full_move_list, 
        position=position, 
        lines=lines, 
        board=board,
        new_move_list=new_move_list, 
        san_move_list=san_move_list, 
        get_footer=get_footer,
        legal_moves=legal_moves
    )

    return outtext

if __name__ == '__main__':
    app.run(debug=True)
