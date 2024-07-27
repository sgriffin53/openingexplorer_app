import chess

def filename_to_uci_line(filename):
    filename = filename.replace('chessopeningtheory_formatted\\', '')
    filename = filename.replace('/home/jimmyrustles/mysite/chessopeningtheory_formatted/', '')
    filename = filename.replace('https://en.wikibooks.org/wiki/Chess_Opening_Theory/', '')
    filename = filename.replace('\\index.html', '')
    filename = filename.replace('/index.html', '')
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
        move = move.replace("%3F", "")
        move = move.replace("!", "").replace("+", "").replace("?", "").replace("#", "")
        move = move.replace("_", "")
        uci_move = str(board.parse_san(move))
        if outstring != '':
            outstring += '_'
        outstring += uci_move
        board.push_san(move)
    return outstring

def update_board(move_list):
    board = chess.Board()
    new_move_list = []
    san_move_list = []

    for move in move_list.split("_"):
        if len(move) == 4:
            uci_move = chess.Move.from_uci(move)
            if uci_move in board.legal_moves:
                san_move_list.append(board.san(uci_move))
                board.push(uci_move)
                new_move_list.append(move)

    return board, "_".join(new_move_list), " ".join(san_move_list)

def update_full_move_list(full_move_list):
    new_full_move_list = []
    board = chess.Board()

    for move in full_move_list.split("_"):
        if len(move) == 4:
            uci_move = chess.Move.from_uci(move)
            if uci_move in board.legal_moves:
                board.push(uci_move)
                new_full_move_list.append(move)

    return "_".join(new_full_move_list)