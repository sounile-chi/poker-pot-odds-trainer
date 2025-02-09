import random
import streamlit as st

def generate_poker_problem():
    pot_size = random.choice([50, 100, 150, 200, 300, 400])
    bet_size = random.choice([pot_size // 4, pot_size // 2, pot_size, pot_size * 2])
    total_pot = pot_size + bet_size + bet_size
    
    street = random.choice(["Flop", "Turn"])
    draw_types = {
        "Flush Draw": 9,
        "Open-Ended Straight Draw": 8,
        "Gutshot Straight Draw": 4,
        "Overcards": 6,
        # "Set to Full House": 7  <--remove this option as it was confusing
    }
    draw_type, outs = random.choice(list(draw_types.items()))
    
    win_percent = outs * (4 if street == "Flop" else 2)  # Adjust equity based on street
    required_equity = round((bet_size / (pot_size + bet_size + bet_size)) * 100, 1)
    correct_decision = "Call" if win_percent >= required_equity else "Fold"
    
    return {
        "Street": street,
        "Pot Size": pot_size,
        "Opponent Bet": bet_size,
        "Pot To You": total_pot - bet_size,
        "Draw Type": draw_type,
        "Outs": outs,
        "Win %": win_percent,
        "Required Win %": required_equity,
        "Correct Decision": correct_decision
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
        result_text = "✅ Correct! \n" + result_text 
    else:
        result_text = "❌ Wrong! \n" + result_text
    
    st.session_state.result = result_text

problem = st.session_state.problem

st.write(f"### You are on the {problem['Street']}")
st.write(f"- **Pot Size:** ${problem['Pot Size']}")
st.write(f"- **Opponent Bets:** ${problem['Opponent Bet']}")
st.write(f"- **The Pot To You Is:** ${problem['Pot To You']}")
st.write(f"- **Your Hand:** {problem['Draw Type']}")


if 'show_hints' not in st.session_state:
    st.session_state.show_hints = {'outs': False, 'win': False, 'equity': False}

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


st.write("---")
st.write("### 👉 Do you call or fold?")

col1, col2 = st.columns(2)
with col1:
    if st.button("Call"):
        check_decision("Call")
with col2:
    if st.button("Fold"):
        check_decision("Fold")

if "result" in st.session_state and st.session_state.result:
    # st.write("---")
    st.markdown(st.session_state.result.replace("\n", "  \n"))
#     st.write("---")
#     st.write(st.session_state.result.replace("", "  "))

st.write("---")
if st.button("Next Problem"):
    new_problem()
    st.rerun()
    new_problem()
