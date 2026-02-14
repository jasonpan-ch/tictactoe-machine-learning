import tkinter as tk

root = tk.Tk(className="tic-tac-toe-ml")

# label = tk.Label(root, text="Tic Tac Toe")
# label.pack()

# def buttonOnClick():
#     print("Button Pressed")

# button = tk.Button(root, text="Start Game", width=20, command=buttonOnClick)
# button.pack()

tk.Label(root, text="Player 1's Name:").grid(row=0, column=0)
tk.Label(root, text="Player 2's Name:").grid(row=1, column=0)

entry1 = tk.Entry(root)
entry2 = tk.Entry(root)

entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)

root.mainloop()