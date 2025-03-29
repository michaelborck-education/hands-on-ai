## Smart To-Do List

**Difficulty**: Intermediate  
**Time**: 60-75 minutes  
**Learning Focus**: Data structures, file I/O, date handling, AI assistance

### Overview

Build a smart to-do list application that helps users organize tasks with categories, priorities, and due dates. The application provides AI-assisted recommendations for task management and organization.

### Instructions

```python
import os
import json
from datetime import datetime, timedelta
from chatcraft import get_response

class SmartTodoList:
    """
    A smart to-do list that can categorize tasks, set priorities, 
    track due dates, and provide AI-assisted task management.
    """
    
    def __init__(self):
        self.tasks = []
        self.categories = ["Work", "School", "Personal", "Shopping", "Health", "Other"]
        self.priorities = ["High", "Medium", "Low"]
        self.data_dir = "todo_data"
        self.data_file = os.path.join(self.data_dir, "tasks.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing tasks if available
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from the data file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
                print(f"Loaded {len(self.tasks)} tasks from {self.data_file}")
            except json.JSONDecodeError:
                print("Error reading tasks file. Starting with empty task list.")
                self.tasks = []
        else:
            print("No existing tasks file found. Starting with empty task list.")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to the data file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
        print(f"Saved {len(self.tasks)} tasks to {self.data_file}")
    
    def add_task(self):
        """Add a new task to the list."""
        print("\n=== Add New Task ===")
        
        # Get task details
        title = input("Task title: ")
        
        # Select category
        print("\nCategories:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")
        
        category_choice = input(f"Select category (1-{len(self.categories)}): ")
        try:
            category_idx = int(category_choice) - 1
            category = self.categories[category_idx]
        except (ValueError, IndexError):
            print("Invalid category selection. Using 'Other'.")
            category = "Other"
        
        # Select priority
        print("\nPriorities:")
        for i, priority in enumerate(self.priorities, 1):
            print(f"{i}. {priority}")
        
        priority_choice = input(f"Select priority (1-{len(self.priorities)}): ")
        try:
            priority_idx = int(priority_choice) - 1
            priority = self.priorities[priority_idx]
        except (ValueError, IndexError):
            print("Invalid priority selection. Using 'Medium'.")
            priority = "Medium"
        
        # Set due date
        due_date = None
        has_due_date = input("\nDoes this task have a due date? (y/n): ").lower() == 'y'
        
        if has_due_date:
            date_format = "%Y-%m-%d"
            date_input = input("Enter due date (YYYY-MM-DD) or relative (e.g., 'tomorrow', '3 days'): ")
            
            try:
                # Parse relative dates
                if date_input.lower() == 'today':
                    due_date = datetime.now().strftime(date_format)
                elif date_input.lower() == 'tomorrow':
                    due_date = (datetime.now() + timedelta(days=1)).strftime(date_format)
                elif 'days' in date_input.lower():
                    # Parse "X days" format
                    try:
                        days = int(date_input.split()[0])
                        due_date = (datetime.now() + timedelta(days=days)).strftime(date_format)
                    except (ValueError, IndexError):
                        print("Could not parse relative date. Please enter a specific date.")
                else:
                    # Try to parse as YYYY-MM-DD
                    due_date = datetime.strptime(date_input, date_format).strftime(date_format)
            except ValueError:
                print("Invalid date format. Due date will not be set.")
        
        # Add notes
        notes = input("\nAdd any notes (optional): ")
        
        # Create task object
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "category": category,
            "priority": priority,
            "due_date": due_date,
            "notes": notes,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add to task list
        self.tasks.append(task)
        print(f"\nTask '{title}' added successfully!")
        
        # Save updated tasks
        self.save_tasks()
    
    def view_tasks(self, show_completed=False):
        """Display tasks based on filters."""
        if not self.tasks:
            print("\nNo tasks found.")
            return
        
        filtered_tasks = [t for t in self.tasks if t["completed"] == show_completed]
        
        if not filtered_tasks:
            status = "completed" if show_completed else "pending"
            print(f"\nNo {status} tasks found.")
            return
        
        # Sort tasks: first by due date (None at the end), then by priority
        def sort_key(task):
            # Priority order: High, Medium, Low
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            
            # Sort by due date first (None/null dates come last)
            if task["due_date"]:
                return (0, task["due_date"], priority_order.get(task["priority"], 1))
            else:
                return (1, "9999-99-99", priority_order.get(task["priority"], 1))
        
        sorted_tasks = sorted(filtered_tasks, key=sort_key)
        
        # Display tasks
        status = "Completed" if show_completed else "Pending"
        print(f"\n=== {status} Tasks ===")
        
        for i, task in enumerate(sorted_tasks, 1):
            due_str = f"Due: {task['due_date']}" if task['due_date'] else "No due date"
            
            # Add warning for tasks due today or overdue
            warning = ""
            if task['due_date']:
                try:
                    due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                    today = datetime.now().date()
                    
                    if due_date < today and not task['completed']:
                        warning = " [OVERDUE!]"
                    elif due_date == today and not task['completed']:
                        warning = " [DUE TODAY!]"
                except ValueError:
                    pass
            
            print(f"{i}. [{task['priority']}] {task['title']}{warning} - {due_str} ({task['category']})")
        
        # Return the sorted tasks for selection
        return sorted_tasks
    
    def toggle_task_status(self):
        """Mark a task as completed or pending."""
        print("\n=== Toggle Task Status ===")
        
        # Show pending tasks first
        pending_tasks = self.view_tasks(show_completed=False)
        
        if pending_tasks:
            # Show completed tasks
            print("\n=== Completed Tasks ===")
            completed_tasks = self.view_tasks(show_completed=True)
            
            # Ask which list to toggle from
            toggle_from = input("\nToggle task from (p)ending or (c)ompleted list? ").lower()
            
            if toggle_from == 'p' and pending_tasks:
                task_list = pending_tasks
                current_status = False
            elif toggle_from == 'c' and completed_tasks:
                task_list = completed_tasks
                current_status = True
            else:
                print("Invalid selection or no tasks in that category.")
                return
            
            # Get task number
            task_num = input(f"Enter task number to toggle (1-{len(task_list)}): ")
            try:
                idx = int(task_num) - 1
                selected_task = task_list[idx]
                
                # Find this task in the main task list and toggle its status
                for task in self.tasks:
                    if task["id"] == selected_task["id"]:
                        task["completed"] = not current_status
                        status = "completed" if task["completed"] else "pending"
                        print(f"\nTask '{task['title']}' marked as {status}.")
                        break
                
                # Save updated tasks
                self.save_tasks()
                
            except (ValueError, IndexError):
                print("Invalid task number.")
    
    def edit_task(self):
        """Edit an existing task."""
        print("\n=== Edit Task ===")
        
        # Show all tasks for selection
        print("\nAll Tasks:")
        all_tasks = self.tasks.copy()
        
        # Sort tasks by completion status, then by other criteria
        def sort_key(task):
            return (task["completed"], task.get("due_date", "9999-99-99"), task["priority"])
        
        sorted_tasks = sorted(all_tasks, key=sort_key)
        
        for i, task in enumerate(sorted_tasks, 1):
            status = "✓" if task["completed"] else "☐"
            due_str = f"Due: {task['due_date']}" if task['due_date'] else "No due date"
            print(f"{i}. {status} [{task['priority']}] {task['title']} - {due_str} ({task['category']})")
        
        # Get task to edit
        task_num = input(f"\nEnter task number to edit (1-{len(sorted_tasks)}): ")
        try:
            idx = int(task_num) - 1
            selected_task = sorted_tasks[idx]
            
            print(f"\nEditing task: {selected_task['title']}")
            
            # Get updated values
            title = input(f"Title [{selected_task['title']}]: ") or selected_task['title']
            
            # Select category
            print("\nCategories:")
            for i, category in enumerate(self.categories, 1):
                print(f"{i}. {category}")
            
            category_choice = input(f"Select category [current: {selected_task['category']}]: ")
            if category_choice:
                try:
                    category_idx = int(category_choice) - 1
                    category = self.categories[category_idx]
                except (ValueError, IndexError):
                    print("Invalid category selection. Keeping current category.")
                    category = selected_task['category']
            else:
                category = selected_task['category']
            
            # Select priority
            print("\nPriorities:")
            for i, priority in enumerate(self.priorities, 1):
                print(f"{i}. {priority}")
            
            priority_choice = input(f"Select priority [current: {selected_task['priority']}]: ")
            if priority_choice:
                try:
                    priority_idx = int(priority_choice) - 1
                    priority = self.priorities[priority_idx]
                except (ValueError, IndexError):
                    print("Invalid priority selection. Keeping current priority.")
                    priority = selected_task['priority']
            else:
                priority = selected_task['priority']
            
            # Update due date
            current_due = selected_task['due_date'] or "None"
            due_choice = input(f"Update due date? Current: {current_due} (y/n): ").lower()
            
            if due_choice == 'y':
                date_format = "%Y-%m-%d"
                date_input = input("Enter due date (YYYY-MM-DD) or relative (e.g., 'tomorrow', '3 days'): ")
                
                try:
                    # Parse relative dates
                    if date_input.lower() == 'today':
                        due_date = datetime.now().strftime(date_format)
                    elif date_input.lower() == 'tomorrow':
                        due_date = (datetime.now() + timedelta(days=1)).strftime(date_format)
                    elif 'days' in date_input.lower():
                        # Parse "X days" format
                        try:
                            days = int(date_input.split()[0])
                            due_date = (datetime.now() + timedelta(days=days)).strftime(date_format)
                        except (ValueError, IndexError):
                            print("Could not parse relative date. Keeping current due date.")
                            due_date = selected_task['due_date']
                    elif date_input.lower() in ('none', 'remove', 'clear'):
                        due_date = None
                    else:
                        # Try to parse as YYYY-MM-DD
                        due_date = datetime.strptime(date_input, date_format).strftime(date_format)
                except ValueError:
                    print("Invalid date format. Keeping current due date.")
                    due_date = selected_task['due_date']
            else:
                due_date = selected_task['due_date']
            
            # Update notes
            current_notes = selected_task['notes'] or "None"
            notes_choice = input(f"Update notes? Current: {current_notes} (y/n): ").lower()
            
            if notes_choice == 'y':
                notes = input("Enter new notes: ")
            else:
                notes = selected_task['notes']
            
            # Find this task in the main task list and update it
            for task in self.tasks:
                if task["id"] == selected_task["id"]:
                    task["title"] = title
                    task["category"] = category
                    task["priority"] = priority
                    task["due_date"] = due_date
                    task["notes"] = notes
                    print(f"\nTask '{title}' updated successfully!")
                    break
            
            # Save updated tasks
            self.save_tasks()
            
        except (ValueError, IndexError):
            print("Invalid task number.")
    
    def delete_task(self):
        """Delete a task from the list."""
        print("\n=== Delete Task ===")
        
        # Show all tasks for selection
        print("\nAll Tasks:")
        all_tasks = self.tasks.copy()
        
        # Sort tasks by completion status, then by other criteria
        def sort_key(task):
            return (task["completed"], task.get("due_date", "9999-99-99"), task["priority"])
        
        sorted_tasks = sorted(all_tasks, key=sort_key)
        
        for i, task in enumerate(sorted_tasks, 1):
            status = "✓" if task["completed"] else "☐"
            due_str = f"Due: {task['due_date']}" if task['due_date'] else "No due date"
            print(f"{i}. {status} [{task['priority']}] {task['title']} - {due_str} ({task['category']})")
        
        # Get task to delete
        task_num = input(f"\nEnter task number to delete (1-{len(sorted_tasks)}): ")
        try:
            idx = int(task_num) - 1
            selected_task = sorted_tasks[idx]
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete '{selected_task['title']}'? (y/n): ").lower()
            
            if confirm == 'y':
                # Remove task from list
                self.tasks = [t for t in self.tasks if t["id"] != selected_task["id"]]
                print(f"\nTask '{selected_task['title']}' deleted successfully!")
                
                # Save updated tasks
                self.save_tasks()
            else:
                print("Deletion cancelled.")
            
        except (ValueError, IndexError):
            print("Invalid task number.")
    
    def get_ai_recommendations(self):
        """Get AI-assisted recommendations for task management."""
        if not self.tasks:
            print("\nNo tasks found. Please add some tasks first.")
            return
        
        print("\n=== AI Task Management Recommendations ===")
        print("Analyzing your tasks...")
        
        try:
            # Prepare task data for AI
            today = datetime.now().date()
            
            # Count tasks by category
            category_counts = {}
            for task in self.tasks:
                cat = task["category"]
                if cat in category_counts:
                    category_counts[cat] += 1
                else:
                    category_counts[cat] = 1
            
            # Count overdue tasks
            overdue_tasks = []
            for task in self.tasks:
                if task["due_date"] and not task["completed"]:
                    try:
                        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                        if due_date < today:
                            overdue_tasks.append({
                                "title": task["title"],
                                "due_date": task["due_date"],
                                "days_overdue": (today - due_date).days,
                                "priority": task["priority"]
                            })
                    except ValueError:
                        pass
            
            # Get tasks due today
            today_tasks = []
            for task in self.tasks:
                if task["due_date"] and not task["completed"]:
                    try:
                        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                        if due_date == today:
                            today_tasks.append({
                                "title": task["title"],
                                "priority": task["priority"],
                                "category": task["category"]
                            })
                    except ValueError:
                        pass
            
            # Get high priority tasks
            high_priority = []
            for task in self.tasks:
                if task["priority"] == "High" and not task["completed"]:
                    high_priority.append({
                        "title": task["title"],
                        "due_date": task["due_date"],
                        "category": task["category"]
                    })
            
            # Create prompt for AI
            prompt = f"""
            Based on the following task data, please provide helpful task management recommendations:
            
            Task summary:
            - Total tasks: {len(self.tasks)}
            - Completed tasks: {sum(1 for t in self.tasks if t["completed"])}
            - Pending tasks: {sum(1 for t in self.tasks if not t["completed"])}
            
            Category breakdown: {category_counts}
            
            Overdue tasks ({len(overdue_tasks)}):
            {overdue_tasks if overdue_tasks else "None"}
            
            Tasks due today ({len(today_tasks)}):
            {today_tasks if today_tasks else "None"}
            
            High priority pending tasks ({len(high_priority)}):
            {high_priority if high_priority else "None"}
            
            Please provide:
            1. A prioritized action plan for the next 24 hours
            2. Task management tips based on the current workload
            3. Suggestions for which tasks to focus on first
            
            Keep your response friendly, practical and under 300 words.
            """
            
            # Get AI recommendations
            recommendations = get_response(prompt)
            print("\n" + recommendations)
            
        except Exception as e:
            print(f"Error getting AI recommendations: {e}")
            print("Unable to generate AI recommendations at this time.")
    
    def run(self):
        """Run the main to-do list interface."""
        print("=== Smart To-Do List ===")
        
        while True:
            print("\nOptions:")
            print("1. Add new task")
            print("2. View pending tasks")
            print("3. View completed tasks")
            print("4. Toggle task status")
            print("5. Edit task")
            print("6. Delete task")
            print("7. Get AI recommendations")
            print("8. Exit")
            
            choice = input("\nSelect an option (1-8): ")
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks(show_completed=False)
            elif choice == '3':
                self.view_tasks(show_completed=True)
            elif choice == '4':
                self.toggle_task_status()
            elif choice == '5':
                self.edit_task()
            elif choice == '6':
                self.delete_task()
            elif choice == '7':
                self.get_ai_recommendations()
            elif choice == '8':
                print("\nExiting Smart To-Do List. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 8.")

# Run the to-do list
if __name__ == "__main__":
    todo_list = SmartTodoList()
    todo_list.run()
```

### Extension Ideas

- Add recurring tasks (daily, weekly, monthly)
- Implement task dependencies (tasks that require other tasks to be completed first)
- Create a calendar view to visualize task distribution
- Add a Pomodoro timer feature for focused work sessions
- Implement task sharing or collaboration features
- Create a mobile-friendly web interface using a framework like Flask

---