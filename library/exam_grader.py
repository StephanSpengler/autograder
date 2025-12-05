import csv
import importlib.util
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
import types
from typing import Callable
import platform
from pathlib import Path

Task = tuple[str, Callable[[types.ModuleType], str], list[float]]

def init(submissions_root: str, output_path: str, submission_file: str, tasks: list[Task]):
    grades = _load_grades(output_path)

    # Fetch student list and skip already graded
    students = sorted(os.listdir(submissions_root))
    
    labels = [task_id for task_id, *_ in tasks]
    def load(i):
        i = i % len(students)
        student = students[i]
        _load_student(
            i,
            student,
            submissions_root,
            submission_file,
            tasks,
            grades[student].copy() if student in grades else {},
            lambda score: (grades.update({student: score}), _save_grades(output_path, labels, grades)),
            load,
        )
    load(0)

def _open_file(path):
    path = Path(path)
    if platform.system() == "Windows":
        os.startfile(path) # type: ignore (Windows-only)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", str(path)])
    else:  # Linux / Unix
        subprocess.run(["xdg-open", str(path)])

def _save_grades(csv_path, labels, grades):
    fieldnames = ["student"] + labels
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for student, scores in grades.items():
            row = {"student": student}
            row.update({k: v for k, v in scores.items()})
            writer.writerow(row)

def _load_grades(csv_path):
    if not os.path.exists(csv_path):
        return {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        return {row["student"]: row for row in reader}

def _import_submission(file_path):
    spec = importlib.util.spec_from_file_location("student", file_path)
    if spec is None:
        raise ImportError(f"Could not load spec from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["student"] = module
    loader = spec.loader
    if loader is None:
        raise ImportError(f"No loader for spec from {file_path}")
    loader.exec_module(module)
    return module

def _truncate(text):
    if text is None:
        return ""
    s = str(text)
    lines = s.splitlines()
    max_chars = 200
    out = []
    for line in lines:
        if len(line) > max_chars:
            out.append(line[: max_chars - 3] + "...")
        else:
            out.append(line)
    return "\n".join(out)

def _load_student(i, student, submissions_root, submission_file, tasks, scores, onSave, load):
    # Load submission
    file_path = os.path.join(submissions_root, student, submission_file)
    results = None
    if not os.path.exists(file_path):
        status = f"Submission file not found."
    else:
        # Open submission in default editor
        _open_file(file_path)

        # Run tests
        try:
            module = _import_submission(file_path)
            results = {}
            for task_id, task_test, _ in tasks:
                try:
                    results[task_id] = task_test(module)
                except Exception as e:
                    results[task_id] = f"Error during testing: {e}"
            status = "Tests completed."
        except Exception as e:
            status = f"Error loading submission: {e}"

    # Open grading window        
    root = tk.Tk()
    tk.Label(root, text=f"Grading: {student}", font=("Arial", 14, "bold")).pack()
    frame = tk.Frame(root)
    frame.pack(pady=10)

    changed = False

    def save():
        onSave(scores)
        nonlocal changed
        changed = False

    def _set_score(task_id, value, entry):
        nonlocal changed
        if value.strip() == "":
            if task_id in scores:
                del scores[task_id]
                changed = True
            return
        try:
            scores[task_id] = float(value)
            changed = True
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
        except ValueError:
            messagebox.showerror("Invalid input", f"{value} is not a valid score")
    
    box = tk.Frame(frame)
    box.pack(fill="x", pady=2)
    for (row_id, (task_id, _, grading_scheme)) in enumerate(tasks):
        # Frame around each task for visual separation
        task_frame = tk.Frame(box, bd=1, relief="solid", padx=6, pady=6)
        task_frame.pack(fill="x", pady=6)

        # Header: task name, score entry and preset buttons
        header = tk.Frame(task_frame)
        header.pack(fill="x")
        tk.Label(header, text=task_id, font=("Arial", 11, "bold")).pack(side="left", anchor="w")

        var = tk.StringVar()
        var.set(scores.get(task_id, ""))
        entry = tk.Entry(header, width=6, textvariable=var)
        entry.pack(side="left", padx=8)
        var.trace_add("write", lambda *_, e=entry, tid=task_id, v=var: _set_score(tid, v.get(), e))

        for val in grading_scheme:
            b = tk.Button(header, text=str(val), command=lambda vl=val, vr=var: vr.set(vl))
            b.pack(side="left", padx=3)

        # Test output shown below the header
        output_text = _truncate(results[task_id] if results is not None else status)
        line_count = len(output_text.splitlines())
        
        if line_count > 10:
            # Use scrollable Text widget for long output
            text_frame = tk.Frame(task_frame)
            text_frame.pack(fill="both", expand=True, pady=(8, 0))
            
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side="right", fill="y")
            
            text_widget = tk.Text(text_frame, height=8, wrap="word", yscrollcommand=scrollbar.set, bg="lightgray")
            text_widget.insert("1.0", output_text)
            text_widget.config(state="disabled")
            text_widget.pack(side="left", fill="both", expand=True)
            text_widget.configure(font=("Arial", 11))
            
            scrollbar.config(command=text_widget.yview)
        else:
            # Use simple Label for short output
            out_label = tk.Label(task_frame, text=output_text, anchor="w", justify="left", wraplength=900)
            out_label.pack(fill="x", pady=(8, 0))
    
    btns = tk.Frame(root)
    btns.pack(pady=10)

    def _navigate_and_maybe_save(target_index=None):
        nonlocal changed
        if changed and messagebox.askyesno("Save changes?", "Save changes before moving?"):
            save()
        if target_index is None:
            target_index = int(simpledialog.askstring("Skip to", "Enter student index (0-based):") or 0)
        root.destroy()
        load(target_index)

    tk.Button(btns, text="Prev", command=lambda: _navigate_and_maybe_save(i-1)).pack(side="left", padx=5)
    tk.Button(btns, text="Reload", command=lambda: _navigate_and_maybe_save(i)).pack(side="left", padx=5)
    tk.Button(btns, text="Save", command=save).pack(side="left", padx=5)
    tk.Button(btns, text="Next", command=lambda: _navigate_and_maybe_save(i+1)).pack(side="left", padx=5)
    tk.Button(btns, text="Skip to...", command=lambda: _navigate_and_maybe_save()).pack(side="left", padx=5)
    root.mainloop()