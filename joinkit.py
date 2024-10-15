import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import os

def browse_file1():
    filepath = filedialog.askopenfilename(filetypes=[("Text and CSV files", "*.csv *.txt *.tsv")])
    if filepath:
        entry_file1.delete(0, tk.END)
        entry_file1.insert(0, filepath)
        preview_file(filepath, tree_file1)

def browse_file2():
    filepath = filedialog.askopenfilename(filetypes=[("Text and CSV files", "*.csv *.txt *.tsv")])
    if filepath:
        entry_file2.delete(0, tk.END)
        entry_file2.insert(0, filepath)
        preview_file(filepath, tree_file2)

def preview_file(filepath, treeview):
    """Loads the first 5 rows of the file into the Treeview table for preview."""
    try:
        # Clear previous data
        treeview.delete(*treeview.get_children())

        # Read file based on extension
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath, nrows=5)
        elif filepath.endswith('.tsv'):
            df = pd.read_csv(filepath, sep='\t', nrows=5)
        else:
            df = pd.read_table(filepath, nrows=5)

        # Set columns
        treeview["columns"] = list(df.columns)
        treeview["show"] = "headings"

        # Create column headers
        for col in df.columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100)

        # Insert rows into the table
        for _, row in df.iterrows():
            treeview.insert("", "end", values=list(row))
    except Exception as e:
        messagebox.showerror("Error", f"Could not preview file: {e}")

def join_files():
    file1_path = entry_file1.get()
    file2_path = entry_file2.get()
    
    if not os.path.isfile(file1_path) or not os.path.isfile(file2_path):
        messagebox.showerror("Error", "Both files must be valid")
        return

    try:
        # Read the full files based on the extension
        if file1_path.endswith('.csv'):
            df1 = pd.read_csv(file1_path)
        elif file1_path.endswith('.tsv'):
            df1 = pd.read_csv(file1_path, sep='\t')
        else:
            df1 = pd.read_table(file1_path)

        if file2_path.endswith('.csv'):
            df2 = pd.read_csv(file2_path)
        elif file2_path.endswith('.tsv'):
            df2 = pd.read_csv(file2_path, sep='\t')
        else:
            df2 = pd.read_table(file2_path)

        # Ask for the column to be used for joining
        column_file1 = simpledialog.askstring("Input", "Enter the column name for File 1 to use as identifier:", parent=root)
        column_file2 = simpledialog.askstring("Input", "Enter the column name for File 2 to use as identifier:", parent=root)
        
        if not column_file1 or not column_file2:
            messagebox.showerror("Error", "You must specify a valid column name for both files.")
            return

        if column_file1 not in df1.columns:
            messagebox.showerror("Error", f"Column '{column_file1}' not found in File 1")
            return

        if column_file2 not in df2.columns:
            messagebox.showerror("Error", f"Column '{column_file2}' not found in File 2")
            return

        # Merging the files
        join_type = combo_join_type.get()
        if join_type == "Inner":
            result_df = pd.merge(df1, df2, how='inner', left_on=column_file1, right_on=column_file2)
        elif join_type == "Outer":
            result_df = pd.merge(df1, df2, how='outer', left_on=column_file1, right_on=column_file2)
        elif join_type == "Left":
            result_df = pd.merge(df1, df2, how='left', left_on=column_file1, right_on=column_file2)
        elif join_type == "Right":
            result_df = pd.merge(df1, df2, how='right', left_on=column_file1, right_on=column_file2)
        else:
            messagebox.showerror("Error", "Invalid join type selected.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV file", "*.csv"), ("Text file", "*.txt"), ("TSV file", "*.tsv")])
        if save_path:
            result_df.to_csv(save_path, index=False)
            messagebox.showinfo("Success", f"Files merged and saved to: {save_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the GUI application
root = tk.Tk()
root.title("File Joiner")

# File 1
label_file1 = tk.Label(root, text="Select first file:")
label_file1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_file1 = tk.Entry(root, width=50)
entry_file1.grid(row=0, column=1, padx=10, pady=5)
button_browse1 = tk.Button(root, text="Browse", command=browse_file1)
button_browse1.grid(row=0, column=2, padx=10, pady=5)

# File 2
label_file2 = tk.Label(root, text="Select second file:")
label_file2.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_file2 = tk.Entry(root, width=50)
entry_file2.grid(row=1, column=1, padx=10, pady=5)
button_browse2 = tk.Button(root, text="Browse", command=browse_file2)
button_browse2.grid(row=1, column=2, padx=10, pady=5)

# Preview File 1
label_preview1 = tk.Label(root, text="Preview File 1:")
label_preview1.grid(row=2, column=0, padx=10, pady=5, sticky="e")
tree_file1 = ttk.Treeview(root, height=5)
tree_file1.grid(row=2, column=1, padx=10, pady=5, columnspan=2, sticky="nsew")

# Preview File 2
label_preview2 = tk.Label(root, text="Preview File 2:")
label_preview2.grid(row=3, column=0, padx=10, pady=5, sticky="e")
tree_file2 = ttk.Treeview(root, height=5)
tree_file2.grid(row=3, column=1, padx=10, pady=5, columnspan=2, sticky="nsew")

# Join Type
label_join_type = tk.Label(root, text="Select join type:")
label_join_type.grid(row=4, column=0, padx=10, pady=5, sticky="e")
combo_join_type = ttk.Combobox(root, values=["Inner", "Outer", "Left", "Right"], state="readonly")
combo_join_type.grid(row=4, column=1, padx=10, pady=5)
combo_join_type.current(0)

# Join Button
button_join = tk.Button(root, text="Join Files", command=join_files)
button_join.grid(row=5, column=1, padx=10, pady=20)

# Set resizing
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Start the GUI loop
root.mainloop()
