import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os


def remove_bottom_whitespace_from_pdf(input_pdf, output_pdf, margin_threshold=20, spazio_in_fondo=50):
    doc = fitz.open(input_pdf)
    for page in doc:
        blocks = page.get_text("blocks")
        if not blocks:
            continue

        x0, y0, x1, y1 = page.rect.x0, page.rect.y0, page.rect.x1, page.rect.y1
        max_y1 = 0

        for b in blocks:
            _, y_top, _, y_bottom, *_ = b
            if y_bottom > max_y1:
                max_y1 = y_bottom

        bottom_margin = page.rect.y1 - max_y1
        if bottom_margin > margin_threshold:
            nuovo_y1 = min(page.rect.y1, max_y1 + spazio_in_fondo)
            new_rect = fitz.Rect(x0, y0, x1, nuovo_y1)
            page.set_cropbox(new_rect)

    doc.save(output_pdf)
    doc.close()


def browse_input_folder():
    folder = filedialog.askdirectory()
    if folder:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, folder)

def browse_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder)

def process_all_pdfs():
    input_folder = input_entry.get()
    output_folder = output_entry.get()
    try:
        threshold = int(threshold_entry.get())
    except ValueError:
        messagebox.showerror("Errore", "Il margine deve essere un numero intero")
        return

    if not input_folder or not output_folder:
        messagebox.showerror("Errore", "Seleziona entrambe le cartelle di input e output.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    total = len(pdf_files)
    if total == 0:
        messagebox.showinfo("Info", "Nessun file PDF trovato nella cartella.")
        return

    progress_bar["maximum"] = total
    progress_bar["value"] = 0
    root.update_idletasks()

    processed = 0
    for i, filename in enumerate(pdf_files, 1):
        input_pdf = os.path.join(input_folder, filename)
        output_pdf = os.path.join(output_folder, filename)
        try:
            remove_bottom_whitespace_from_pdf(input_pdf, output_pdf, threshold)
            processed += 1
        except Exception as e:
            print(f"Errore su {filename}: {e}")

        progress_bar["value"] = i
        progress_label.config(text=f"{i}/{total} file elaborati")
        root.update_idletasks()

    messagebox.showinfo("Completato", f"{processed} file PDF processati correttamente.")

# GUI
root = tk.Tk()
root.title("Taglia margine bianco PDF (Cartella intera)")
root.geometry("500x350")
root.resizable(False, False)

tk.Label(root, text="Cartella PDF di input:").pack(pady=(10, 0))
input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=2)
tk.Button(root, text="Sfoglia...", command=browse_input_folder).pack()

tk.Label(root, text="Cartella PDF di output:").pack(pady=(10, 0))
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=2)
tk.Button(root, text="Sfoglia...", command=browse_output_folder).pack()

tk.Label(root, text="Margine minimo da tagliare (default 20):").pack(pady=(10, 0))
threshold_entry = tk.Entry(root, width=10)
threshold_entry.insert(0, "20")
threshold_entry.pack()

tk.Button(root, text="Esegui su tutti i PDF", command=process_all_pdfs, bg="lightgreen", width=30).pack(pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=(10, 0))

progress_label = tk.Label(root, text="")
progress_label.pack(pady=(5, 10))

root.mainloop()
