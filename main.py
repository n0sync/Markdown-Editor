from src.editor import MarkdownEditor
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownEditor(root)
    root.mainloop()
