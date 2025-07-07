import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import sys
from pdf_merge_logic import merge_pdfs


class PDFMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Merger")
        self.geometry("500x440")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        self.pdf_files = []
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TListbox', font=('Segoe UI', 10))
        style.configure('Green.Horizontal.TProgressbar', troughcolor='#e0e0e0',
                        bordercolor='#e0e0e0', background='#4CAF50', lightcolor='#4CAF50', darkcolor='#388E3C')

        lbl = ttk.Label(
            self, text="Selected PDF files (drag to reorder):", background="#f0f0f0")
        lbl.pack(pady=(20, 5), anchor='w', padx=20)

        frame = tk.Frame(self, bg="#f0f0f0")
        frame.pack(padx=20, fill='x')

        self.listbox = tk.Listbox(
            frame, selectmode=tk.SINGLE, height=10, activestyle='none', font=('Segoe UI', 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<Button-1>', self.on_listbox_click)
        self.listbox.bind('<B1-Motion>', self.on_listbox_drag)
        self.drag_data = {"widget": None, "index": None}

        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        add_btn = ttk.Button(btn_frame, text="Add PDFs", command=self.add_pdfs)
        add_btn.grid(row=0, column=0, padx=5)
        remove_btn = ttk.Button(
            btn_frame, text="Remove Selected", command=self.remove_selected)
        remove_btn.grid(row=0, column=1, padx=5)
        up_btn = ttk.Button(btn_frame, text="Move Up", command=self.move_up)
        up_btn.grid(row=0, column=2, padx=5)
        down_btn = ttk.Button(btn_frame, text="Move Down",
                              command=self.move_down)
        down_btn.grid(row=0, column=3, padx=5)

        merge_btn = ttk.Button(self, text="Merge PDFs",
                               command=self.merge_pdfs_ui)
        merge_btn.pack(pady=20)

        # Progress bar (initially hidden, styled green)
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=300, mode="determinate", style='Green.Horizontal.TProgressbar')
        self.progress.pack(pady=(0, 10))
        self.progress.pack_forget()

        # Add author label in the very bottom right as a clickable blue link
        author_label = ttk.Label(self, text="By Abdelhaq El Amraoui", foreground="blue",
                                 cursor="hand2", background="#f0f0f0", font=("Segoe UI", 9, "italic"))
        author_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-6)
        author_label.bind("<Button-1>", lambda e: self.open_github())

    def add_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        for f in files:
            if f not in self.pdf_files:
                self.pdf_files.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))

    def remove_selected(self):
        sel = self.listbox.curselection()
        if sel:
            idx = sel[0]
            self.listbox.delete(idx)
            del self.pdf_files[idx]

    def move_up(self):
        sel = self.listbox.curselection()
        if sel and sel[0] > 0:
            idx = sel[0]
            self.pdf_files[idx -
                           1], self.pdf_files[idx] = self.pdf_files[idx], self.pdf_files[idx-1]
            txt = self.listbox.get(idx)
            self.listbox.delete(idx)
            self.listbox.insert(idx-1, txt)
            self.listbox.select_set(idx-1)

    def move_down(self):
        sel = self.listbox.curselection()
        if sel and sel[0] < self.listbox.size() - 1:
            idx = sel[0]
            self.pdf_files[idx +
                           1], self.pdf_files[idx] = self.pdf_files[idx], self.pdf_files[idx+1]
            txt = self.listbox.get(idx)
            self.listbox.delete(idx)
            self.listbox.insert(idx+1, txt)
            self.listbox.select_set(idx+1)

    def merge_pdfs_ui(self):
        if not self.pdf_files:
            messagebox.showwarning("No PDFs", "Please add PDF files to merge.")
            return
        save_path = filedialog.asksaveasfilename(
            title="Save Merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not save_path:
            return
        try:
            self.show_progress_bar(len(self.pdf_files))
            self.update_idletasks()
            self.merge_with_progress(self.pdf_files, save_path)
            self.hide_progress_bar()
            if messagebox.askyesno("Success", f"PDFs merged successfully into:\n{save_path}\n\nOpen the merged PDF now?"):
                self.open_file(save_path)
        except Exception as e:
            self.hide_progress_bar()
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

    def show_progress_bar(self, total):
        self.progress['maximum'] = total
        self.progress['value'] = 0
        self.progress.pack(pady=(0, 10))
        self.progress.update()

    def hide_progress_bar(self):
        self.progress.pack_forget()

    def merge_with_progress(self, pdf_files, output_path):
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        for idx, pdf in enumerate(pdf_files):
            merger.append(pdf)
            self.progress['value'] = idx + 1
            self.progress.update()
        merger.write(output_path)
        merger.close()

    def open_file(self, path):
        try:
            if sys.platform.startswith('win'):
                os.startfile(path)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{path}"')
            else:
                os.system(f'xdg-open "{path}"')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def open_github(self):
        import webbrowser
        webbrowser.open_new("https://github.com/abdelhaqelamraoui/pdf_merger")

    # Drag-and-drop reordering for listbox
    def on_listbox_click(self, event):
        self.drag_data["widget"] = event.widget
        self.drag_data["index"] = event.widget.nearest(event.y)

    def on_listbox_drag(self, event):
        widget = self.drag_data["widget"]
        if widget:
            idx = widget.nearest(event.y)
            if idx != self.drag_data["index"] and 0 <= idx < widget.size():
                # Swap in listbox
                txt1 = widget.get(self.drag_data["index"])
                txt2 = widget.get(idx)
                widget.delete(self.drag_data["index"])
                widget.insert(idx, txt1)
                widget.delete(idx+1)
                widget.insert(self.drag_data["index"], txt2)
                # Swap in file list
                self.pdf_files[self.drag_data["index"]
                               ], self.pdf_files[idx] = self.pdf_files[idx], self.pdf_files[self.drag_data["index"]]
                self.drag_data["index"] = idx


if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()
