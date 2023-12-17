```python
import tkinter as tk
from tkinter import StringVar, OptionMenu
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Plot Graph")

        # Create and pack the main frame
        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack()

        # Create and pack the plot frame
        self.plot_frame = tk.Frame(self.main_frame, borderwidth=2, relief=tk.GROOVE)
        self.plot_frame.pack(pady=10)

        # Create a StringVar for the plot type
        self.plot_type_var = StringVar(value="Line Plot")

        # Create a Combobox for selecting the plot type
        plot_type_combobox = OptionMenu(self.main_frame, self.plot_type_var, "Line Plot", "Scatter Plot")
        plot_type_combobox.pack(pady=5)
        
        # Create a button to update the plot
        update_button = tk.Button(self.main_frame, text="Update Plot", command=self.update_plot)
        update_button.pack()

        # Create an initial plot
        self.create_plot()

    def create_plot(self):
        # Create a Figure and an Axes
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)

        # Plot some data (sample data for illustration)
        x_data = [1, 2, 3, 4, 5]
        y_data = [2, 4, 1, 7, 3]

        # Plot type based on the selected option
        plot_type = self.plot_type_var.get()
        if plot_type == "Line Plot":
            self.axes.plot(x_data, y_data, label="Line Plot")
        elif plot_type == "Scatter Plot":
            self.axes.scatter(x_data, y_data, label="Scatter Plot")

        # Add labels and legend
        self.axes.set_xlabel("X-axis")
        self.axes.set_ylabel("Y-axis")
        self.axes.legend()

        # Embed the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

    def update_plot(self):
        # Clear the previous plot
        self.axes.clear()

        # Create a new plot
        self.create_plot()

# Create the main window
root = tk.Tk()

# Instantiate the PlotGraphApp class
app = PlotGraphApp(root)

# Start the main loop
root.mainloop()
```
