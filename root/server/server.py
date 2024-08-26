import asyncio
import websockets
import json
from game_logic import Game
import os

clients = {}
game = Game()

async def handler(websocket, path):
    global game
    try:
        player = "A" if len(clients) == 0 else "B"
        clients[websocket] = player
        
        await websocket.send(json.dumps({"type": "init", "player": player, "board": game.grid}))

        async for message in websocket:
            data = json.loads(message)

            if data["type"] == "move":
                piece = f"{player}-{data['piece']}"
                direction = data['direction']

                if game.current_player == player:
                    move_valid = game.move_piece(piece, direction)
                    winner = game.check_winner()

                    for client in clients:
                        if move_valid:
                            await client.send(json.dumps({
                                "type": "update",
                                "board": game.grid,
                                "current_player": game.current_player
                            }))
                        else:
                            await client.send(json.dumps({
                                "type": "invalid_move",
                                "message": "Invalid move. Try again."
                            }))

                    if winner:
                        for client in clients:
                            await client.send(json.dumps({
                                "type": "game_over",
                                "winner": winner
                            }))
                        break
                else:
                    await websocket.send(json.dumps({
                        "type": "invalid_move",
                        "message": "It's not your turn."
                    }))
    finally:
        del clients[websocket]

# Creating a new event loop and setting it as the current event loop
async def main():
    # Use os.getenv to fetch the PORT environment variable; default to 8765 if not set
    port = int(os.environ.get("PORT", 8765)) 
    start_server = websockets.serve(handler, "0.0.0.0", port)
    await start_server

if __name__ == "__main__":
    asyncio.run(main())
