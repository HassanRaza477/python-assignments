# Import necessary packages
import streamlit as st
import random

# Configure page settings
st.set_page_config(
    page_title="Guess the Secret Number!",
    page_icon="🔢",
    layout="centered"
)

# Initialize game state variables
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = None
if 'attempt_count' not in st.session_state:
    st.session_state.attempt_count = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = True

def start_new_game():
    """Reset all settings for a fresh game session"""
    # Get user-selected number range
    min_val = st.session_state.user_min
    max_val = st.session_state.user_max
    
    # Auto-correct if user reverses min/max
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    
    # Generate new mystery number
    st.session_state.secret_number = random.randint(min_val, max_val)
    
    # Reset game counters
    st.session_state.attempt_count = 0
    st.session_state.game_over = False
    
    # Set attempt limits based on difficulty
    difficulty_settings = {
        'Easy': None,
        'Medium': 15,
        'Hard': 7
    }
    st.session_state.max_attempts = difficulty_settings[st.session_state.difficulty_level]

def check_guess(player_guess):
    """Validate player's guess and provide feedback"""
    st.session_state.attempt_count += 1
    
    if player_guess == st.session_state.secret_number:
        st.session_state.game_over = True
        st.success(f"🎉 Correct! You found the number in {st.session_state.attempt_count} tries!")
        st.balloons()
    else:
        # Provide directional feedback
        if player_guess < st.session_state.secret_number:
            st.warning("📈 too low")
        else:
            st.warning("📉 too higher")
        
        # Check attempt limit
        if st.session_state.max_attempts and st.session_state.attempt_count >= st.session_state.max_attempts:
            st.session_state.game_over = True
            st.error(f"😢 Out of attempts! The secret number was {st.session_state.secret_number}")

# Game settings sidebar
with st.sidebar:
    st.header("⚙️ Game Configuration")
    
    # Number range selection
    st.subheader("Choose Number Range")
    col1, col2 = st.columns(2)
    with col1:
        min_number = st.number_input("Minimum Number", value=1, key='user_min')
    with col2:
        max_number = st.number_input("Maximum Number", value=100, key='user_max')
    
    # Difficulty level
    difficulty = st.selectbox(
        "Select Challenge Level",
        options=['Easy', 'Medium', 'Hard'],
        index=0,
        key='difficulty_level'
    )
    
    # New game button
    if st.button(" Start New Game", use_container_width=True):
        start_new_game()

# Main game interface
st.title("🔍 Number Detective")

if not st.session_state.game_over:
    # Active game display
    st.subheader(f"💡 Guess between {min_number} and {max_number}")
    
    # Guess input
    current_guess = st.number_input(
        "Enter your guess:",
        min_value=min_number,
        max_value=max_number,
        key="current_guess"
    )
    
    # Guess submission button
    if st.button(" Check Guess", type="primary", use_container_width=True):
        check_guess(current_guess)
        
else:
    # Game over screen
    st.subheader("Game Complete!")
    if st.session_state.secret_number is not None:
        st.markdown(f"**Secret Number:** 🎯 `{st.session_state.secret_number}`")
    
    if st.button("🎲 Play Again", type="primary", use_container_width=True):
        start_new_game()
        st.rerun()

# Attempt counter display
if st.session_state.max_attempts:
    attempt_text = f"Attempts: {st.session_state.attempt_count}/{st.session_state.max_attempts}"
else:
    attempt_text = f"Attempts: {st.session_state.attempt_count} (Unlimited)"
st.caption(f"📊 {attempt_text}")

# Help section
with st.expander("❓ How to Play"):
    st.markdown("""
    **Simple Rules:**
    1. Choose your settings in the sidebar
    2. Click "Start New Game"
    3. Enter numbers and check your guesses
    4. Use feedback to adjust your next guess
    5. Find the number in fewest tries!
    
    **Difficulty Levels:**
    - 🟢 Easy: No attempt limit
    - 🟠 Medium: 15 attempts
    - 🔴 Hard: Only 7 tries
    """)

# Footer
st.markdown("---")
st.caption("Ready to test your guessing skills? Play now and share your score with friends! 🏆")