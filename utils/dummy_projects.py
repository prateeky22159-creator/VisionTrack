import pandas as pd
import random
import datetime

def generate_dummy_projects(num_projects=10, tasks_per_project=20):
    projects = []
    users = ["Prateek Yadav", "Ananya Sharma", "Ravi Kumar", "Neha Verma", "Arjun Singh", "Pooja Iyer"]
    statuses = ["To Do", "In Progress", "Done"]

    project_names = [
        "CRM_Upgrade", "Payment_Gateway", "Mobile_Banking_App", "HR_Management_System",
        "Ecommerce_Website", "Data_Warehouse", "Customer_Support_Portal", "Cybersecurity_Upgrade",
        "Cloud_Migration", "AI_Analytics_Platform"
    ]

    for project_key in project_names:
        for t in range(1, tasks_per_project + 1):
            task_id = f"{project_key}-{t}"
            task_name = f"{project_key} Task {t}"
            status = random.choice(statuses)
            assigned_to = random.choice(users)

            start_date = datetime.date.today() - datetime.timedelta(days=random.randint(1, 90))
            due_date = start_date + datetime.timedelta(days=random.randint(5, 30))
            planned_time = random.randint(4, 16)  # hours
            actual_time = planned_time + random.randint(-2, 6)

            resolution_date = None
            if status == "Done":
                resolution_date = due_date + datetime.timedelta(days=random.choice([-2, -1, 0, 2, 5]))

            delay_flag = "Yes" if resolution_date and resolution_date > due_date else "No"
            missed_timeline = "Yes" if status != "Done" and due_date < datetime.date.today() else "No"

            projects.append({
                "project_key": project_key,
                "task_id": task_id,
                "task_name": task_name,
                "status": status,
                "assigned_to": assigned_to,
                "start_date": start_date,
                "due_date": due_date,
                "resolution_date": resolution_date,
                "planned_time": planned_time,
                "actual_time": actual_time,
                "delay_flag": delay_flag,
                "missed_timeline": missed_timeline
            })

    return pd.DataFrame(projects)
