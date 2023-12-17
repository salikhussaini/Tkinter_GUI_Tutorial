# Tkinter GUI Programming Tutorial: Canvas and Drawing Shapes


In this example:
- The `draw_circle` function gets the coordinates of the mouse click using `event.x` and `event.y`.
- It then draws a small purple circle at that location.
- Canvas widget in Tkinter for drawing shapes and handling mouse events.

## Step 1: Introduction to the Canvas Widget

The Canvas widget in Tkinter provides a versatile area for drawing graphics, including shapes, lines, and text. Let's start by creating a basic window with a Canvas.

```python
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Canvas Tutorial")

# Create a Canvas widget
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Start the main loop
root.mainloop()
```

In this example:
- `tk.Canvas` creates a canvas widget.
- The canvas is given a width of 400 pixels, a height of 300 pixels, and a white background.

## Step 2: Drawing Shapes on the Canvas

Now, let's draw some basic shapes on the canvas. We'll create a function, `draw_shapes`, and a button that triggers the drawing.

```python
import tkinter as tk

def draw_shapes():
    # Draw a rectangle
    canvas.create_rectangle(50, 50, 150, 100, fill="blue")

    # Draw an oval
    canvas.create_oval(200, 50, 300, 100, fill="red")

    # Draw a line
    canvas.create_line(350, 50, 350, 100, fill="green", width=3)

# Create the main window
root = tk.Tk()
root.title("Canvas Tutorial")

# Create a Canvas widget
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Create a button to trigger drawing
draw_button = tk.Button(root, text="Draw Shapes", command=draw_shapes)
draw_button.pack()

# Start the main loop
root.mainloop()
```

In this example:
- The `draw_shapes` function uses `canvas.create_rectangle`, `canvas.create_oval`, and `canvas.create_line` to draw shapes.
- The button triggers the drawing when clicked.

## Step 3: Handling Mouse Events on the Canvas

The Canvas widget allows us to handle mouse events, such as clicks. Let's create a function that draws a circle wherever the user clicks on the canvas.

```python
import tkinter as tk

def draw_circle(event):
    x, y = event.x, event.y
    canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="purple")

# Create the main window
root = tk.Tk()
root.title("Canvas Tutorial")

# Create a Canvas widget
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Bind the canvas to the draw_circle function
canvas.bind("<Button-1>", draw_circle)

# Start the main loop
root.mainloop()
```
