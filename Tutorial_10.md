In this example:

- Users can upload a CSV file using the "Upload CSV" button.
- The data from the CSV file is displayed in a text widget.
- Users can select x and y variables from the dropdown menus.
- Clicking the "Perform Linear Regression" button displays a scatter plot with the actual and predicted values based on linear regression.
- The `pandas`, `scikit-learn`, and `matplotlib` libraries are used for data manipulation, machine learning, and plotting, respectively.

```python
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to upload CSV file
def upload_csv():
    file_path = filedialog.askopenfilename(title="Select a CSV File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

    if file_path:
        # Load CSV into a DataFrame
        df = pd.read_csv(file_path)
        display_data(df)

# Function to perform linear regression
def perform_linear_regression():
    # Get selected x and y columns
    x_column = x_variable.get()
    y_column = y_variable.get()

    if x_column and y_column:
        # Extract x and y data
        X = df[[x_column]]
        y = df[y_column]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and train the linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predictions on the test set
        predictions = model.predict(X_test)

        # Display the linear regression plot
        display_linear_regression_plot(X_test, y_test, predictions)

# Function to display data in a Table
def display_data(data_frame):
    # Display data in a Table
    data_frame_display.config(state=tk.NORMAL)
    data_frame_display.delete(1.0, tk.END)
    data_frame_display.insert(tk.END, data_frame.to_string(index=False))
    data_frame_display.config(state=tk.DISABLED)

# Function to display linear regression plot
def display_linear_regression_plot(X_test, y_test, predictions):
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Scatter plot of actual vs. predicted values
    ax.scatter(X_test, y_test, color='blue', label='Actual')
    ax.scatter(X_test, predictions, color='red', label='Predicted')

    ax.set_xlabel(x_variable.get())
    ax.set_ylabel(y_variable.get())
    ax.legend()

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

# Create the main window
root = tk.Tk()
root.title("Linear Regression with Tkinter")

# Create and place widgets in the window
upload_button = tk.Button(root, text="Upload CSV", command=upload_csv)
upload_button.pack(pady=10)

# Create a text widget to display data
data_frame_display = tk.Text(root, wrap="none", width=60, height=10)
data_frame_display.pack()

# Dropdowns for selecting x and y variables
x_variable = tk.StringVar()
y_variable = tk.StringVar()

x_dropdown = tk.OptionMenu(root, x_variable, *[], command=perform_linear_regression)
y_dropdown = tk.OptionMenu(root, y_variable, *[], command=perform_linear_regression)

x_dropdown.pack(pady=5)
y_dropdown.pack(pady=5)

# Start the main loop
root.mainloop()
```
Note: Make sure to install the necessary libraries before running the code by using:
```bash
pip install pandas scikit-learn matplotlib
```
