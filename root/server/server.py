import os
import asyncio
import websockets
import json
import logging
from game_logic import Game

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get port from environment variable or default to 8765
PORT = int(os.environ.get("PORT", 8765))
HOST = "0.0.0.0"

clients = {}
game = Game()

async def handler(websocket, path):
    global game
    player = None
    try:
        player = "A" if len(clients) == 0 else "B"
        clients[websocket] = player
        logging.info(f"Player {player} connected.")

        await websocket.send(json.dumps({
            "type": "init",
            "player": player,
            "board": game.grid
        }))

        
        async for message in websocket:
            data = json.loads(message)
            logging.info(f"Received message from Player {player}: {data}")

            if data["type"] == "move":
                piece_type = data['piece']
                direction = data['direction']
                piece = f"{player}-{piece_type}"

                if game.current_player == player:
                    move_valid = game.move_piece(piece, direction)
                    winner = game.check_winner()

                    if move_valid:
                        response = json.dumps({
                            "type": "update",
                            "board": game.grid,
                            "current_player": game.current_player
                        })
                        await asyncio.wait([client.send(response) for client in clients])
                        logging.info(f"Player {player} moved {piece_type} to {direction}.")

                        if winner:
                            game_over_response = json.dumps({
                                "type": "game_over",
                                "winner": winner
                            })
                            await asyncio.wait([client.send(game_over_response) for client in clients])
                            logging.info(f"Game over! Winner: Player {winner}")
                            game.reset_game()
                    else:
                        response = json.dumps({
                            "type": "invalid_move",
                            "message": "Invalid move. Try again."
                        })
                        await websocket.send(response)
                        logging.warning(f"Player {player} attempted invalid move: {piece_type} to {direction}.")
                else:
                    response = json.dumps({
                        "type": "invalid_move",
                        "message": "It's not your turn."
                    })
                    await websocket.send(response)
                    logging.warning(f"Player {player} attempted to move out of turn.")
    except websockets.exceptions.ConnectionClosed as e:
        logging.info(f"Player {player} disconnected.")
    finally:
        if websocket in clients:
            del clients[websocket]
        
        if not clients:
            game.reset_game()
            logging.info("All players disconnected. Game reset.")

async def main():
    async with websockets.serve(handler, HOST, PORT):
        logging.info(f"Server started on {HOST}:{PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped manually.")
