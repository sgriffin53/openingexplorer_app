/* chess.js */
var whiteSquareGrey = '#a9a9a9';
var blackSquareGrey = '#696969';
var whiteSquareGreen = '#00d900';
var blackSquareGreen = '#009900';

function removeGreySquares() {
    $('#myBoard .square-55d63').css('background', '');
}

function greySquare(square) {
    var $square = $('#myBoard .square-' + square);
    var background = whiteSquareGrey;
    if ($square.hasClass('black-3c85d')) {
        background = blackSquareGrey;
    }
    $square.css('background', background);
}

function greenSquare(square) {
    var $square = $('#myBoard .square-' + square);
    var background = whiteSquareGreen;
    if ($square.hasClass('black-3c85d')) {
        background = blackSquareGreen;
    }
    $square.css('background', background);
}

function highlightWikiMoves() {
    for (var i = 0; i < wiki_moves.length; i++) {
        greenSquare(wiki_moves[i][2] + wiki_moves[i][3]);
        greySquare(wiki_moves[i][0] + wiki_moves[i][1]);
    }
}

function onMouseoverSquare(square, piece) {
    legal_moves = [];
    for (var i = 0; i < legal_moves.length; i++) {
        if (legal_moves[i][0] == square[0] && legal_moves[i][1] == square[1]) {
            greySquare(legal_moves[i][2] + legal_moves[i][3]);
            greySquare(square);
        }
    }
    for (var i = 0; i < wiki_moves.length; i++) {
        if (wiki_moves[i][0] == square[0] && wiki_moves[i][1] == square[1]) {
            greenSquare(wiki_moves[i][2] + wiki_moves[i][3]);
        }
    }
    wiki_move = false;
    for (var i = 0; i < wiki_moves.length; i++) {
        if (wiki_moves[i][0] + wiki_moves[i][1] == square) wiki_move = true;
    }
    if (wiki_move == false && document.getElementById("highlight_wiki_check").checked.toString() == 'true') highlightWikiMoves();
}

function onMouseoutSquare(square, piece) {
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
    document.getElementById("move_list").value = '{{ new_move_list }}';
    document.getElementById("my_form").submit();
}

function clickFBcheckbox() {
    document.getElementById("flipped").value = document.getElementById("flip_board_check").checked.toString();
    document.getElementById("my_form").submit();
}

function clickHWcheckbox() {
    document.getElementById("highlight_wiki_moves").value = document.getElementById("highlight_wiki_check").checked.toString();
    document.getElementById("my_form").submit();
}

function forwardOne() {
    document.getElementById("move_list").value = '{{ new_move_list_forward }}';
    document.getElementById("my_form").submit();
}

function forwardAll() {
    document.getElementById("move_list").value = '{{ full_move_list }}';
    document.getElementById("my_form").submit();
}

function onDrop(source, target, piece, newPos, oldPos, orientation) {
    if (document.getElementById("move_list").value != "") document.getElementById("move_list").value += "_";
    document.getElementById("move_list").value += source + target;
    if (document.getElementById("full_move_list").value != "") document.getElementById("full_move_list").value += "_";
    document.getElementById("full_move_list").value += source + target;
    document.getElementById("my_form").submit();
}

var config = {
    draggable: true,
    position: '{{ position }}',
    onDrop: onDrop,
    onMouseoverSquare: onMouseoverSquare,
    onMouseoutSquare: onMouseoutSquare,
    orientation: '{{ orientation }}'
};
board = ChessBoard('myBoard', config);
if (document.getElementById("highlight_wiki_check").checked.toString() == 'true') highlightWikiMoves();
