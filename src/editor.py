import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import markdown
from tkinterweb import HtmlFrame
from pygments.formatters import HtmlFormatter
from weasyprint import HTML


class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Markdown Editor")
        self.root.geometry("1200x800")
        self.live_preview = tk.BooleanVar(value=True)
        self.setup_ui()
        self.setup_menu()
        self.apply_dark_theme()

    
    def setup_ui(self):
        self.pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.pane.pack(fill=tk.BOTH, expand=True)
        self.input_area = scrolledtext.ScrolledText(
        self.pane, wrap=tk.WORD, font=('TimesNewRoman', 12), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.pane.add(self.input_area, weight=1)
        self.preview_frame = HtmlFrame(self.pane)  
        self.pane.add(self.preview_frame, weight=1)
        self.status_bar = ttk.Label(self.root, text="Ready", anchor="w", background="#252526", foreground="white")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.input_area.bind("<KeyRelease>", self.update_preview)
    

    def highlight_syntax(self):
        self.input_area.tag_configure('heading', foreground='#569CD6')
    
    
    def apply_dark_theme(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#252526")
        style.configure("TLabel", background="#252526", foreground="white")
        style.configure("TButton", background="#333333", foreground="white", borderwidth=1)
        style.configure("TMenu", background="#252526", foreground="white", relief="flat")
        self.root.config(bg="#252526")


    def render_markdown(self, text):
        extensions = ['fenced_code', 'tables', 'codehilite']
        html = markdown.markdown(text, extensions=extensions)
        formatter = HtmlFormatter(style='monokai')
        return f"<style>{formatter.get_style_defs()}</style>{html}"


    def update_preview(self, event=None):
        if self.live_preview.get():
            markdown_text = self.input_area.get("1.0", tk.END).strip()
            html_output = self.render_markdown(markdown_text)
            self.preview_frame.load_html(html_output)


    def setup_menu(self):
        menubar = tk.Menu(self.root, bg="#252526", fg="white", tearoff=0)
        file_menu = tk.Menu(menubar, tearoff=0, bg="#252526", fg="white")
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Export to PDF", command=self.export_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        view_menu = tk.Menu(menubar, tearoff=0, bg="#252526", fg="white")
        view_menu.add_checkbutton(label="Live Preview", variable=self.live_preview)
        menubar.add_cascade(label="View", menu=view_menu)
        self.root.config(menu=menubar)
    

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Markdown Files", "*.md")])
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.input_area.delete("1.0", tk.END)
                    self.input_area.insert(tk.END, f.read())
                self.status_bar.config(text=f"Opened: {filepath}")
                self.update_preview()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(self.input_area.get("1.0", tk.END))
                self.status_bar.config(text=f"Saved: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def export_pdf(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if filepath:
            try:
                html_content = self.render_markdown(self.input_area.get("1.0", tk.END))
                HTML(string=html_content).write_pdf(filepath)
                self.status_bar.config(text=f"Exported PDF: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export PDF: {e}")


