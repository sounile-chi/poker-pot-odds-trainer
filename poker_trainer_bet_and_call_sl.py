import random
import streamlit as st

def generate_poker_problem(push_threshold):
    pot_size = random.randint(100, 500)  # Any number between 100 and 500
    bet_size = random.choice([pot_size // 4, pot_size // 2, pot_size // 2, pot_size * 2// 3, pot_size // 3, pot_size*3//2])
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
    

    if abs(win_percent - required_equity) <= push_threshold:
        correct_decision = "Push"
    elif win_percent > required_equity + push_threshold:
        correct_decision = "Call"
    else:
        correct_decision = "Fold"


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

def generate_bet_sizing_problem():
    HAND_TYPES = {
        "Flush Draw": 9,
        "Open-Ended Straight Draw": 8,
        # "Gutshot Straight Draw": 4,  #you basically never call with gutshot alone so remove from tool
        "Overcards": 6
    }
    opponent_hand, opponent_outs = random.choice(list(HAND_TYPES.items()))
    
    pot_size = random.randint(100, 500)  # Any number between 100 and 500
    street = random.choice(["Flop", "Turn"])
    opponent_win_percentage = opponent_outs * 4 if street == "Flop" else opponent_outs * 2
    required_equity = opponent_win_percentage / 100
    min_bet = (opponent_win_percentage / 100) * pot_size / (1 - 2 * (opponent_win_percentage / 100))

    
    max_bet = pot_size * 2  # Setting max reasonable bet to 2x the pot
    
    return {
        "Street": street,
        "Pot Size": pot_size,
        "Opponent Hand": opponent_hand,
        "Opponent Outs": opponent_outs,
        "Opponent Win %": opponent_win_percentage,
        "Minimum Bet": round(min_bet, 1),
        "Max Bet": max_bet
    }

st.title("Poker Trainer")

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Call or Fold Trainer"


tab_selection = st.radio(
    "Select Trainer", 
    ["Call or Fold Trainer", "Bet Sizing Trainer"],
    index=0 if st.session_state.active_tab == "Call or Fold Trainer" else 1,
    label_visibility="visible"
)

# Store the current tab selection
st.session_state.active_tab = tab_selection

if st.session_state.active_tab == "Call or Fold Trainer":
    st.header("Call or Fold Trainer")
    
    # Slider to adjust "Push" threshold
    push_threshold = st.slider("Set 'Push' Threshold (%) if win percent and equity are close", min_value=1, max_value=5, value=3)


    if "problem" not in st.session_state:
        st.session_state.problem = generate_poker_problem(push_threshold)


    def new_call_fold_problem():
        st.session_state.show_hints = {'outs': False, 'win': False, 'equity': False}
        st.session_state.problem = generate_poker_problem(push_threshold)
        st.session_state.result = None

    def check_decision(decision):
        problem = st.session_state.problem
        correct_decision = problem["Correct Decision"]  # ✅ Get the correct decision from problem data

        result_text = f"You chose: {decision}\n\n"
        result_text += f"Correct Decision: {problem['Correct Decision']}\n"
        result_text += f"Win %: {problem['Win %']}%\n"
        result_text += f"Required Equity: {problem['Required Win %']}%\n"
        result_text += f"Number of Outs: {problem['Outs']}\n"
        
        if decision == correct_decision:
            result_text = "✅ Correct! \n" + result_text 
        elif correct_decision == "Push" and decision in ["Call", "Fold"]:
            result_text = "⚖️ Close Decision! 'Push' was the best option, but Call/Fold were reasonable."
        else:
            result_text = "❌ Wrong! \n" + result_text 
        
        st.session_state.result = result_text

    problem = st.session_state.problem



    st.write(f"### You are on the {problem['Street']}")
    st.write(f"- **Pot Size:** ${problem['Pot Size']}")
    st.write(f"- **Opponent Bets:** ${problem['Opponent Bet']}")
    # st.write(f"- **The Pot To You Is:** ${problem['Pot To You']}")
    st.write(f"- **You are Drawing With:** {problem['Draw Type']}")


    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = {'outs': False, 'win': False, 'equity': False}


    st.write("### 🔍 Hints")
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
    st.write("### 👉 Do you call or fold or is it a push?")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Call"):
            check_decision("Call")
    with col2:
        if st.button("Fold"):
            check_decision("Fold")
    with col3:
        if st.button("Push"):
            check_decision("Push")
    

    if "result" in st.session_state and st.session_state.result:
        st.write("---")
        st.markdown(st.session_state.result.replace("\n", "  \n"))

    
    if st.button("Next Problem", key="next_cf"):
        new_call_fold_problem()
        st.rerun()

elif st.session_state.active_tab == "Bet Sizing Trainer":
    st.header("Bet Sizing Trainer")
    
    # Ensure bet_problem is initialized
    if "bet_problem" not in st.session_state:
        st.session_state.bet_problem = generate_bet_sizing_problem()
    
    def new_bet_sizing_problem():
        st.session_state.bet_problem = generate_bet_sizing_problem()
        st.session_state.show_hints = {'outs': False, 'win': False, 'equity': False}
        st.session_state.bet_result = None
    
    bet_problem = st.session_state.bet_problem  # Ensure bet_problem is assigned

    
    st.write(f"### You are on the {bet_problem['Street']}, and you are in the lead")
    st.write(f"- **Pot Size:** ${bet_problem['Pot Size']}")
    st.write(f"- **Opponent's Estimated Hand:** {bet_problem['Opponent Hand']}")
    
    # Define tolerance levels in a dictionary
    tolerance_levels = {
        15: 3,  # If opponent's required equity is ≤ 15%, allow ±3%
        30: 5,  # If opponent's required equity is ≤ 30%, allow ±5%
        100: 5  
        # If opponent's required equity is > 30%, allow ±7%
    }

    # Function to determine appropriate tolerance
    def get_tolerance(equity):
        for threshold, tolerance in tolerance_levels.items():
            if equity <= threshold:
                return tolerance
        return 5  # Default fallback (should never reach this)

    # ✅ Ensure hint state exists for bet sizing
    if "show_hints_bs" not in st.session_state:
        st.session_state.show_hints_bs = {'outs': False, 'win': False}

    st.write("### 🔍 Hints")

    col_hint1, col_hint2 = st.columns(2)

    with col_hint1:
        if st.button("Show/Hide Opponent's Outs"):
            st.session_state.show_hints_bs['outs'] = not st.session_state.show_hints_bs['outs']
    if st.session_state.show_hints_bs['outs']:
        st.write(f"📌 Opponent's Outs: {bet_problem['Opponent Outs']}")

    with col_hint2:
        if st.button("Show/Hide Opponent's Win %"):
            st.session_state.show_hints_bs['win'] = not st.session_state.show_hints_bs['win']
    if st.session_state.show_hints_bs['win']:
        st.write(f"📌 Opponent's Win %: {bet_problem['Opponent Win %']}%")

    bet_input = st.number_input(
        "Enter your bet to price out the opponent:", 
        min_value=1,  # Ensure the bet is at least 1 to avoid auto-calculations at 0
        max_value=int(bet_problem['Max Bet']), 
        step=1
    )
    your_equity = round(bet_input / (bet_problem['Pot Size'] + bet_input)*100,1)
    opponent_required_equity = round(bet_input / (bet_problem['Pot Size'] + 2*bet_input)*100,1)
    
    if st.button("Submit Bet", key="submit_bet") and bet_input > 0:
        # Get the dynamic tolerance based on the opponent's required equity
        tolerance = get_tolerance(opponent_required_equity)

        # Determine the acceptable range
        min_acceptable_equity = bet_problem['Opponent Win %'] - tolerance
        max_acceptable_equity = bet_problem['Opponent Win %'] + tolerance

       # Evaluate the bet
        if min_acceptable_equity <= opponent_required_equity <= max_acceptable_equity:
            st.session_state.bet_result = f"✅ Correct! Your bet of ${bet_input} is within the allowed equity range of ±{tolerance}%."
        elif opponent_required_equity < min_acceptable_equity:
            st.session_state.bet_result = f"❌ Too low. You should aim for an opponent required equity of at least {min_acceptable_equity}%."
        else:  # opponent_required_equity > max_acceptable_equity
            st.session_state.bet_result = f"❌ Too high. You should aim for an opponent required equity no more than {max_acceptable_equity}%."

    # ✅ Only show results after submission
    if "bet_result" in st.session_state and st.session_state.bet_result:
        st.write("---")
        st.write(st.session_state.bet_result)
        st.write(f"Opponent's Outs: {bet_problem['Opponent Outs']}")
        st.write(f"Opponent's Win %: {bet_problem['Opponent Win %']}%")
        st.write(f"Your Minimum Bet To Get Them to Fold: {bet_problem['Minimum Bet']}")
        st.write(f"Opponent's Required Equity To Call Your Bet: {opponent_required_equity}%")
        st.write("---")
    
    if st.button("Next Problem", key="next_bs"):
        new_bet_sizing_problem()
        st.rerun()
