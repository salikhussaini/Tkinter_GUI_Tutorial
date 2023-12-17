# Python Tutorial: Scrollbar and Listbox

In this example:
- `listbox.curselection()` retrieves the index of the selected item.
- `listbox.get(index)` gets the value of the selected item.
- The button triggers the `show_selection` function, printing the selected item to the console.
- implement scrollable widgets using the Scrollbar
- work with the Listbox widget in Python using Tkinter.
  
## Step 1: Implementing a Scrollbar

Let's start by creating a simple window with a scrollable widget. We'll use the Scrollbar and Listbox widgets.

```python
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Listbox Tutorial")

# Create a Listbox
listbox = tk.Listbox(root, height=5)
listbox.pack(side=tk.LEFT, fill=tk.Y)

# Create a Scrollbar
scrollbar = tk.Scrollbar(root, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the Listbox to use the Scrollbar
listbox.config(yscrollcommand=scrollbar.set)

# Add items to the Listbox
for i in range(1, 21):
    listbox.insert(tk.END, f"Item {i}")

# Start the main loop
root.mainloop()
```

In this example:
- `tk.Listbox` creates a Listbox widget.
- `tk.Scrollbar` creates a vertical Scrollbar widget.
- We configure the Listbox to use the Scrollbar for vertical scrolling.

## Step 2: Working with Listbox Selection

Let's modify the code to interact with the selected items in the Listbox. We'll add a button to show the selected item when clicked.

```python
import tkinter as tk

def show_selection():
    selected_item = listbox.get(listbox.curselection())
    print(f"Selected Item: {selected_item}")

# Create the main window
root = tk.Tk()
root.title("Listbox Tutorial")

# Create a Listbox
listbox = tk.Listbox(root, height=5)
listbox.pack(side=tk.LEFT, fill=tk.Y)

# Create a Scrollbar
scrollbar = tk.Scrollbar(root, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the Listbox to use the Scrollbar
listbox.config(yscrollcommand=scrollbar.set)

# Add items to the Listbox
for i in range(1, 21):
    listbox.insert(tk.END, f"Item {i}")

# Create a button to show the selected item
show_button = tk.Button(root, text="Show Selection", command=show_selection)
show_button.pack()

# Start the main loop
root.mainloop()
```
