import random
import streamlit as st

def generate_poker_problem():
    CARD_SUITS = ["spades", "hearts", "diamonds", "clubs"]
    CARD_RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
    
    HAND_TYPES = {
        "Flush Draw": lambda: (random.choice(CARD_SUITS), None),
        "Open-Ended Straight Draw": lambda: (None, ["5", "6", "7", "8"]),
        "Gutshot Straight Draw": lambda: (None, ["4", "5", "7", "8"]),
        "Overcards": lambda: (None, ["king", "queen"]),
        "Set to Full House": lambda: (None, ["7", "7"])
    }

    def get_suited_card(suit):
        rank = random.choice(CARD_RANKS)
        return f"{rank}_of_{suit}.png"

    def get_straight_cards(ranks):
        suit = random.choice(CARD_SUITS)
        return [f"{rank}_of_{suit}.png" for rank in ranks]
    
    hand_type, setup_func = random.choice(list(HAND_TYPES.items()))
    suit, ranks = setup_func()
    
    if suit:
        if random.choice([True, False]):  # Ensure it's actually a draw, not a made flush
            hole_cards = [get_suited_card(suit), get_suited_card(suit)]
            board = [get_suited_card(suit) for _ in range(2)] + [get_suited_card(random.choice(CARD_SUITS)), get_suited_card(random.choice(CARD_SUITS))]
        else:
            hole_cards = [get_suited_card(suit), get_suited_card(random.choice(CARD_SUITS))]
            board = [get_suited_card(suit) for _ in range(3)] + [get_suited_card(random.choice(CARD_SUITS))]
        hole_cards = [get_suited_card(suit), get_suited_card(suit)]
        board = [get_suited_card(suit) for _ in range(3)] + [get_suited_card(random.choice(CARD_SUITS))]
    elif ranks:
        hole_cards = get_straight_cards(ranks[:2])
        board = get_straight_cards(ranks[2:]) + [get_straight_cards([random.choice(CARD_RANKS)])[0]]
    
    outs = {
        "Flush Draw": 9,
        "Open-Ended Straight Draw": 8,
        "Gutshot Straight Draw": 4,
        "Overcards": 6,
        "Set to Full House": 7
    }[hand_type]
    
    pot_size = random.choice([50, 100, 150, 200, 300, 400])
    bet_size = random.choice([pot_size // 4, pot_size // 2, pot_size, pot_size * 2])
    opponent_bet = random.choice([pot_size // 4, pot_size // 2, pot_size, pot_size * 2])    
    pot_to_you = pot_size + opponent_bet

    return {
        "Street": "Flop" if len(board) == 3 else "Turn",
        "Pot Size": pot_size,
        "Opponent Bet": opponent_bet,
        "Pot To You": pot_to_you,
        "Hole Cards": hole_cards,
        "Board": board,
        "Outs": outs,
        "Win %": outs * 4 if len(board) == 3 else outs * 2,
        "Required Win %": round((opponent_bet / (pot_size + 2 * opponent_bet)) * 100, 1),
        "Correct Decision": "Call" if outs * (4 if len(board) == 3 else 2) >= (opponent_bet / (pot_size + 2 * opponent_bet)) * 100 else "Fold",
        "Current Draw": hand_type
    }

st.title("Poker Pot Odds Trainer")

if "problem" not in st.session_state:
    st.session_state.show_hints = {'outs': False, 'win': False, 'equity': False}
    st.session_state.problem = generate_poker_problem()

def new_problem():
    st.session_state.show_hints = {'outs': False, 'win': False, 'equity': False}
    st.session_state.problem = generate_poker_problem()
    st.session_state.result = None

def check_decision(decision):
    problem = st.session_state.problem
    result_text = f"You chose: {decision}\n\n"
    result_text += f"Correct Decision: {problem['Correct Decision']}\n"
    result_text += f"Win %: {problem['Win %']}%\n"
    result_text += f"Required Equity: {problem['Required Win %']}%\n"
    result_text += f"Number of Outs: {problem['Outs']}\n"
    
    if decision == problem['Correct Decision']:
        result_text = "✅ Correct!\n" + result_text 
    else:
        result_text = "❌ Wrong!\n" + result_text
    
    st.session_state.result = result_text

problem = st.session_state.problem

st.write(f"### You are on the {problem['Street']}")
st.write("### Your Hand:")
st.image([f"cards/{card}" for card in problem["Hole Cards"]], width=100)

st.write("### Board:")
st.image([f"cards/{card}" for card in problem["Board"]], width=100)

st.write(f"### Debugging: Current Draw - {problem['Current Draw']}")
st.write(f"- **Pot Size:** ${problem['Pot Size']}")
st.write(f"- **Opponent Bets:** ${problem['Opponent Bet']}")
st.write(f"- **The Pot To You Is:** ${problem['Pot To You']}")
st.write("---")

col_hint1, col_hint2, col_hint3 = st.columns(3)
with col_hint1:
    if st.button("Show/Hide Number of Outs"):
        st.session_state.show_hints['outs'] = not st.session_state.show_hints['outs']
if st.session_state.show_hints['outs']:
    st.write(f"📌 Number of Outs: {problem['Outs']}")
with col_hint2:
    if st.button("Show/Hide Win %"):
        st.session_state.show_hints['win'] = not st.session_state.show_hints['win']
if st.session_state.show_hints['win']:
    st.write(f"📌 Win %: {problem['Win %']}%")
with col_hint3:
    if st.button("Show/Hide Required Equity"):
        st.session_state.show_hints['equity'] = not st.session_state.show_hints['equity']
if st.session_state.show_hints['equity']:
    st.write(f"📌 Required Equity: {problem['Required Win %']}%")

st.write("### 👉 Do you call or fold?")

col1, col2 = st.columns(2)
with col1:
    if st.button("Call"):
        check_decision("Call")
with col2:
    if st.button("Fold"):
        check_decision("Fold")

if "result" in st.session_state and st.session_state.result:
    st.write("---")
    st.write(st.session_state.result.replace("", ""))
    st.write("---")

if st.button("Next Problem"):
    new_problem()
    st.rerun()
