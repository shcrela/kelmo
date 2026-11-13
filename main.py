import streamlit as st
from setup import words, initialize_session
from eval import evaluate_guess, apply_custom_css
from unidecode import unidecode

# Ensure session is initialized before accessing it
initialize_session()

# Apply the custom styles
apply_custom_css()

if not words:
    st.stop()

target_word = st.session_state.target_word
word_length = len(target_word)

st.write(f"Devinez le mot de {word_length} lettres. Il vous reste {st.session_state.max_attempts - len(st.session_state.guesses)} essais sur {st.session_state.max_attempts}.")

# Render the game grid
st.markdown('<div class="wordle-container">', unsafe_allow_html=True)

# Render past guesses
for guess in st.session_state.guesses:
    evaluation = evaluate_guess(guess, target_word)
    row_html = '<div class="wordle-row">'
    for i, char in enumerate(guess):
        row_html += f'<div class="wordle-box {evaluation[i]}">{char}</div>'
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)

# Render empty rows for remaining attempts
remaining_attempts = st.session_state.max_attempts - len(st.session_state.guesses)
for _ in range(remaining_attempts):
    row_html = '<div class="wordle-row">'
    for i in range(word_length):
        # Display the first letter as a hint in the first column
        if i == 0:
            row_html += f'<div class="wordle-box">{target_word[0]}</div>'
        else:
            row_html += f'<div class="wordle-box"></div>'
    row_html += '</div>'
    st.markdown(row_html, unsafe_allow_html=True)
    
st.markdown('</div>', unsafe_allow_html=True)

# Input field and game logic
if not st.session_state.game_over:
    with st.form("guess_form", clear_on_submit=True):
        user_guess = st.text_input("Entrez votre mot :", max_chars=word_length).lower()
        user_guess = unidecode(user_guess)
        submit_button = st.form_submit_button("Valider")

        if submit_button:
            if len(user_guess) != word_length:
                st.warning(f"Le mot doit contenir exactement {word_length} lettres.")
            elif user_guess not in words:
                st.warning("Ce mot n'est pas dans le dictionnaire.")
            else:
                st.session_state.guesses.append(user_guess)
                
                if user_guess == target_word:
                    st.session_state.game_over = True
                elif len(st.session_state.guesses) >= st.session_state.max_attempts:
                    st.session_state.game_over = True
                    
                st.rerun()

# Restart mechanism and Game Over UI
if st.session_state.game_over:
    # Check if the last guess was the winning word
    last_guess = st.session_state.guesses[-1] if st.session_state.guesses else ""
    
    if last_guess == target_word:
        attempts_used = len(st.session_state.guesses)
        
        if attempts_used <= 2:
            stars = "⭐⭐⭐"
        elif attempts_used <= 4:
            stars = "⭐⭐"
        else:
            stars = "⭐"
        
        st.balloons()
        
        st.markdown(f"""
            <style>
            @keyframes star-bounce {{
                0% {{ transform: scale(0); opacity: 0; }}
                50% {{ transform: scale(1.5); opacity: 1; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
            .stars-container {{
                text-align: center;
                font-size: 60px;
                animation: star-bounce 1s ease-out;
                margin: 10px 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            </style>
            <div class="stars-container">{stars}</div>
        """, unsafe_allow_html=True)
        
        st.success(f"Félicitations ! Vous avez trouvé le mot en {attempts_used} essai(s).")
    else:
        st.error(f"Perdu ! Le mot était : {target_word.upper()}")

    if st.button("Nouvelle Partie", key="restart_game_btn"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        initialize_session()
        st.rerun()