"""
Learner Progress Tracking System (LPTS)
Programmer: Adivhaho Munaka
Date: 2026-06-11
Purpose: Console-based learner tracking system with tkinter messagebox feedback.
Notes: Data stored in 'learners.txt' in JSON format for reliable persistence.
"""

import tkinter as tk
from tkinter import messagebox
import os
import json

# -------------------------
# Object Oriented Classes
# -------------------------

class Person:
    """Base class for people (simple: name and age)."""
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class Learner(Person):
    """
    Learner class inherits from Person.
    Attributes:
      learner_id : simple id (string or number stored as str)
      name, age, course (from Person + course)
      marks : list of floats
      _avg : protected attribute (encapsulated average)
    """
    def __init__(self, learner_id: str, name: str, age: int, course: str):
        super().__init__(name, age)
        self.learner_id = str(learner_id)
        self.course = course
        self.marks = []          # list to store marks
        self._avg = None         # protected attribute for average

    # Encapsulation: control access to average via method
    def calculate_average(self):
        """Calculate and store average in protected attribute. Returns average or None."""
        if not self.marks:
            self._avg = None
        else:
            self._avg = sum(self.marks) / len(self.marks)
        return self._avg

    def get_average(self):
        """Accessor for protected average attribute."""
        return self._avg

    def performance_result(self):
        """Return performance category based on average (assumes calculate_average called)."""
        avg = self.get_average()
        if avg is None:
            return "No marks"
        if avg < 50:
            return "Fail"
        elif avg < 75:
            return "Pass"
        else:
            return "Distinction"

    def qualifies_certificate(self):
        """Return True if qualifies for certificate (example rule: average >= 50)."""
        avg = self.get_average()
        return (avg is not None) and (avg >= 50)

    def to_dict(self):
        """Convert learner to dictionary for JSON serialization."""
        return {
            'learner_id': self.learner_id,
            'name': self.name,
            'age': self.age,
            'course': self.course,
            'marks': self.marks
        }

    @staticmethod
    def from_dict(data):
        """Create learner from dictionary."""
        L = Learner(data['learner_id'], data['name'], data['age'], data['course'])
        L.marks = data.get('marks', [])
        L.calculate_average()
        return L


# -------------------------
# File storage helpers
# -------------------------

DATA_FILE = "learners.txt"


