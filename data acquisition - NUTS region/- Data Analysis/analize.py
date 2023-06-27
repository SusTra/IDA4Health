import pandas as pd
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd


# Load the three CSV files
df1 = pd.read_csv('input.csv', encoding="utf-8", sep=";")
df2 = pd.read_csv('control_1.csv', encoding="utf-8", sep=";")
df3 = pd.read_csv('output.csv', encoding="utf-8", sep=";")

dfs = [df1, df2, df3]
for i, df in enumerate(dfs, start=1):
    new_columns = [f'{(str(i) + " - ") if (col != "NUTS Region") else ("") }{col}' for col in df.columns]
    df.columns = new_columns

# join together by the NUTS region, keep also the rows that have some data missing
df = pd.merge(df1, df2, on='NUTS Region', how='outer')
df = pd.merge(df, df3, on='NUTS Region', how='outer')

# Reset the index of the combined dataframe
df = df.reset_index(drop=True)

# Create the GUI window
window = tk.Tk()
window.title("Correlation Analysis")
window.geometry("600x600")

# Variable selection labels
input_label = tk.Label(window, text="Select Input Variable:")
input_label.pack()

output_label = tk.Label(window, text="Select Output Variable:")
output_label.pack()

control_label = tk.Label(window, text="Select Control Variables:")
control_label.pack()

print(df.columns[df.columns.str.startswith("1 - ")])

# Variable selection comboboxes
input_combo = ttk.Combobox(window, state="readonly", width=50)
input_combo['values'] = [column for column in df.columns[df.columns.str.startswith("1 - ")]]
input_combo.pack()

output_combo = ttk.Combobox(window, state="readonly", width=50)
output_combo['values'] =  [column for column in df.columns[df.columns.str.startswith("3 - ")]]
output_combo.pack()

control_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE, width=50)
control_listbox.pack()

control_scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL)
control_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

control_listbox.config(yscrollcommand=control_scrollbar.set)
control_scrollbar.config(command=control_listbox.yview)

for column in df.columns[df.columns.str.startswith("2 - ")]:
    control_listbox.insert(tk.END, column)

# Calculate button event
def calculate_correlation(df):
    input_variables = [input_combo.get()]
    output_variables = [output_combo.get()]
    control_variables = [control_listbox.get(column) for column in control_listbox.curselection()]

    print(input_variables, output_variables, control_variables)

    if not input_variables or not output_variables or not control_variables:
        messagebox.showerror("Error", "Please select all variables.")
        return
    
    df = df.dropna(subset=input_variables + control_variables + output_variables)

    # ouput the number of rows
    print(f"Number of rows: {len(df)}")

    # Calculate partial correlations for death rate and pollution level
    partial_corr = pg.partial_corr(data=df, x=input_variables[0], y=output_variables[0], covar=control_variables, method='pearson')['r'][0]
    print(f"Partial correlation between death_rate and pollution_level controlling for {control_variables}: ", partial_corr)

    # Visualize the data, only the input and output
    sns.pairplot(df, x_vars=input_variables, y_vars=output_variables, height=5, aspect=1, kind='reg')
    
    # beneath the plot, write the partial correlation
    plt.figtext(0.5, 0.01, f"Partial correlation between {input_variables[0]} and {output_variables[0]} controlling for {control_variables}: {partial_corr}", wrap=True, horizontalalignment='center', fontsize=12)

    plt.show()

# Calculate button event
def calculate_button_click():
    calculate_correlation(df)

# Calculate button
calculate_button = tk.Button(window, text="Calculate", command=calculate_button_click)
calculate_button.pack()

# Start the GUI event loop
window.mainloop()

