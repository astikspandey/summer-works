import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta
import calendar
from datetime import datetime

class AddHabitWindow(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Add New Habit")
        self.geometry("400x300")
        self.configure(bg="#e3f2fd")  # Light blue background

        # Make window modal
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Add New Habit", 
                font=("Helvetica", 18, "bold"), 
                bg="#e3f2fd", 
                fg="#1a237e").pack(pady=10)

        form_frame = tk.Frame(self, bg="#e3f2fd")
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Habit Name
        tk.Label(form_frame, text="Habit Name:", 
                font=("Helvetica", 14), 
                bg="#e3f2fd").grid(row=0, column=0, sticky="w", pady=5)
        self.habit_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.habit_entry.grid(row=0, column=1, pady=5)

        # Times
        tk.Label(form_frame, text="Times:", 
                font=("Helvetica", 14), 
                bg="#e3f2fd").grid(row=1, column=0, sticky="w", pady=5)
        self.times_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=30)
        self.times_entry.grid(row=1, column=1, pady=5)

        # Frequency
        tk.Label(form_frame, text="Frequency:", 
                font=("Helvetica", 14), 
                bg="#e3f2fd").grid(row=2, column=0, sticky="w", pady=5)
        self.freq_combo = ttk.Combobox(form_frame, 
                                     values=["Daily", "Weekly", "Monthly"],
                                     state="readonly",
                                     font=("Helvetica", 14),
                                     width=28)
        self.freq_combo.set("Daily")
        self.freq_combo.grid(row=2, column=1, pady=5)

        # Save button - updated colors
        tk.Button(self, text="Save", 
                 font=("Helvetica", 14, "bold"), 
                 bg="#bbdefb",  # Light blue button background
                 fg="#1a237e",  # Dark blue text
                 activebackground="#2962ff",  # Bright blue when clicked
                 command=self.save_habit).pack(pady=20)

    def save_habit(self):
        name = self.habit_entry.get()
        times = self.times_entry.get()
        frequency = self.freq_combo.get()
        
        if name and times:
            try:
                times = int(times)
                if times > 0:
                    habit_data = {
                        "name": name,
                        "times": times,
                        "frequency": frequency
                    }
                    self.callback(habit_data)
                    self.destroy()
                else:
                    messagebox.showwarning("Error", "Please enter a positive number")
            except ValueError:
                messagebox.showwarning("Error", "Please enter a valid number")
        else:
            messagebox.showwarning("Error", "Please fill all fields")

