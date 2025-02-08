import random
import tkinter as tk
from tkinter import messagebox

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
        "Set to Full House": 7
    }
    draw_type, outs = random.choice(list(draw_types.items()))
    
    win_percent = outs * (4 if street == "Flop" else 2)  # Adjust equity based on street
    required_equity = round((bet_size / (pot_size + bet_size + bet_size)) * 100, 1)
    correct_decision = "Call" if win_percent >= required_equity else "Fold"
    
    return {
        "Street": street,
        "Pot Size": pot_size,
        "Opponent Bet": bet_size,
        "Pot To You": bet_size + pot_size,
        "Total Pot After Call": total_pot,
        "Draw Type": draw_type,
        "Outs": outs,
        "Win %": win_percent,
        "Required Win %": required_equity,
        "Correct Decision": correct_decision
    }

def display_problem():
    def next_problem():
        root.destroy()
        display_problem()
    
    def end_program():
        root.destroy()
    problem = generate_poker_problem()
    
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", end_program)
    root.title("Poker Decision Trainer")
    
    problem_text = f"""
    You are on the {problem['Street']}:
    - Pot Size: ${problem['Pot Size']}
    - Opponent Bets: ${problem['Opponent Bet']}
    - The Pot To You Is: ${problem['Pot To You']}
    - Your Hand: {problem['Draw Type']}
    
    👉 Do you call or fold?
    """
    
    label = tk.Label(root, text=problem_text, justify="left")
    label.pack()
    
    def show_outs():
        messagebox.showinfo("Hint", f"Number of Outs: {problem['Outs']}")
    
    def show_win_percent():
        messagebox.showinfo("Hint", f"Win %: {problem['Win %']}%")
    
    def show_required_equity():
        messagebox.showinfo("Hint", f"Required Equity to Call: {problem['Required Win %']}%")
    
    def check_decision(decision):
        result_text = f"You chose: {decision}\n"
        # result_text += f"Correct Decision: {problem['Correct Decision']}\n"
        result_text += f"Number of Outs: {problem['Outs']}\n"
        result_text += f"Win %: {problem['Win %']}%\n"
        result_text += f"Required Equity: {problem['Required Win %']}%\n"
        
        if decision == problem['Correct Decision']:
            result_text = "✅ Correct!  " + result_text 
        else:
            result_text = "❌ Wrong!  " + result_text
        
        messagebox.showinfo("Result", result_text)
        # if decision == problem['Correct Decision']:
        #     messagebox.showinfo("Result", f"✅ Correct! {decision} was the right move.")
        # else:
        #     messagebox.showinfo("Result", f"❌ Wrong! The correct move was {problem['Correct Decision']}")
    
    btn_outs = tk.Button(root, text="Show Number of Outs", command=show_outs)
    btn_outs.pack()
    
    btn_win_percent = tk.Button(root, text="Show Win %", command=show_win_percent)
    btn_win_percent.pack()
    
    btn_equity = tk.Button(root, text="Show Required Equity", command=show_required_equity)
    btn_equity.pack()
    
    btn_call = tk.Button(root, text="Call", command=lambda: check_decision("Call"))
    btn_call.pack()
    
    btn_fold = tk.Button(root, text="Fold", command=lambda: check_decision("Fold"))
    btn_fold.pack()
    
    btn_next = tk.Button(root, text="Next Problem", command=next_problem)
    btn_next.pack()
    
    btn_end = tk.Button(root, text="End", command=end_program)
    btn_end.pack()
    
    root.mainloop()

display_problem()
