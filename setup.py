import streamlit as st
import random
import sys
from unidecode import unidecode

st.set_page_config(page_title="Kelmo", page_icon="🔤")

@st.cache_data
def load_dictionary(full_filepath="dictionnaire.txt", common_filepath="mots_courants.txt"):
    try:
        with open(full_filepath, "r", encoding="utf-8") as ff:
            all_valid_words = ff.read().splitlines()

        with open(common_filepath, "r", encoding="utf-8") as cf:
            common_words = cf.read().splitlines()

        return all_valid_words, common_words
    except FileNotFoundError:
        st.error("Les fichiers dictionnaire sont introuvables.")
        return [], []

words, common_words = load_dictionary()

def get_requested_length():
    for arg in sys.argv[1:]:
        if arg.startswith('-') and arg[1:].isdigit():
            length = int(arg[1:])
            if 5 <= length <= 11:
                return length
    return None

def initialize_session():
    if 'target_word' not in st.session_state:
        requested_length = get_requested_length()
        
        # Filtre selon la taille demandée dans le pool de mots COURANTS
        if requested_length:
            valid_targets = [w for w in common_words if len(w) == requested_length]
        else:
            valid_targets = common_words
            
        st.session_state.target_word = random.choice(valid_targets) if valid_targets else ""
        
    if 'guesses' not in st.session_state:
        st.session_state.guesses = []
    if 'max_attempts' not in st.session_state:
        st.session_state.max_attempts = 7
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

initialize_session()