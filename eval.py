import streamlit as st

def evaluate_guess(guess, target):
    # Initialize all letters as 'absent' (gray)
    result = ["absent"] * len(guess)
    target_counts = {}
    
    for char in target:
        target_counts[char] = target_counts.get(char, 0) + 1
        
    # First pass: Check for exact matches (green)
    for i, char in enumerate(guess):
        if char == target[i]:
            result[i] = "correct"
            target_counts[char] -= 1
            
    # Second pass: Check for misplaced letters (yellow)
    for i, char in enumerate(guess):
        if result[i] == "absent" and target_counts.get(char, 0) > 0:
            result[i] = "present"
            target_counts[char] -= 1
            
    return result

def apply_custom_css():
    st.markdown("""
    <style>
    .wordle-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        margin-bottom: 20px;
    }
    .wordle-row {
        display: flex;
        gap: 5px;
    }
    .wordle-box {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
        border: 2px solid #d3d6da;
        color: black;
    }
    .correct { background-color: #6aaa64; color: white; border-color: #6aaa64; }
    .present { background-color: #c9b458; color: white; border-color: #c9b458; }
    .absent { background-color: #787c7e; color: white; border-color: #787c7e; }
    </style>
    """, unsafe_allow_html=True)