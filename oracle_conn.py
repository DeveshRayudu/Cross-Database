import tkinter as tk

root = tk.Tk()
root.title("Centered Labels")

# Create a frame
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# A centered label in column 0
label1 = tk.Label(frame, text="Centered Label")
label1.grid(row=0, column=0, padx=10, pady=10, sticky='ew')  # 'ew' = east-west (horizontal)

# Make column 0 expand to fill space, so the label can center
frame.grid_columnconfigure(0, weight=1)

root.mainloop()
