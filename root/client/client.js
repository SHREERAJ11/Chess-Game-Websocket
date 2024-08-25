// Dynamically set WebSocket URL based on the environment
const ws = new WebSocket(`ws://${window.location.host}`);

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "init") {
        initializeBoard(message.board);
        document.getElementById("status").innerText = `Current Player: ${message.player}`;
    } else if (message.type === "update") {
        updateBoard(message.board);
        document.getElementById("status").innerText = `Current Player: ${message.current_player}`;
    } else if (message.type === "invalid_move") {
        alert(message.message);
    } else if (message.type === "game_over") {
        alert(`Game over! Winner: ${message.winner}`);
    }
};

function initializeBoard(board) {
    const boardElement = document.getElementById("board");
    boardElement.innerHTML = '';
    board.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            const cellElement = document.createElement("div");
            cellElement.classList.add("cell");
            if (cell) {
                cellElement.innerText = cell;
                cellElement.classList.add(cell[0]); // Add a class based on the player (A or B)
            }
            cellElement.onclick = () => selectPiece(rowIndex, colIndex);
            boardElement.appendChild(cellElement);
        });
    });
}

function updateBoard(board) {
    const boardElement = document.getElementById("board");
    board.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            const cellElement = boardElement.children[rowIndex * 5 + colIndex];
            cellElement.innerText = cell;
            cellElement.className = "cell";
            if (cell) {
                cellElement.classList.add(cell[0]); // Update class based on the player (A or B)
            }
        });
    });
}

let selectedPiece = null;

function selectPiece(row, col) {
    if (!selectedPiece) {
        selectedPiece = { row, col };
        document.getElementById("controls").innerHTML = generateMoveButtons(row, col);
    } else {
        selectedPiece = null;
        document.getElementById("controls").innerHTML = '';
    }
}

function generateMoveButtons(row, col) {
    const piece = document.getElementById("board").children[row * 5 + col].innerText;
    const pieceType = piece.split("-")[1];

    let buttons = '';

    const directions = {
        "P": ["L", "R", "F", "B"],
        "H1": ["L", "R", "F", "B"],
        "H2": ["FL", "FR", "BL", "BR"]
    };

    directions[pieceType].forEach(direction => {
        buttons += `<button onclick="movePiece('${piece}', '${direction}')">${direction}</button>`;
    });

    return buttons;
}

function movePiece(piece, direction) {
    const move = { type: "move", piece, direction };
    ws.send(JSON.stringify(move));
}
