import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def read_members(filename):
    df = pd.read_csv(filename)
    active_patreon = df[df['Patron Status'] == 'Active patron']

    mostly_informed = active_patreon[active_patreon['Tier'] == 'Mostly Informed']
    slightly_informed = active_patreon[active_patreon['Tier'] == 'Slightly Informed']
    slightly_recent = slightly_informed.sort_values(by='Patronage Since Date', ascending=False)
    top_15_slightly = slightly_recent.head(15)

    coffee_informed = active_patreon[active_patreon['Tier'] == 'Coffee donor']
    coffee_recent = coffee_informed.sort_values(by='Patronage Since Date', ascending=False)
    top_10_coffee = coffee_recent.head(10)

    return {
        "10 most recent Coffee patrons": top_10_coffee['Name'].tolist(),
        "15 most recent Slightly Informed patrons": top_15_slightly['Name'].tolist(),
        "All of Mostly Informed patrons": mostly_informed['Name'].tolist()
    }

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    try:
        global current_result
        current_result = read_members(file_path)
        output_text.delete(1.0, tk.END)
        for section, names in current_result.items():
            output_text.insert(tk.END, f"{section}:\n")
            for name in names:
                output_text.insert(tk.END, f"  {name}\n")
            output_text.insert(tk.END, "\n")
        save_button.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_to_text():
    if not current_result:
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for section, names in current_result.items():
                f.write(f"{section}:\n")
                for name in names:
                    f.write(f"  {name}\n")
                f.write("\n")
        messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI setup ---
root = tk.Tk()
root.title("Patreon Member Viewer")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

choose_button = tk.Button(frame, text="Choose CSV File", command=choose_file)
choose_button.pack(pady=(0, 10))

output_text = scrolledtext.ScrolledText(frame, width=60, height=25)
output_text.pack()

save_button = tk.Button(frame, text="Download as Text File", command=save_to_text, state=tk.DISABLED)
save_button.pack(pady=(10, 0))

current_result = {}  # Global storage of processed results

root.mainloop()
