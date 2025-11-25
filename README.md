# 🎲 Skyjo Score Tracker

A complete **Skyjo** card game score tracking application built with **Python** and **Streamlit**. Track scores across 10 rounds, visualize player performance with real-time graphs, and manage your game sessions with ease!

## ✨ Features

- 🎮 **Multiple Players**: Support for 2-8 players
- 📊 **Real-time Score Graph**: Interactive cumulative score visualization using Plotly
- 📋 **Score Table**: Clean dataframe display with round-by-round scores
- 🏆 **Winner Detection**: Automatically determines the winner (lowest score)
- 💾 **Export Scores**: Download score history as CSV
- 🔄 **Game Management**: Easy game reset and new game creation
- 💿 **Auto-Save**: Game state persists in browser localStorage - survives page reloads!
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🎯 How to Use

### 1. Game Setup
- Open the **sidebar** (left side)
- Enter the **number of players** (2-8)
- Enter **player names**
- Set **number of rounds** (default: 10)
- Click **"Start Game"**

### 2. Playing the Game
- After each round of physical Skyjo gameplay, enter each player's score
- Click **"Submit Round Scores"** to record the round
- The score table and graph update automatically

### 3. Tracking Progress
- **Score Table**: Shows all round scores and cumulative totals
- **Score Graph**: Visual representation of cumulative scores over time
- **Current Standings**: Real-time leaderboard showing player rankings

### 4. Game End
- After all rounds are completed, the winner is automatically announced
- Download the score history as CSV for record-keeping
- Click **"New Game"** to start fresh

## 📖 About Skyjo

**Skyjo** is a popular card game where the objective is to have the **lowest score** possible.

### Basic Rules:
- Each player has a grid of cards (typically 12 cards in 3 rows of 4)
- Cards have values ranging from -2 to 12
- Players take turns drawing and discarding cards
- When a player reveals all their cards, the round ends
- The goal is to minimize your total card value

### Scoring:
- Each card's face value counts as points
- **Lower scores are better**
- Cumulative scores across all rounds determine the final winner

## 🛠️ Technology Stack

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and dataframe creation
- **Plotly**: Interactive data visualization
- **Python 3.8+**: Core programming language

## 📁 Project Structure

```
skyjo/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎨 Features in Detail

### Score Table
- Round-by-round score breakdown
- Highlighted total scores row
- Auto-calculated cumulative totals
- Export functionality for record-keeping

### Real-time Graph
- Line chart with markers for each round
- Different color for each player
- Hover tooltips showing exact scores
- Cumulative score progression tracking

### Game State Management
- Persistent session state during gameplay
- Safe round progression
- Validation of score entries
- Automatic winner calculation

## 🤝 Contributing

Feel free to fork this project and add your own features! Some ideas:
- Add game statistics (average score per round, best/worst rounds)
- Implement undo functionality
- Add custom scoring rules
- Create player profiles with game history
- Add animations and sound effects

## 📝 License

This project is open source and available for personal and educational use.

## 🐛 Issues & Support

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

---

**Enjoy your Skyjo games!** 🎲🎉
