"""
Programmer: Adivhaho Munaka
Date: 2026-05-05
Program Purpose:
Learner Progress Tracking System (LPTS) for managing learners, marks,
performance, and progress summaries using OOP, lists, loops, functions,
recursion, and exception handling.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox as msg
from tkinter import ttk

# -------------------------------
# PERSON CLASS (BASE CLASS)
# -------------------------------
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# -------------------------------
# LEARNER CLASS (INHERITS PERSON)
# -------------------------------
class Learner(Person):
    def __init__(self, learner_id, name, age, course):
        super().__init__(name, age)
        self.learner_id = str(learner_id)  # Ensure string type
        self.course = course
        self.marks = []

        # Encapsulated attribute
        self._average = 0

    # Encapsulation: getter
    def get_average(self):
        return self._average

    # Encapsulation: setter
    def set_average(self, avg):
        self._average = avg

    # Predicate function
    def has_passed(self):
        return self._average >= 50


# -------------------------------
# RECURSIVE FUNCTION (OPTIMIZED)
# -------------------------------
def recursive_sum(marks, index=0):
    """Calculate sum of marks recursively."""
    if index == len(marks):
        return 0
    return marks[index] + recursive_sum(marks, index + 1)


# Alternative: Efficient sum (recommended for large datasets)
def calculate_sum(marks):
    """Use built-in sum for efficiency."""
    return sum(marks) if marks else 0


# -------------------------------
# SEARCH FUNCTION (KEYWORD ARGUMENT)
# -------------------------------
def search_learner(learners, *, learner_id):
    """Search for learner by ID."""
    learner_id = str(learner_id)  # Ensure consistent type
    for learner in learners:
        if learner.learner_id == learner_id:
            return learner
    return None


# -------------------------------
# ADD LEARNER
# -------------------------------
def add_learner(learners):
    """Add a new learner to the system."""
    try:
        learner_id = simpledialog.askstring("Input", "Enter learner ID:")
        if not learner_id:
            return

        name = simpledialog.askstring("Input", "Enter learner name:")
        if not name:
            return

        age_str = simpledialog.askstring("Input", "Enter learner age:")
        if not age_str:
            return

        age = int(age_str)

        if age < 5 or age > 100:
            msg.showerror("Error", "Invalid age. Must be between 5 and 100.")
            return

        course = simpledialog.askstring("Input", "Enter course name:")
        if not course:
            return

        # Check if learner ID already exists
        if search_learner(learners, learner_id=learner_id):
            msg.showerror("Error", "Learner ID already exists.")
            return

        new_learner = Learner(learner_id, name, age, course)
        learners.append(new_learner)

        msg.showinfo("Success", "Learner added successfully.")

    except ValueError:
        msg.showerror("Error", "Invalid numeric input for age.")
    except Exception as e:
        msg.showerror("Error", f"An unexpected error occurred: {str(e)}")


# -------------------------------
# ENTER MARKS
# -------------------------------
def enter_marks(learners):
    """Enter marks for a learner."""
    try:
        learner_id = simpledialog.askstring("Input", "Enter learner ID:")
        if not learner_id:
            return

        learner = search_learner(learners, learner_id=learner_id)

        if learner is None:
            msg.showerror("Error", "Learner not found.")
            return

        count_str = simpledialog.askstring("Input", "How many marks do you want to enter?")
        if not count_str:
            return

        count = int(count_str)

        if count <= 0:
            msg.showerror("Error", "Number of marks must be positive.")
            return

        for i in range(count):
            mark_str = simpledialog.askstring("Input", f"Enter mark {i+1} (0-100):")
            if mark_str is None:
                break

            try:
                mark = float(mark_str)

                if mark < 0 or mark > 100:
                    msg.showwarning("Warning", f"Invalid mark {mark}. Must be 0-100. Skipped.")
                    continue

                learner.marks.append(mark)
            except ValueError:
                msg.showwarning("Warning", "Invalid mark entry. Skipped.")

        msg.showinfo("System Message", "Marks captured successfully.")

    except ValueError:
        msg.showerror("Error", "Invalid input.")
    except Exception as e:
        msg.showerror("Error", f"An unexpected error occurred: {str(e)}")


# -------------------------------
# CALCULATE AVERAGE
# -------------------------------
def calculate_average(learner):
    """Calculate and set the average for a learner."""
    if len(learner.marks) == 0:
        learner.set_average(0)
        return 0

    total = calculate_sum(learner.marks)  # Use efficient sum
    avg = total / len(learner.marks)
    learner.set_average(avg)
    return avg


# -------------------------------
# VIEW ALL LEARNERS
# -------------------------------
def view_learners(learners):
    """Display all learners and their summaries."""
    if len(learners) == 0:
        msg.showinfo("View Learners", "No learners available.")
        return

    summary = ""
    for learner in learners:
        calculate_average(learner)
        
        if learner.get_average() >= 75:
            result = "Pass with Distinction"
        elif learner.get_average() >= 50:
            result = "Pass"
        else:
            result = "Fail"

        certificate = "Yes" if learner.get_average() >= 50 else "No"

        summary += f"\n{'='*40}\n"
        summary += f"Learner ID: {learner.learner_id}\n"
        summary += f"Name: {learner.name}\n"
        summary += f"Age: {learner.age}\n"
        summary += f"Course: {learner.course}\n"
        summary += f"Marks: {learner.marks}\n"
        summary += f"Average: {learner.get_average():.2f}\n"
        summary += f"Result: {result}\n"
        summary += f"Certificate: {certificate}\n"

    msg.showinfo("All Learners", summary)


# -------------------------------
# UPDATE LEARNER
# -------------------------------
def update_learner(learners):
    """Update learner details."""
    try:
        learner_id = simpledialog.askstring("Input", "Enter learner ID to update:")
        if not learner_id:
            return

        learner = search_learner(learners, learner_id=learner_id)

        if learner is None:
            msg.showerror("Error", "Learner not found.")
            return

        name = simpledialog.askstring("Input", "Enter new name:", initialvalue=learner.name)
        if name:
            learner.name = name

        age_str = simpledialog.askstring("Input", "Enter new age:", initialvalue=str(learner.age))
        if age_str:
            age = int(age_str)
            if 5 <= age <= 100:
                learner.age = age
            else:
                msg.showerror("Error", "Invalid age. Must be between 5 and 100.")
                return

        course = simpledialog.askstring("Input", "Enter new course:", initialvalue=learner.course)
        if course:
            learner.course = course

        msg.showinfo("Updated", "Learner details updated successfully.")

    except ValueError:
        msg.showerror("Error", "Invalid input.")
    except Exception as e:
        msg.showerror("Error", f"An unexpected error occurred: {str(e)}")


# -------------------------------
# REMOVE LEARNER
# -------------------------------
def remove_learner(learners):
    """Remove a learner from the system."""
    try:
        learner_id = simpledialog.askstring("Input", "Enter learner ID to remove:")
        if not learner_id:
            return

        learner = search_learner(learners, learner_id=learner_id)

        if learner is None:
            msg.showerror("Error", "Learner not found.")
            return

        confirm = msg.askyesno("Confirm", f"Are you sure you want to remove {learner.name}?")
        if confirm:
            learners.remove(learner)
            msg.showinfo("Deleted", "Learner removed successfully.")

    except Exception as e:
        msg.showerror("Error", f"An unexpected error occurred: {str(e)}")


# -------------------------------
# SHOW LEARNER RESULT
# -------------------------------
def show_result(learners):
    """Display the result for a specific learner."""
    try:
        learner_id = simpledialog.askstring("Input", "Enter learner ID:")
        if not learner_id:
            return

        learner = search_learner(learners, learner_id=learner_id)

        if learner is None:
            msg.showerror("Error", "Learner not found.")
            return

        avg = calculate_average(learner)

        if avg >= 75:
            performance = "Pass with Distinction"
        elif avg >= 50:
            performance = "Pass"
        else:
            performance = "Fail"

        result_msg = f"Name: {learner.name}\nAverage: {avg:.2f}\nPerformance: {performance}"
        msg.showinfo("Result", result_msg)

        if avg >= 50:
            msg.showinfo("Certificate", f"{learner.name} qualifies for a certificate!")
        else:
            msg.showinfo("Certificate", f"{learner.name} does NOT qualify for a certificate.")

    except Exception as e:
        msg.showerror("Error", f"An unexpected error occurred: {str(e)}")


# -------------------------------
# GUI APPLICATION CLASS
# -------------------------------
class LearnerTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learner Progress Tracking System")
        self.root.geometry("400x500")
        self.learners = []

        # Create menu frame
        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(frame, text="Learner Progress Tracking System", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        # Buttons
        buttons = [
            ("1. Add Learner", lambda: add_learner(self.learners)),
            ("2. Enter Marks", lambda: enter_marks(self.learners)),
            ("3. View All Learners", lambda: view_learners(self.learners)),
            ("4. Search Learner", self.search_learner_gui),
            ("5. Update Learner", lambda: update_learner(self.learners)),
            ("6. Remove Learner", lambda: remove_learner(self.learners)),
            ("7. Show Learner Result", lambda: show_result(self.learners)),
            ("8. Exit", self.exit_app),
        ]

        for text, command in buttons:
            btn = ttk.Button(frame, text=text, command=command, width=30)
            btn.pack(pady=5)

    def search_learner_gui(self):
        """GUI wrapper for search."""
        learner_id = simpledialog.askstring("Input", "Enter learner ID to search:")
        if learner_id:
            learner = search_learner(self.learners, learner_id=learner_id)
            if learner:
                view_learners([learner])
            else:
                msg.showerror("Error", "Learner not found.")

    def exit_app(self):
        """Exit the application."""
        if msg.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()


# -------------------------------
# MAIN ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = LearnerTrackingApp(root)
    root.mainloop()
