import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import pickle
import base64
from urllib.parse import urlencode

# Page configuration
st.set_page_config(
    page_title="Skyjo Score Tracker",
    page_icon="🎲",
    layout="wide"
)

# Helper functions for state persistence
def encode_state(state_dict):
    """Encode state dictionary to base64 string"""
    json_str = json.dumps(state_dict)
    return base64.urlsafe_b64encode(json_str.encode()).decode()

def decode_state(encoded_str):
    """Decode base64 string to state dictionary"""
    try:
        json_str = base64.urlsafe_b64decode(encoded_str.encode()).decode()
        return json.loads(json_str)
    except:
        return None

# Initialize session state
def init_session_state():
    """Initialize session state with persistence check"""
    # Check query parameters first
    query_params = st.query_params
    
    if 'state' in query_params and 'loaded' not in st.session_state:
        # Load from query params (page reload scenario)
        loaded_state = decode_state(query_params['state'])
        if loaded_state:
            st.session_state.game_started = loaded_state.get('game_started', False)
            st.session_state.players = loaded_state.get('players', [])
            st.session_state.scores = loaded_state.get('scores', {})
            st.session_state.current_round = loaded_state.get('current_round', 1)
            st.session_state.max_rounds = loaded_state.get('max_rounds', 10)
            st.session_state.game_finished = loaded_state.get('game_finished', False)
            st.session_state.loaded = True
            return
    
    # Initialize defaults if not loaded
    defaults = {
        'game_started': False,
        'players': [],
        'scores': {},
        'current_round': 1,
        'max_rounds': 10,
        'game_finished': False,
        'loaded': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

def save_state_to_url():
    """Save game state to URL query parameters"""
    game_state = {
        'game_started': st.session_state.game_started,
        'players': st.session_state.players,
        'scores': st.session_state.scores,
        'current_round': st.session_state.current_round,
        'max_rounds': st.session_state.max_rounds,
        'game_finished': st.session_state.game_finished
    }
    
    encoded = encode_state(game_state)
    st.query_params.update({"state": encoded})

def initialize_game(players, max_rounds):
    """Initialize a new game with players"""
    st.session_state.players = players
    st.session_state.max_rounds = max_rounds
    st.session_state.current_round = 1
    st.session_state.game_finished = False
    st.session_state.scores = {player: [] for player in players}
    st.session_state.game_started = True
    save_state_to_url()

def add_round_scores(round_scores):
    """Add scores for the current round"""
    for player, score in round_scores.items():
        st.session_state.scores[player].append(score)
    st.session_state.current_round += 1
    
    # Check if game is finished
    if st.session_state.current_round > st.session_state.max_rounds:
        st.session_state.game_finished = True
    
    save_state_to_url()

def reset_game():
    """Reset the game"""
    st.session_state.game_started = False
    st.session_state.players = []
    st.session_state.scores = {}
    st.session_state.current_round = 1
    st.session_state.game_finished = False
    
    # Clear query params
    st.query_params.clear()

def copy_to_clipboard(text):
    """Copy text to clipboard using JavaScript"""
    st.components.v1.html(
        f"""
        <script>
            navigator.clipboard.writeText('{text}').then(function() {{
                console.log('Copied to clipboard successfully!');
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        </script>
        """,
        height=0,
    )

def create_score_graph():
    """Create real-time score graph using Plotly"""
    if not st.session_state.scores or not any(st.session_state.scores.values()):
        return None
    
    fig = go.Figure()
    
    # Add a line for each player
    for player in st.session_state.players:
        scores = st.session_state.scores[player]
        if scores:
            rounds = list(range(1, len(scores) + 1))
            cumulative_scores = [sum(scores[:i+1]) for i in range(len(scores))]
            
            fig.add_trace(go.Scatter(
                x=rounds,
                y=cumulative_scores,
                mode='lines+markers',
                name=player,
                line=dict(width=3),
                marker=dict(size=8)
            ))
    
    fig.update_layout(
        title={
            'text': '📊 Cumulative Score Progress',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#1f77b4'}
        },
        xaxis_title='Round',
        yaxis_title='Cumulative Score',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(dtick=1)
    
    return fig

def create_scores_dataframe():
    """Create a pandas DataFrame with all scores"""
    if not st.session_state.scores or not any(st.session_state.scores.values()):
        return None
    
    # Prepare data for DataFrame
    data = {}
    max_rounds_played = max(len(scores) for scores in st.session_state.scores.values())
    
    for player in st.session_state.players:
        scores = st.session_state.scores[player]
        # Pad with empty strings if needed
        padded_scores = scores + [''] * (max_rounds_played - len(scores))
        data[player] = padded_scores
    
    df = pd.DataFrame(data)
    df.index = [f'Round {i+1}' for i in range(len(df))]
    
    # Add cumulative totals row
    cumulative = {}
    for player in st.session_state.players:
        scores = st.session_state.scores[player]
        cumulative[player] = sum(scores) if scores else ''
    
    cumulative_df = pd.DataFrame([cumulative], index=['Total Score'])
    df = pd.concat([df, cumulative_df])
    
    return df

def get_winner():
    """Determine the winner (lowest total score)"""
    if not st.session_state.game_finished:
        return None
    
    totals = {player: sum(scores) for player, scores in st.session_state.scores.items()}
    winner = min(totals, key=totals.get)
    return winner, totals[winner]

# Main App UI
st.title("🎲 Skyjo Score Tracker")
st.markdown("---")

# Sidebar for game setup
with st.sidebar:
    st.header("⚙️ Game Setup")
    
    if not st.session_state.game_started:
        st.subheader("New Game")
        
        # Number of players
        num_players = st.number_input(
            "Number of Players",
            min_value=2,
            max_value=8,
            value=4,
            step=1
        )
        
        # Player names
        player_names = []
        for i in range(num_players):
            name = st.text_input(
                f"Player {i+1} Name",
                value=f"Player {i+1}",
                key=f"player_{i}"
            )
            player_names.append(name)
        
        # Number of rounds
        max_rounds = st.number_input(
            "Number of Rounds",
            min_value=1,
            max_value=20,
            value=10,
            step=1
        )
        
        if st.button("🎮 Start Game", type="primary", width="stretch"):
            initialize_game(player_names, max_rounds)
            st.rerun()
    
    else:
        st.success("✅ Game in Progress")
        st.metric("Current Round", f"{st.session_state.current_round} / {st.session_state.max_rounds}")
        
        if st.button("🔄 New Game", type="secondary", width="stretch"):
            reset_game()
            st.rerun()
        
        st.markdown("---")
        st.subheader("📋 Players")
        for i, player in enumerate(st.session_state.players, 1):
            st.text(f"{i}. {player}")
        
        # Share match button
        st.markdown("---")
        st.subheader("🔗 Share Match")
        
        # Get current URL with state
        current_state = st.query_params.get("state", None)
        if current_state:
            # Construct full shareable URL
            import urllib.parse
            base_url = "http://skyjoo.streamlit.app"  # Change this to your deployed URL
            share_url = f"{base_url}/?state={current_state}"
            
            st.text_area(
                "Share this link:",
                value=share_url,
                height=80,
                help="Copy and send this link to transfer scoring to another device",
                key="share_url_display"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy Link", key="copy_btn", width="stretch"):
                    copy_to_clipboard(share_url)
                    st.success("✅ Copied to clipboard!")
            with col2:
                # WhatsApp share button
                whatsapp_text = urllib.parse.quote(f"Join my Skyjo game! Round {st.session_state.current_round}/{st.session_state.max_rounds}\n{share_url}")
                whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
                st.link_button("💬 WhatsApp", whatsapp_url, width="stretch")
            
            st.caption("💡 **Battery low?** Share this link to continue on another device!")

# Main content area
if not st.session_state.game_started:
    st.info("👈 Configure the game settings in the sidebar and click 'Start Game' to begin!")
    
    # Game rules
    with st.expander("📖 How to Play Skyjo"):
        st.markdown("""
        ### Skyjo Rules (Simplified)
        
        **Objective:** Have the lowest score after all rounds.
        
        **Gameplay:**
        - Each round, players aim to get the lowest possible score
        - At the end of each round, enter each player's score
        - Scores are cumulative across all rounds
        - After 10 rounds (or your chosen number), the player with the lowest total score wins!
        
        **Scoring:**
        - Lower scores are better
        - Each card has a point value (typically -2 to 12)
        - Try to get rid of high-value cards and keep low-value cards
        """)

else:
    if st.session_state.game_finished:
        # Game Over - Show Winner
        st.balloons()
        winner, winning_score = get_winner()
        st.success(f"🏆 Game Over! **{winner}** wins with a total score of **{winning_score}** points!")
        
    elif st.session_state.current_round <= st.session_state.max_rounds:
        # Score Entry Form
        st.subheader(f"🎯 Round {st.session_state.current_round} Score Entry")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form(key="score_entry_form"):
                st.write("Enter scores for each player:")
                
                round_scores = {}
                cols = st.columns(len(st.session_state.players))
                
                for idx, player in enumerate(st.session_state.players):
                    with cols[idx]:
                        score = st.number_input(
                            player,
                            min_value=-50,
                            max_value=150,
                            value=0,
                            step=1,
                            key=f"score_{player}_{st.session_state.current_round}"
                        )
                        round_scores[player] = score
                
                submit_button = st.form_submit_button("✅ Submit Round Scores", type="primary", width="stretch")
                
                if submit_button:
                    add_round_scores(round_scores)
                    st.success(f"Round {st.session_state.current_round - 1} scores recorded!")
                    st.rerun()
        
        with col2:
            st.info(f"**Rounds Remaining:** {st.session_state.max_rounds - st.session_state.current_round + 1}")
            
            # Show current standings
            if any(st.session_state.scores.values()):
                st.subheader("📊 Current Standings")
                standings = []
                for player in st.session_state.players:
                    total = sum(st.session_state.scores[player])
                    standings.append((player, total))
                
                standings.sort(key=lambda x: x[1])
                
                for rank, (player, total) in enumerate(standings, 1):
                    emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "📍"
                    st.metric(f"{emoji} {player}", f"{total} pts")
    
    # Score Table
    st.markdown("---")
    st.subheader("📋 Score Table")
    
    df = create_scores_dataframe()
    if df is not None:
        # Style the dataframe
        def highlight_totals(s):
            return ['background-color: #e1f5ff; font-weight: bold' if s.name == 'Total Score' else '' for _ in s]
        
        styled_df = df.style.apply(highlight_totals, axis=1)
        st.dataframe(styled_df, width='stretch', height=400)
        
        # Download button
        csv = df.to_csv()
        st.download_button(
            label="📥 Download Scores as CSV",
            data=csv,
            file_name=f"skyjo_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No scores recorded yet. Start entering scores for each round!")
    
    # Real-time Score Graph
    st.markdown("---")
    fig = create_score_graph()
    if fig is not None:
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Score graph will appear after the first round is recorded.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Made with ❤️ using Streamlit | 🎲 Skyjo Score Tracker | by <a href='https://github.com/sbeving' target='_blank'>Saleh Eddine Touil</a>"
    "</div>",
    unsafe_allow_html=True
)
