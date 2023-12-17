

# Tkinter GUI Tutorial

- Tkinter is a popular Python library for creating Graphical User Interfaces (GUIs). 
- In this tutorial, we'll create a simple Tkinter application with an Entry widget, a Button, and a Label.

- This example creates a simple application
    - with an Entry widget to take user input
    - , a Button to trigger an action
    - , and a Label to display the result.
      
## Step 1: Import Tkinter

```python
import tkinter as tk
```

## Step 2: Create the Main Window

```python
# Create the main window
root = tk.Tk()
root.title("Tkinter GUI Tutorial")
```

## Step 3: Create Widgets

```python
# Create widgets
label = tk.Label(root, text="Enter your name:")
entry = tk.Entry(root)
button = tk.Button(root, text="Greet Me!", command=on_button_click)
```

## Step 4: Define Functions

```python
# Define functions
def on_button_click():
    input_text = entry.get()
    label.config(text=f"Hello, {input_text}!")
```

## Step 5: Organize Widgets Using Grid

```python
# Use grid to organize widgets
label.grid(row=0, column=0, columnspan=2, pady=10)
entry.grid(row=1, column=0, columnspan=2, pady=5)
button.grid(row=2, column=0, columnspan=2, pady=10)
```

## Step 6: Start the Main Loop

```python
# Start the main loop
root.mainloop()
```


