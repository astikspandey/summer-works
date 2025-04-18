import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "library_data.json"

# Load library from file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        content = f.read().strip()
        library = json.loads(content) if content else []
else:
    library = []

# Save library to file
def save_library():
    with open(DATA_FILE, "w") as f:
        json.dump(library, f, indent=2)

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library Manager")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ffe4b5")

        title_label = tk.Label(root, text="Welcome to the Library Manager!", font=("Helvetica", 26, "bold"), bg="#ffe4b5", fg="#2c3e50")
        title_label.pack(pady=20)

        main_frame = tk.Frame(root, bg="#fff8dc")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        button_frame = tk.Frame(main_frame, bg="#fff8dc")
        button_frame.pack(side="left", padx=20, pady=10)

        button_style = {
            "width": 25,
            "height": 2,
            "font": ("Helvetica", 16, "bold"),
            "bg": "#f5f5dc",
            "fg": "#333333",
            "activebackground": "#2980b9",
            "relief": "raised",
            "bd": 2
        }

        tk.Button(button_frame, text="➕ Add Book", command=self.add_book, **button_style).pack(pady=10)
        tk.Button(button_frame, text="📖 Borrow Book", command=self.borrow_book, **button_style).pack(pady=10)
        tk.Button(button_frame, text="🔁 Return Book", command=self.return_book, **button_style).pack(pady=10)
        tk.Button(button_frame, text="❌ Remove Book", command=self.remove_book, **button_style).pack(pady=10)

        right_frame = tk.Frame(main_frame, bg="#fff8dc")
        right_frame.pack(side="right", fill="both", expand=True)

        listbox_label = tk.Label(right_frame, text="Library Collection:", font=("Helvetica", 16, "bold"), bg="#fff8dc", fg="#2c3e50")
        listbox_label.pack(pady=(0, 10))

        self.book_listbox = tk.Listbox(
            right_frame,
            width=90,
            height=25,
            font=("Serif", 14),
            bd=2,
            relief="sunken",
            bg="#FFF4F2",  # Light pink color
        )
        self.book_listbox.pack(pady=10, fill="both", expand=True)
        self.book_listbox.bind("<Double-Button-1>", self.show_book_details)

        self.view_books()
        self.root.after(1000, self.check_reminders)  # Fix: call check_reminders after window is ready

    def view_books(self):
        self.book_listbox.delete(0, tk.END)
        if not library:
            self.book_listbox.insert(tk.END, "No books in the library.")
        else:
            for book in library:
                status = "✅ Available for borrowing" if book['status'] == 'available' else f"❎ Borrowed (Due {book['return_date']})"
                self.book_listbox.insert(tk.END, f"{book['title']} by {book['author']} ({book['year']}) [{status}]")

    def show_book_details(self, event):
        selection = self.book_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index >= len(library):
            return

        book = library[index]
        status = "Available" if book['status'] == 'available' else f"Borrowed (Due {book['return_date']})"
        details = (
            f"Title: {book['title']}\n"
            f"Author: {book['author']}\n"
            f"Year: {book['year']}\n"
            f"Status: {status}"
        )

        detail_window = tk.Toplevel(self.root)
        detail_window.title("Book Details")
        detail_window.geometry("400x350")
        detail_window.configure(bg="#fffaf0")

        tk.Label(detail_window, text="Book Details", font=("Helvetica", 28, "bold"), bg="#fffaf0", fg="#2c3e50").pack(pady=10)
        tk.Label(detail_window, text=details, font=("Helvetica", 16), bg="#fffaf0", justify="left", anchor="w").pack(padx=20, pady=10, fill="both")

    def borrow_from_details(self, index, window):
        book = library[index]
        if book['status'] == 'borrowed':
            messagebox.showinfo("Info", "This book is already borrowed.")
            return

        return_date = datetime.now().replace(microsecond=0) + timedelta(days=7)
        book['status'] = 'borrowed'
        book['return_date'] = return_date.strftime("%Y-%m-%d")
        save_library()
        self.view_books()
        # Removed window.destroy() to keep the app running

    def return_from_details(self, index, window):
        book = library[index]
        if book['status'] == 'available':
            messagebox.showinfo("Info", "This book is not currently borrowed.")
            return

        book['status'] = 'available'
        book['return_date'] = ''
        save_library()
        self.view_books()

    def add_book(self):
        def save_new_book():
            title = title_entry.get().strip()
            author = author_entry.get().strip()
            year = year_entry.get().strip()

            if not title or not author or not year:
                messagebox.showwarning("Input Error", "All fields are required!")
                return  # Form remains open

            try:
                year = int(year)  # Validate that the year is a number
                current_year = datetime.now().year
                if year < 1000 or year > current_year:
                    messagebox.showwarning("Input Error", f"Year must be between 1000 and {current_year}!")
                    return  # Form remains open
            except ValueError:
                messagebox.showwarning("Input Error", "Year must be a valid number!")
                return  # Form remains open

            library.append({
                "title": title,
                "author": author,
                "year": year,
                "status": "available",
                "return_date": ""
            })
            save_library()
            self.view_books()
            add_book_window.destroy()  # Form closes only after successful save

        # Create a new window for the form
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add New Book")
        add_book_window.geometry("400x300")
        add_book_window.configure(bg="#fffaf0")

        # Bring the form to the top
        add_book_window.lift()
        add_book_window.attributes("-topmost", True)
        add_book_window.after(1, lambda: add_book_window.attributes("-topmost", False))

        tk.Label(add_book_window, text="Add New Book", font=("Helvetica", 18, "bold"), bg="#fffaf0", fg="#2c3e50").pack(pady=10)

        form_frame = tk.Frame(add_book_window, bg="#fffaf0")
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        tk.Label(form_frame, text="Title:", font=("Helvetica", 14), bg="#fffaf0").grid(row=0, column=0, sticky="w", pady=5)
        title_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        title_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Author:", font=("Helvetica", 14), bg="#fffaf0").grid(row=1, column=0, sticky="w", pady=5)
        author_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        author_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Year:", font=("Helvetica", 14), bg="#fffaf0").grid(row=2, column=0, sticky="w", pady=5)
        year_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        year_entry.grid(row=2, column=1, pady=5)

        # Add the Save button
        tk.Button(add_book_window, text="Save", font=("Helvetica", 14, "bold"), bg="#2ecc71", fg="white", command=save_new_book).pack(pady=20)

    def borrow_book(self):
        index = self.book_listbox.curselection()
        if not index:
            messagebox.showinfo("Info", "Please select a book to borrow.")
            return
        self.borrow_from_details(index[0], self.root)

    def return_book(self):
        index = self.book_listbox.curselection()
        if not index:
            messagebox.showinfo("Info", "Please select a book to return.")
            return
        self.return_from_details(index[0], self.root)

    def remove_book(self):
        index = self.book_listbox.curselection()
        if not index:
            messagebox.showinfo("Info", "Please select a book to remove.")
            return
        del library[index[0]]
        save_library()
        self.view_books()

    def check_reminders(self):
        today = datetime.now().date()
        overdue_books = [book['title'] for book in library if book['status'] == 'borrowed' and datetime.strptime(book['return_date'], "%Y-%m-%d").date() <= today]
        if overdue_books:
            messagebox.showwarning("Overdue Books", "\n".join(f"'{title}' is overdue!" for title in overdue_books))

if __name__ == '__main__':
    root = tk.Tk()
    LibraryApp(root)
    root.mainloop()