class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Habit Tracker")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1a237e")

        # Title Label - updated background and text colors
        title_label = tk.Label(root, text="Welcome to the Habit Tracker!", 
                             font=("Helvetica", 26, "bold"), 
                             bg="#1a237e", 
                             fg="white")
        title_label.pack(pady=20)

        # Main frame - change from #fff8dc (lighter orange) to #e3f2fd (light blue)
        main_frame = tk.Frame(root, bg="#e3f2fd")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Button frame - match main frame color
        button_frame = tk.Frame(main_frame, bg="#e3f2fd")
        button_frame.pack(side="left", padx=20, pady=10)

        # Button styling - updated colors
        button_style = {
            "width": 25,
            "height": 2,
            "font": ("Helvetica", 16, "bold"),
            "bg": "#bbdefb",  # Light blue button background
            "fg": "#1a237e",  # Dark blue text
            "activebackground": "#2962ff",  # Bright blue when clicked
            "relief": "raised",
            "bd": 2
        }

        # Search Button
        tk.Button(button_frame, text="🔍 Search",
                 command=self.show_search_form,
                 **button_style).pack(pady=10)
        
        # Buttons
        tk.Button(button_frame, text="➕        Add Habit", 
                 command=self.add_habit, **button_style).pack(pady=10)
        tk.Button(button_frame, text="🗑️ Delete Habit", 
                 command=self.delete_habit, **button_style).pack(pady=10)
        tk.Button(button_frame, text="📊 View Progress", 
                 command=self.show_progress, **button_style).pack(pady=10)

        # Right frame - match main frame color
        right_frame = tk.Frame(main_frame, bg="#e3f2fd")
        right_frame.pack(side="right", fill="both", expand=True)

        # Habit list label - updated colors
        listbox_label = tk.Label(right_frame, text="Your Habits:", 
                               font=("Helvetica", 16, "bold"), 
                               bg="#e3f2fd", 
                               fg="#1a237e")
        listbox_label.pack(pady=(0, 10))

        # Habit text widget - using Text instead of Listbox for better styling
        self.habit_text = tk.Text(
            right_frame,
            width=90,
            height=25,
            font=("Serif", 14),
            bd=2,
            relief="sunken",
            bg="#f5f9ff",  # Very light blue background
            wrap=tk.WORD,
            cursor="arrow"
        )
        self.habit_text.pack(pady=10, fill="both", expand=True)
        self.habit_text.bind("<Double-Button-1>", self.show_habit_details)
        
        # Configure tags for different styles
        self.habit_text.tag_configure('header', font=('Helvetica', 16, 'bold'), foreground='#1a237e')
        self.habit_text.tag_configure('habit', font=('Serif', 14))
        self.habit_text.tag_configure('empty', font=('Serif', 14))
        
        # Disable text widget editing
        self.habit_text.config(state='disabled')

        # Load existing habits
        self.json_file = "habits.json"
        self.habits = self.load_habits()
        self.load_habits_to_listbox()

    def show_search_form(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Habits")
        search_window.geometry("400x300")
        search_window.configure(bg="#e3f2fd")

        # Search entry
        search_frame = tk.Frame(search_window, bg="#e3f2fd")
        search_frame.pack(pady=20)
        
        tk.Label(search_frame, text="Search Habits:", 
                font=("Helvetica", 14), 
                bg="#e3f2fd").pack(side="left", padx=10)
        
        self.search_entry = tk.Entry(search_frame, 
                                    font=("Helvetica", 14), 
                                    width=20)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.filter_habits)

        # Results listbox
        self.results_listbox = tk.Listbox(search_window,
                                        font=("Helvetica", 12),
                                        width=40,
                                        height=10)
        self.results_listbox.pack(pady=20)
        self.results_listbox.bind("<<ListboxSelect>>", self.select_habit)
        
        # Close button
        tk.Button(search_window, text="Close", 
                 command=search_window.destroy,
                 font=("Helvetica", 12),
                 bg="#bbdefb",
                 fg="#1a237e").pack(pady=10)

    def add_habit(self):
        AddHabitWindow(self.root, self.add_habit_to_list)

    def add_habit_to_list(self, habit_data):
        self.habits.append(habit_data)
        self.save_habits()
        self.load_habits_to_listbox()

    def delete_habit(self):
        selected = self.habit_text.tag_ranges('sel')
        if selected:
            start = str(selected[0])
            end = str(selected[1])
            
            # Find the habit index
            for i, habit in enumerate(self.habits):
                if f'{i}.0' <= start <= f'{i}.0 lineend':
                    del self.habits[i]
                    self.save_habits()
                    self.load_habits_to_listbox()
                    break

    def show_progress(self):
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Habit Progress")
        progress_window.geometry("600x400")
        progress_window.configure(bg="#e3f2fd")

        progress_frame = tk.Frame(progress_window, bg="#e3f2fd")
        progress_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for i, habit in enumerate(self.habits):
            tk.Label(progress_frame, text=habit['name'],
                    font=("Helvetica", 14, "bold"),
                    bg="#e3f2fd",
                    fg="#1a237e").pack(anchor="w", pady=5)
            
            progress = (habit.get('times', 0) / habit.get('frequency', 1)) * 100
            progress_bar = ttk.Progressbar(progress_frame,
                                         length=400,
                                         mode='determinate',
                                         value=progress)
            progress_bar.pack(anchor="w", pady=5)

    def show_habit_details(self, event):
        # Get the line number where the double-click occurred
        index = self.habit_text.index("@%d,%d" % (event.x, event.y))
        line = int(index.split('.')[0])
        
        # Get the text of the clicked line
        line_text = self.habit_text.get(f"{line}.0", f"{line}.end").strip()
        
        # Find the habit that matches this line
        for i, habit in enumerate(self.habits):
            if habit['name'] in line_text:
                detail_window = tk.Toplevel(self.root)
                detail_window.title(f"Habit Details: {habit['name']}")
                detail_window.geometry("400x300")
                detail_window.configure(bg="#e3f2fd")

                tk.Label(detail_window, text=habit['name'],
                        font=("Helvetica", 18, "bold"),
                        bg="#e3f2fd",
                        fg="#1a237e").pack(pady=10)

                tk.Label(detail_window, text=f"Times: {habit.get('times', 0)}",
                        font=("Helvetica", 14),
                        bg="#e3f2fd").pack(pady=5)

                tk.Label(detail_window, text=f"Frequency: {habit.get('frequency', 'Daily')}",
                        font=("Helvetica", 14),
                        bg="#e3f2fd",
                        fg="#1a237e").pack(pady=5)

                buttons_frame = tk.Frame(detail_window, bg="#e3f2fd")
                buttons_frame.pack(pady=10)

                tk.Button(buttons_frame, text="Mark as Done",
                        command=lambda: self.mark_habit_done(i, detail_window),
                        font=("Helvetica", 12),
                        bg="#bbdefb",
                        fg="#1a237e").pack(side="left", padx=5)

                tk.Button(buttons_frame, text="Add Note",
                        command=lambda: self.add_note_for_habit(habit['name'], i, detail_window),
                        font=("Helvetica", 12),
                        bg="#bbdefb",
                        fg="#1a237e").pack(side="left", padx=5)

                tk.Button(buttons_frame, text="Close",
                        command=detail_window.destroy,
                        font=("Helvetica", 12),
                        bg="#bbdefb",
                        fg="#1a237e").pack(side="left", padx=5)
                return

    def mark_habit_done(self, index, detail_window=None):
        if 0 <= index < len(self.habits):
            self.habits[index]['times'] = self.habits[index].get('times', 0) + 1
            self.habits[index]['last_completed'] = datetime.now().strftime("%Y-%m-%d")
            self.save_habits()
            self.load_habits_to_listbox()
            if detail_window:
                detail_window.destroy()

    def add_note_for_habit(self, habit_name, index, detail_window=None):
        note_window = tk.Toplevel(self.root)
        note_window.title(f"Add Note for {habit_name}")
        note_window.geometry("400x300")
        note_window.configure(bg="#e3f2fd")

        tk.Label(note_window, text="Add Note:",
                font=("Helvetica", 14),
                bg="#e3f2fd").pack(pady=10)

        self.note_text = tk.Text(note_window,
                                height=10,
                                width=40,
                                font=("Helvetica", 12))
        self.note_text.pack(pady=10)

        tk.Button(note_window, text="Save Note",
                command=lambda: self.save_note(index, note_window),
                font=("Helvetica", 12),
                bg="#bbdefb",
                fg="#1a237e").pack(pady=10)

    def save_note(self, index):
        note = self.note_text.get("1.0", tk.END).strip()
        if note:
            if 'notes' not in self.habits[index]:
                self.habits[index]['notes'] = []
            self.habits[index]['notes'].append({
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'content': note
            })
            self.save_habits()
            self.load_habits_to_listbox()

    def load_habits(self):
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            messagebox.showerror("Error", f"Error loading habits: {str(e)}")
            return []

    def save_habits(self):
        try:
            with open(self.json_file, 'w') as f:
                json.dump(self.habits, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving habits: {str(e)}")

    def load_habits_to_listbox(self):
        self.habit_text.config(state='normal')
        self.habit_text.delete('1.0', tk.END)
        
        if not self.habits:
            self.habit_text.insert(tk.END, "No habits added yet.\n", 'empty')
        else:
            for i, habit in enumerate(self.habits):
                self.habit_text.insert(tk.END, f"{habit['name']}\n", 'habit')
                if 'times' in habit:
                    self.habit_text.insert(tk.END, f"Times: {habit['times']}\n", 'habit')
                if 'frequency' in habit:
                    self.habit_text.insert(tk.END, f"Frequency: {habit['frequency']}\n", 'habit')
                if 'notes' in habit and habit['notes']:
                    self.habit_text.insert(tk.END, "Notes:\n", 'habit')
                    for note in habit['notes']:
                        self.habit_text.insert(tk.END, 
                                             f"- {note['content']} ({note['date']})\n",
                                             'habit')
                self.habit_text.insert(tk.END, "\n", 'habit')
        
        self.habit_text.config(state='disabled')

    def filter_habits(self, event):
        search_text = self.search_entry.get().lower()
        self.results_listbox.delete(0, tk.END)
        
        for i, habit in enumerate(self.habits):
            if search_text in habit['name'].lower():
                self.results_listbox.insert(tk.END, f"{i+1}. {habit['name']}")

    def select_habit(self, event):
        selection = self.results_listbox.curselection()
        if selection:
            index = int(self.results_listbox.get(selection[0]).split('.')[0]) - 1
            self.habit_text.see(f"{index}.0")
            self.habit_text.tag_add('sel', f"{index}.0", f"{index}.0 lineend")
        tk.Button(button_frame, text="🔍 Search",
                 command=self.show_search_form,
                 **button_style).pack(pady=10)
        
        # Buttons
        tk.Button(button_frame, text="➕        Add Habit", 
                 command=self.add_habit, **button_style).pack(pady=10)
        tk.Button(button_frame, text="🗑️ Delete Habit", 
                 command=self.delete_habit, **button_style).pack(pady=10)
        tk.Button(button_frame, text="📊 View Progress", 
                 command=self.show_progress, **button_style).pack(pady=10)

        # Right frame - match main frame color
        right_frame = tk.Frame(main_frame, bg="#e3f2fd")
        right_frame.pack(side="right", fill="both", expand=True)

        # Habit list label - updated colors
        listbox_label = tk.Label(right_frame, text="Your Habits:", 
                               font=("Helvetica", 16, "bold"), 
                               bg="#e3f2fd", 
                               fg="#1a237e")
        listbox_label.pack(pady=(0, 10))

        # Habit text widget - using Text instead of Listbox for better styling
        self.habit_text = tk.Text(
            right_frame,
            width=90,
            height=25,
            font=("Serif", 14),
            bd=2,
            relief="sunken",
            bg="#f5f9ff",  # Very light blue background
            wrap=tk.WORD,
            cursor="arrow"
        )
        self.habit_text.pack(pady=10, fill="both", expand=True)
        self.habit_text.bind("<Double-Button-1>", self.show_habit_details)
        
        # Configure tags for different styles
        self.habit_text.tag_configure('header', font=('Helvetica', 16, 'bold'), foreground='#1a237e')
        self.habit_text.tag_configure('habit', font=('Serif', 14))
        self.habit_text.tag_configure('empty', font=('Serif', 14))
        
        # Disable text widget editing
        self.habit_text.config(state='disabled')

        # Load existing habits
        self.json_file = "habits.json"
        self.habits = self.load_habits()
        self.load_habits_to_listbox()

    def show_search_form(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Habits")
        search_window.geometry("400x300")
        search_window.configure(bg="#e3f2fd")

        # Search entry
        search_frame = tk.Frame(search_window, bg="#e3f2fd")
        search_frame.pack(pady=20)
        
        tk.Label(search_frame, text="Search Habits:", 
                font=("Helvetica", 14), 
                bg="#e3f2fd").pack(side="left", padx=10)
        
        self.search_entry = tk.Entry(search_frame, 
                                    font=("Helvetica", 14), 
                                    width=20)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.filter_habits)

        # Results listbox
        self.search_listbox = tk.Listbox(search_window,
                                        font=("Helvetica", 12),
                                        width=40,
                                        height=10)
        self.search_listbox.pack(pady=20)
        self.search_listbox.bind("<<ListboxSelect>>", self.select_habit)
        
        # Close button
        tk.Button(search_window, text="Close", 
                 command=search_window.destroy,
                 font=("Helvetica", 12),
                 bg="#bbdefb",
                 fg="#1a237e").pack(pady=10)

    def filter_habits(self, event):
        search_text = self.search_entry.get().lower()
        filtered_habits = [habit for habit in self.habits 
                          if habit['name'].lower().startswith(search_text)]
        
        self.search_listbox.delete(0, tk.END)
        for habit in filtered_habits:
            self.search_listbox.insert(tk.END, 
                                    f"{habit['name']} - {habit['completed_times']}/{habit['times']} {habit['frequency']}")

        
    def select_habit(self, event):
        selection = self.search_listbox.curselection()
        if selection:
            index = selection[0]
            habit_text = self.search_listbox.get(index)
            
            # Find the original habit index
            original_index = None
            for i, habit in enumerate(self.habits):
                if f"{habit['name']} - {habit['completed_times']}/{habit['times']} {habit['frequency']}" == habit_text:
                    original_index = i
                    break
            
            if original_index is not None:
                # Select the habit in the main listbox
                self.habit_listbox.selection_clear(0, tk.END)
                self.habit_listbox.selection_set(original_index)
                self.habit_listbox.see(original_index)
                
                # Show habit details
                self.show_habit_details(None)
                
                # Close the search window
                self.search_window.destroy()

    def show_habit_details(self, event):
        # Get the line number where the double-click occurred
        index = self.habit_text.index("@%d,%d" % (event.x, event.y))
        line = int(index.split('.')[0])
        
        # Get the text of the clicked line
        line_text = self.habit_text.get(f"{line}.0", f"{line}.end").strip()
        
        # Find the habit that matches this line
        for i, habit in enumerate(self.habits):
            if habit['name'] in line_text:
                detail_window = tk.Toplevel(self.root)
                detail_window.title(f"Habit Details: {habit['name']}")
                detail_window.geometry("400x300")
                detail_window.configure(bg="#e3f2fd")

                tk.Label(detail_window, text=habit['name'],
                        font=("Helvetica", 18, "bold"),
                        bg="#e3f2fd",
                        fg="#1a237e").pack(pady=10)

                tk.Label(detail_window, text=f"Times: {habit.get('times', 0)}",
                        font=("Helvetica", 14),
                        bg="#e3f2fd").pack(pady=5)

                tk.Label(detail_window, text=f"Frequency: {habit.get('frequency', 'Daily')}",
                        font=("Helvetica", 14),
                        bg="#e3f2fd",
                        fg="#1a237e").pack(pady=5)

                buttons_frame = tk.Frame(detail_window, bg="#e3f2fd")
                buttons_frame.pack(pady=10)

                tk.Button(buttons_frame, text="Mark as Done",
                        command=lambda: self.mark_habit_done(i, detail_window),
                        font=("Helvetica", 12),
                        bg="#bbdefb",
                        fg="#1a237e").pack(side="left", padx=5)

                tk.Button(buttons_frame, text="Add Note",
                        command=lambda: self.add_note_for_habit(habit['name'], i, detail_window),
                        font=("Helvetica", 12),
                        bg="#bbdefb",
                        fg="#1a237e").pack(side="left", padx=5)

                tk.Button(buttons_frame, text="Close",
                        command=detail_window.destroy,
                        font=("Helvetica", 12),
                        bg="#bbdefb",
                        fg="#1a237e").pack(side="left", padx=5)
                return

    def mark_habit_done(self, index, detail_window=None):
        if index < 0 or index >= len(self.habits):
            return

        habit = self.habits[index]
        current_date = datetime.now().date()
        
        # Check if habit can be marked as done
        if habit['last_completed'] and habit['last_completed'] == current_date.strftime("%Y-%m-%d"):
            messagebox.showinfo("Already Completed", 
                f"You've already completed this habit today!\n"
                f"Current Streak: {habit['current_streak']} days")
            return

        # Update habit data
        habit['completed_times'] = habit.get('completed_times', 0) + 1
        habit['current_streak'] = habit.get('current_streak', 0) + 1
        habit['best_streak'] = max(habit.get('best_streak', 0), habit['current_streak'])
        habit['last_completed'] = current_date.strftime("%Y-%m-%d")
        
        # Save progress
        self.save_habits()
        
        # Update the text widget display
        self.habit_text.config(state='normal')
        self.habit_text.delete(f"{index}.0", f"{index+1}.0")
        self.habit_text.insert(f"{index}.0", self.format_habit_string(habit) + "\n")
        self.habit_text.config(state='disabled')
        
        # Check if all times are completed
        if habit['completed_times'] == habit['times']:
            messagebox.showinfo("Congratulations!", 
                f"You've completed all {habit['times']} times for {habit['name']}!\n"
                f"Current Streak: {habit['current_streak']} days\n"
                f"Best Streak: {habit['best_streak']} days")
            # Prompt for note after completing all times
            self.add_note_for_habit(habit['name'], index, detail_window)
        else:
            # Show progress message without prompting for note
            messagebox.showinfo("Success", 
                f"Progress: {habit['completed_times']}/{habit['times']}\n"
                f"Current Streak: {habit['current_streak']} days")
            
            if detail_window:
                detail_window.destroy()
            
    def add_note_for_habit(self, habit_name, index, detail_window=None):
        note_window = tk.Toplevel(self.root)
        note_window.title("Add Note")
        note_window.geometry("600x500")  # Increased height to fit all content
        note_window.configure(bg="#e3f2fd")
        
        tk.Label(note_window, 
                text="Add a note for today's completion:", 
                font=("Helvetica", 14, "bold"),
                bg="#e3f2fd",
                fg="#1a237e").pack(pady=10)
        
        note_text = tk.Text(note_window, 
                           height=8,
                           width=40,
                           font=("Helvetica", 12),
                           bg="#f5f9ff")
        note_text.pack(pady=10, padx=20)
        
        # Add mood rating section
        tk.Label(note_window,
                text="How did you feel after completing this habit?",
                font=("Helvetica", 12, "bold"),
                bg="#e3f2fd",
                fg="#1a237e").pack(pady=(20,10))
        
        # Mood options with emojis and colors
        moods = [
            ("😄 Very Satisfied", "#b3ff66"),  # Light green
            ("🙂 Satisfied", "#ffed4d"),       # Light yellow
            ("😐 Neutral", "#ffb84d"),         # Light orange
            ("😞 Unsatisfied", "#ff884d"),     # Dark orange
            ("😡 Very Unsatisfied", "#ff4d4d") # Light red
        ]
        
        mood_frame = tk.Frame(note_window, bg="#e3f2fd")
        mood_frame.pack(pady=10)
        
        selected_mood = tk.StringVar()
        
        class ColoredCombobox(ttk.Combobox):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.option_add('*TCombobox*Listbox.font', ('Helvetica', 14))
                self.bind('<<ComboboxSelected>>', self._on_select)
                
            def _on_select(self, event):
                selected = self.get()
                index = self['values'].index(selected)
                self.configure(style=f'Mood.{index}.TCombobox')
        
        # Create styles for each mood
        style = ttk.Style()
        for i, (mood, color) in enumerate(moods):
            style.configure(
                f'Mood.{i}.TCombobox',
                fieldbackground=color,
                selectbackground=color
            )
        
        mood_dropdown = ColoredCombobox(
            mood_frame,
            textvariable=selected_mood,
            values=[m[0] for m in moods],
            state="readonly",
            font=("Helvetica", 14),
            width=20
        )
        mood_dropdown.pack()

        # Configure the listbox colors using a simpler approach
        style = ttk.Style()
        for i, (mood, color) in enumerate(moods):
            style.map('Mood.TCombobox',
                     fieldbackground=[('readonly', color)])
        mood_dropdown.configure(style='Mood.TCombobox')
        
        def save_note():
            note = note_text.get("1.0", "end-1c")
            mood = selected_mood.get()
            
            if not mood:
                messagebox.showwarning("Missing Mood", "Please select how you felt!")
                return
                
            # Extract mood text without emoji
            mood_text = mood.split(' ', 1)[1]
                
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            try:
                with open("notes.json", "r") as f:
                    notes = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                notes = {}
                
            if habit_name not in notes:
                notes[habit_name] = []
                
            notes[habit_name].append({
                "date": current_date,
                "note": note,
                "mood": mood_text
            })
            
            # Save the notes to file
            with open("notes.json", "w") as f:
                json.dump(notes, f, indent=2)
                
            note_window.destroy()
            if detail_window:
                detail_window.destroy()
            
            with open("notes.json", "w") as f:
                json.dump(notes, f, indent=2)
            note_window.destroy()
            if detail_window:
                detail_window.destroy()

        # Save button with proper styling and placement
        save_frame = tk.Frame(note_window, bg="#e3f2fd")
        save_frame.pack(fill="x", pady=(20, 10))
        
        save_button = tk.Button(save_frame,
            text="Save Note & Mood",
            font=("Helvetica", 14, "bold"),
            bg="#bbdefb",
            fg="#1a237e",
            activebackground="#2962ff",
            relief="raised",
            bd=2,
            padx=20,
            command=save_note)
        save_button.pack(pady=10)

    def load_habits(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        valid_habits = []
                        for habit in data:
                            if isinstance(habit, dict) and all(key in habit for key in ['name', 'times', 'frequency']):
                                # Add missing fields with default values
                                if 'completed_times' not in habit:
                                    habit['completed_times'] = 0
                                if 'current_streak' not in habit:
                                    habit['current_streak'] = 0
                                if 'best_streak' not in habit:
                                    habit['best_streak'] = 0
                                if 'last_completed' not in habit:
                                    habit['last_completed'] = None
                                valid_habits.append(habit)
                        return valid_habits
                    return []
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def save_habits(self):
        with open(self.json_file, 'w') as file:
            json.dump(self.habits, file)

    def load_habits_to_listbox(self):
        # Clear existing content
        self.habit_text.config(state='normal')
        self.habit_text.delete('1.0', tk.END)
        
        # Group habits by frequency
        habit_groups = {
            'Daily': [],
            'Weekly': [],
            'Monthly': []
        }
        
        for habit in self.habits:
            frequency = habit.get('frequency', 'Daily')
            if frequency in habit_groups:
                habit_groups[frequency].append(habit)
        
        # Add section headers and habits
        for frequency in ['Daily', 'Weekly', 'Monthly']:
            if habit_groups[frequency]:
                # Add section header with tag
                self.habit_text.insert(tk.END, f"\n{frequency.upper()} HABITS\n", 'header')
                
                # Add habits for this frequency
                for habit in habit_groups[frequency]:
                    habit_str = self.format_habit_string(habit)
                    self.habit_text.insert(tk.END, f"{habit_str}\n", 'habit')
                    
                # Add empty line between sections
                self.habit_text.insert(tk.END, "\n", 'empty')
        
        # Disable editing
        self.habit_text.config(state='disabled')

    def add_habit(self):
        AddHabitWindow(self.root, self.add_habit_to_list)
    
    def add_habit_to_list(self, habit_data):
        # Update habit data with default values
        habit_data.update({
            "completed_times": 0,
            "current_streak": 0,
            "best_streak": 0,
            "last_completed": None
        })
        
        # Format and add to habits list
        habit_str = self.format_habit_string(habit_data)
        self.habits.append(habit_data)
        
        # Update the text widget
        self.habit_text.config(state='normal')
        self.habit_text.insert(tk.END, f"{habit_str}\n", 'habit')
        self.habit_text.config(state='disabled')
        
        # Save changes
        self.save_habits()
        
        # Reorganize habits by frequency
        self.load_habits_to_listbox()

    def format_habit_string(self, habit):
        return f"{habit['name']} - {habit['completed_times']}/{habit['times']} times {habit['frequency']}"

    def delete_habit(self):
        # Get the line number of the clicked position
        line_number = int(self.habit_text.index('current').split('.')[0])
        
        # Get all text up to the current line
        text = self.habit_text.get('1.0', f'{line_number}.0')
        
        # Count the number of lines before the current line
        lines = text.count('\n')
        
        # Adjust for section headers and empty lines
        adjusted_index = 0
        for i, habit in enumerate(self.habits):
            if lines <= 1:  # If we're on a section header or empty line
                return
            lines -= 1
            adjusted_index = i
        
        # Remove from text widget and habits list
        self.habit_text.config(state='normal')
        self.habit_text.delete(f'{line_number}.0', f'{line_number}.end+1lines')
        self.habits.pop(adjusted_index)
        self.save_habits()
        self.habit_text.config(state='disabled')
        
        # Reorganize habits by frequency
        self.load_habits_to_listbox()

    def show_progress(self):
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Progress & Notes")
        progress_window.geometry("800x600")
        progress_window.configure(bg="#e3f2fd")
        
        tk.Label(progress_window,
                text="Progress & Notes",
                font=("Helvetica", 24, "bold"),
                bg="#e3f2fd",
                fg="#1a237e").pack(pady=20)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(progress_window)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Streaks tab
        streaks_frame = ttk.Frame(notebook)
        notebook.add(streaks_frame, text="Streaks")
        
        streaks_text = tk.Text(streaks_frame,
                              font=("Helvetica", 12),
                              bg="#f5f9ff",
                              wrap=tk.WORD)
        streaks_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add streak information
        for habit in self.habits:
            streaks_text.insert(tk.END, 
                f"🎯 {habit['name']}\n".center(50),  # Center the title
                ("title", "emoji"))  # Tag for styling
            streaks_text.insert(tk.END,
                f"   Current Streak: {habit['current_streak']} days\n"
                f"   Best Streak: {habit['best_streak']} days\n"
                f"   Progress: {habit['completed_times']}/{habit['times']} times {habit['frequency']}\n\n")

        # Configure text tags for emoji styling
        streaks_text.tag_configure("emoji", font=("Helvetica", 20))  # Larger emoji font
        streaks_text.tag_configure("title", font=("Helvetica", 14, "bold"))
        
        # Notes tab
        notes_frame = ttk.Frame(notebook)
        notebook.add(notes_frame, text="Notes")
        
        notes_text = tk.Text(notes_frame,
                            font=("Helvetica", 12),
                            bg="#f5f9ff",
                            wrap=tk.WORD)
        notes_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            with open("notes.json", "r") as f:
                notes = json.load(f)
                
            for habit_name, habit_notes in notes.items():
                notes_text.insert(tk.END, f"📝 {habit_name}\n", ("emoji",))  # Tag for styling
                for note in habit_notes:
                    mood_emoji = {
                        "Very Unsatisfied": "😡",
                        "Unsatisfied": "☹️",
                        "Neutral": "😐",
                        "Satisfied": "🙂",
                        "Very Satisfied": "😄"
                    }.get(note.get('mood', ''), '')
                    
                    notes_text.insert(tk.END, 
                        f"   {note['date']}\n"
                        f"   Mood: {mood_emoji} ", ("emoji",))  # Tag for styling
                    notes_text.insert(tk.END,
                        f"{note.get('mood', 'No mood recorded')}\n"
                        f"   Note: {note['note']}\n\n")
        except (FileNotFoundError, json.JSONDecodeError):
            notes_text.insert(tk.END, "No notes available yet.")
        
        # Configure text tags for emoji styling
        notes_text.tag_configure("emoji", font=("Helvetica", 20))  # Larger emoji font
        notes_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()