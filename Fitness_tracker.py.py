import tkinter as tk
from tkinter import messagebox, ttk
import os
import json

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} - {self.duration} min, {self.calories_burned} cal"

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []
        self.load_data()

    def add_workout(self, workout):
        self.workouts.append(workout)
        self.save_data()

    def get_workouts(self):
        return [str(workout) for workout in self.workouts]

    def save_data(self, filename="workouts.json"):
        with open(filename, 'w') as file:
            json.dump([vars(workout) for workout in self.workouts], file)

    def load_data(self, filename="workouts.json"):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                self.workouts = [Workout(**item) for item in data]

class WorkoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏋️ Fitness Tracker")
        self.root.geometry("500x500")
        self.root.configure(bg="#F0F8FF")

        self.user = None

        # Custom Styles
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5, background="#A0C4FF")
        style.map("TButton", background=[("active", "#76a5af")])

        # Title
        self.title_label = tk.Label(root, text="🏋️ Workout Tracker", font=("Arial", 16, "bold"), bg="#F0F8FF", fg="#333")
        self.title_label.pack(pady=10)

        # Form Frame
        self.form_frame = tk.Frame(root, bg="#FFFFFF", padx=15, pady=15, relief="ridge", borderwidth=2)
        self.form_frame.pack(pady=5, fill="both")

        # Input Fields
        self.create_label_entry("Enter Name:", 0)
        self.create_label_entry("Enter Age:", 1)
        self.create_label_entry("Enter Weight (kg):", 2)

        # Create User Button
        self.create_user_btn = ttk.Button(root, text="Create Profile", command=self.create_user)
        self.create_user_btn.pack(pady=5)

        # Workout List
        self.workout_listbox = tk.Listbox(root, width=50, height=8, bg="#FFD6A5", font=("Arial", 11), relief="ridge", borderwidth=2)
        self.workout_listbox.pack(pady=5)
        self.workout_listbox.bind("<Double-Button-1>", self.edit_workout)

        # Buttons Frame
        self.button_frame = tk.Frame(root, bg="#F0F8FF")
        self.button_frame.pack(pady=5)

        # Action Buttons
        self.add_workout_btn = ttk.Button(self.button_frame, text="➕ Add Workout", command=self.add_workout, state=tk.DISABLED)
        self.add_workout_btn.grid(row=0, column=0, padx=5, pady=5)

        self.save_btn = ttk.Button(self.button_frame, text="💾 Save Workouts", command=self.save_workouts, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=1, padx=5, pady=5)

    def create_label_entry(self, text, row):
        tk.Label(self.form_frame, text=text, font=("Arial", 11), bg="#FFFFFF").grid(row=row, column=0, sticky="w", pady=2)
        entry = ttk.Entry(self.form_frame)
        entry.grid(row=row, column=1, pady=2)
        setattr(self, f"entry_{row}", entry)

    def create_user(self):
        name = self.entry_0.get()
        age = self.entry_1.get()
        weight = self.entry_2.get()

        if name and age.isdigit() and weight.replace('.', '', 1).isdigit():
            self.user = User(name, int(age), float(weight))
            self.add_workout_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)
            self.load_workouts()
            messagebox.showinfo("Success", "User profile created!")
        else:
            messagebox.showerror("Error", "Invalid input. Please enter valid details.")

    def add_workout(self, workout=None, index=None):
        if not self.user:
            return
        
        workout_window = tk.Toplevel(self.root)
        workout_window.title("Add/Edit Workout")
        workout_window.geometry("300x200")
        
        fields = ["Date (YYYY-MM-DD):", "Exercise Type:", "Duration (minutes):", "Calories Burned:"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(workout_window, text=field, font=("Arial", 10)).grid(row=i, column=0, padx=5, pady=3)
            entry = ttk.Entry(workout_window)
            entry.grid(row=i, column=1, padx=5, pady=3)
            entries[field] = entry

        if workout:
            entries["Date (YYYY-MM-DD):"].insert(0, workout.date)
            entries["Exercise Type:"].insert(0, workout.exercise_type)
            entries["Duration (minutes):"].insert(0, str(workout.duration))
            entries["Calories Burned:"].insert(0, str(workout.calories_burned))

        def save_workout():
            date = entries["Date (YYYY-MM-DD):"].get()
            exercise_type = entries["Exercise Type:"].get()
            duration = entries["Duration (minutes):"].get()
            calories_burned = entries["Calories Burned:"].get()

            if date and exercise_type and duration.isdigit() and calories_burned.isdigit():
                if workout:
                    workout.date = date
                    workout.exercise_type = exercise_type
                    workout.duration = int(duration)
                    workout.calories_burned = int(calories_burned)
                    self.user.save_data()
                    self.load_workouts()
                else:
                    new_workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                    self.user.add_workout(new_workout)
                    self.workout_listbox.insert(tk.END, str(new_workout))
                
                workout_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid input. Please enter valid details.")

        ttk.Button(workout_window, text="Save Workout", command=save_workout).grid(row=4, column=0, columnspan=2, pady=5)

    def load_workouts(self):
        if not self.user:
            return
        self.workout_listbox.delete(0, tk.END)
        for workout in self.user.get_workouts():
            self.workout_listbox.insert(tk.END, workout)

    def edit_workout(self, event):
        selected_index = self.workout_listbox.curselection()
        if not selected_index:
            return
        index = selected_index[0]
        workout = self.user.workouts[index]
        self.add_workout(workout, index)

    def save_workouts(self):
        if not self.user:
            messagebox.showerror("Error", "No user profile found. Create a profile first.")
            return
        self.user.save_data()
        messagebox.showinfo("Success", "Workouts saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutApp(root)
    root.mainloop()
