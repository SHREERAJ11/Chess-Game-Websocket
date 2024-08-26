# Chess-Game-Websocket

### A Turn-based Chess-like Game with Websocket Communication

This project is a basic implementation of a turn-based chess-like game using Python, WebSockets, HTML, CSS, and JavaScript. The game allows two players to connect to the server and take turns moving pieces on a grid-based board. The project demonstrates the use of WebSocket communication between the client and server to manage real-time gameplay.

## Features

- **Two-Player Game:** Supports two players (Player A and Player B) connected via WebSocket.
- **Real-Time Updates:** Game state is updated in real-time for both players.
- **Basic Move Validation:** Ensures players make valid moves according to the game logic.
- **Winner Detection:** Automatically detects and announces the winner.

## Technologies Used

- **Backend:**
  - Python
  - WebSockets
  - asyncio
  
- **Frontend:**
  - HTML
  - CSS
  - JavaScript

## Project Structure

The project is organized as follows:

```plaintext
root/
│
├── .gitignore            # Python template
├── README.md             # Project documentation
│
├── server/
│   ├── game_logic.py     # Game logic for handling moves and determining the winner
│   ├── server.py         # WebSocket server code
│   ├── requirements.txt  # Dependencies
│   ├── Procfile          # Render-specific process file
│
└── client/
    ├── client.html       # Frontend HTML file
    ├── styles.css        # Frontend CSS file
    └── client.js         # Frontend JavaScript file
```

## How to Run Locally

- **Prerequisites**

    Python 3.11.x
    Web browser

- **Installation**

  - Clone the repository:

        git clone https://github.com/SHREERAJ11/Chess-Game-Websocket.git
        cd Chess-Game-Websocket

  - Install the dependencies:

        pip install -r root/server/requirements.txt

  - Run the WebSocket server:

        python root/server/server.py

  - Open `client/client.html` in your web browser. Connect two tabs to simulate two players.

## Deployment

The project is deployed on Vercel. You can view and play the game live at:

[Game URL](https://chess-game-websocket-fthy4lwge-shreeraj11s-projects.vercel.app)



### Deployment Steps

   - Ensure the code is correctly pushed to your GitHub repository.

   - Connect your repository to Render.

   - Set the build command to:
     
          pip install -r root/server/requirements.txt

   - Set the start command to:

          python root/server/server.py

   - Deploy and wait for the process to complete.

## Contact

For any inquiries, feel free to reach out via Email or connect with me on [LinkedIn](https://www.linkedin.com/in/sobhan-shreeraj/).