def save_learners_to_file(learners):
    """
    Save learners to a JSON text file for reliable data persistence.
    Handles all data types correctly (strings, numbers, lists).
    """
    try:
        learner_dicts = [L.to_dict() for L in learners]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(learner_dicts, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save data: {e}")
        return False


def load_learners_from_file():
    """Load learners from JSON file and return a list of Learner objects."""
    learners = []
    if not os.path.exists(DATA_FILE):
        return learners
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            learners = [Learner.from_dict(item) for item in data]
    except json.JSONDecodeError:
        messagebox.showerror("Load Error", "Corrupted data file. Starting with empty list.")
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load data: {e}")
    return learners


# -------------------------
# Utility functions
# -------------------------

def is_valid_mark(mark):
    """Predicate function: returns True if mark is between 0 and 100."""
    try:
        m = float(mark)
        return 0.0 <= m <= 100.0
    except:
        return False


def sum_marks_recursive(marks, n=None):
    """
    Recursive function to sum marks.
    If n is None, start from full length.
    """
    if n is None:
        n = len(marks)
    # base case
    if n == 0:
        return 0.0
    # recursive case
    return marks[n-1] + sum_marks_recursive(marks, n-1)


def find_learner_by_id(learners, lid):
    """Search helper: returns learner or None."""
    lid = str(lid).strip()
    for L in learners:
        if L.learner_id == lid:
            return L
    return None


# -------------------------
# Core program functions
# -------------------------

def add_learner(learners):
    """Add a new learner (with validation)."""
    try:
        lid = input("Enter learner ID: ").strip()
        if lid == "":
            messagebox.showwarning("Invalid", "ID cannot be empty.")
            return
        # check duplicate
        if any(L.learner_id == lid for L in learners):
            messagebox.showwarning("Duplicate", "Learner ID already exists.")
            return
        name = input("Enter learner name: ").strip()
        if not name:
            messagebox.showwarning("Invalid", "Name cannot be empty.")
            return
        age_str = input("Enter learner age: ").strip()
        try:
            age = int(age_str)
            if age <= 0 or age > 120:
                raise ValueError("Age must be between 1 and 120.")
        except ValueError as ve:
            messagebox.showwarning("Invalid Age", f"Age must be a positive integer. {ve}")
            return
        course = input("Enter course name: ").strip()
        if not course:
            messagebox.showwarning("Invalid", "Course cannot be empty.")
            return
        L = Learner(lid, name, age, course)
        learners.append(L)
        if save_learners_to_file(learners):
            messagebox.showinfo("Success", "Learner added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not add learner: {e}")


def enter_marks(learners):
    """Enter marks for a learner (appends to existing marks)."""
    try:
        lid = input("Enter learner ID: ").strip()
        L = find_learner_by_id(learners, lid)
        if not L:
            messagebox.showwarning("Not found", "Learner not found.")
            return
        count_str = input("How many marks do you want to enter? ").strip()
        try:
            count = int(count_str)
            if count <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Invalid", "Enter a positive integer for count.")
            return
        for i in range(1, count + 1):
            while True:
                mark_str = input(f"Enter mark {i}: ").strip()
                if is_valid_mark(mark_str):
                    L.marks.append(float(mark_str))
                    break
                else:
                    print("Invalid mark. Enter a number between 0 and 100.")
                    # allow user to cancel entry
                    cont = input("Try again? (y/n): ").strip().lower()
                    if cont != "y":
                        break
        L.calculate_average()
        if save_learners_to_file(learners):
            messagebox.showinfo("Success", "Marks captured successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not enter marks: {e}")


def view_all_learners(learners):
    """Display summaries for all learners."""
    if not learners:
        print("No learners in the system.")
        messagebox.showinfo("View Learners", "No learners in the system.")
        return
    print("\n" + "="*50)
    print("LEARNER SUMMARY")
    print("="*50)
    for L in learners:
        L.calculate_average()
        avg = L.get_average()
        avg_str = f"{avg:.2f}" if avg is not None else "N/A"
        print(f"\nLearner ID: {L.learner_id}")
        print(f"Name: {L.name}")
        print(f"Age: {L.age}")
        print(f"Course: {L.course}")
        print(f"Marks: {L.marks}")
        print(f"Average: {avg_str}")
        print(f"Result: {L.performance_result()}")
        print(f"Certificate: {'Yes' if L.qualifies_certificate() else 'No'}")
        print("-" * 50)


def search_learner(learners):
    """Search and display a single learner by ID."""
    lid = input("Enter learner ID to search: ").strip()
    L = find_learner_by_id(learners, lid)
    if not L:
        messagebox.showwarning("Not found", "Learner not found.")
        return
    L.calculate_average()
    avg = L.get_average()
    avg_str = f"{avg:.2f}" if avg is not None else "N/A"
    print("\n" + "="*50)
    print("LEARNER DETAILS")
    print("="*50)
    print(f"Learner ID: {L.learner_id}")
    print(f"Name: {L.name}")
    print(f"Age: {L.age}")
    print(f"Course: {L.course}")
    print(f"Marks: {L.marks}")
    print(f"Average: {avg_str}")
    print(f"Result: {L.performance_result()}")
    print(f"Certificate: {'Yes' if L.qualifies_certificate() else 'No'}")
    print("="*50)


def update_learner(learners):
    """Update name, age, course for a learner."""
    lid = input("Enter learner ID to update: ").strip()
    L = find_learner_by_id(learners, lid)
    if not L:
        messagebox.showwarning("Not found", "Learner not found.")
        return
    print(f"\nCurrent details - Name: {L.name}, Age: {L.age}, Course: {L.course}")
    new_name = input("Enter new name (leave blank to keep current): ").strip()
    new_age = input("Enter new age (leave blank to keep current): ").strip()
    new_course = input("Enter new course (leave blank to keep current): ").strip()
    
    if new_name:
        L.name = new_name
    if new_age:
        try:
            age_val = int(new_age)
            if 1 <= age_val <= 120:
                L.age = age_val
            else:
                messagebox.showwarning("Invalid", "Age must be between 1 and 120. Keeping old age.")
        except:
            messagebox.showwarning("Invalid", "Age must be integer. Keeping old age.")
    if new_course:
        L.course = new_course
    
    if save_learners_to_file(learners):
        messagebox.showinfo("Updated", "Learner details updated successfully.")


def remove_learner(learners):
    """Remove a learner by ID."""
    lid = input("Enter learner ID to remove: ").strip()
    L = find_learner_by_id(learners, lid)
    if not L:
        messagebox.showwarning("Not found", "Learner not found.")
        return
    confirm = input(f"Are you sure you want to remove {L.name}? (y/n): ").strip().lower()
    if confirm == "y":
        learners.remove(L)
        if save_learners_to_file(learners):
            messagebox.showinfo("Deleted", "Learner removed successfully.")
    else:
        print("Removal cancelled.")


def show_learner_result(learners):
    """Show result and certificate eligibility for a learner."""
    lid = input("Enter learner ID: ").strip()
    L = find_learner_by_id(learners, lid)
    if not L:
        messagebox.showwarning("Not found", "Learner not found.")
        return
    L.calculate_average()
    avg = L.get_average()
    avg_str = f"{avg:.2f}" if avg is not None else "N/A"
    print(f"\n{'='*50}")
    print(f"Result for {L.name}")
    print(f"Average: {avg_str}")
    print(f"Performance: {L.performance_result()}")
    print(f"{'='*50}\n")
    # messagebox feedback
    if L.qualifies_certificate():
        messagebox.showinfo("Result", f"{L.name} qualifies for a certificate.\nAverage: {avg_str}\nPerformance: {L.performance_result()}")
    else:
        messagebox.showinfo("Result", f"{L.name} does not qualify for a certificate.\nAverage: {avg_str}\nPerformance: {L.performance_result()}")


def greet_user(name="Staff", loud=False):
    """Example function: default argument and keyword argument usage."""
    msg = f"Hello, {name}"
    if loud:
        msg = msg.upper()
    print(msg)


# -------------------------
# Main menu (condition-controlled loop)
# -------------------------

def main_menu():
    """Main menu loop for the application."""
    # load learners from file at start
    learners = load_learners_from_file()
    print(f"Loaded {len(learners)} learner(s) from {DATA_FILE}")

    # create a hidden tkinter root for messageboxes
    root = tk.Tk()
    root.withdraw()  # hide main window

    while True:
        print("\n" + "="*50)
        print("LEARNER PROGRESS TRACKING SYSTEM")
        print("="*50)
        print("1. Add learner")
        print("2. Enter marks")
        print("3. View all learners")
        print("4. Search learner")
        print("5. Update learner")
        print("6. Remove learner")
        print("7. Show learner result")
        print("8. Exit")
        print("="*50)
        choice = input("Enter your choice (1-8): ").strip()
        
        # handle invalid menu selection with exception handling
        try:
            if choice == "1":
                add_learner(learners)
            elif choice == "2":
                enter_marks(learners)
            elif choice == "3":
                view_all_learners(learners)
            elif choice == "4":
                search_learner(learners)
            elif choice == "5":
                update_learner(learners)
            elif choice == "6":
                remove_learner(learners)
            elif choice == "7":
                show_learner_result(learners)
            elif choice == "8":
                # confirm exit with messagebox
                if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                    if save_learners_to_file(learners):
                        print("Data saved successfully.")
                    print("Goodbye.")
                    break
                else:
                    continue
            else:
                print("Invalid choice. Please enter a number 1-8.")
        except Exception as e:
            # catch-all to avoid program crash
            messagebox.showerror("Error", f"An error occurred: {e}")

    # destroy hidden root before exit
    root.destroy()


# -------------------------
# Run program
# -------------------------
if __name__ == "__main__":
    # small demo of keyword/default argument usage
    greet_user()  # default
    greet_user("Admin", loud=True)  # keyword-like usage
    print()
    main_menu()
