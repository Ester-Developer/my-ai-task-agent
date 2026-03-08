tasks = []
task_id_counter = 1

def add_task(title: str, description: str = "", task_type: str = "general", status: str = "pending", **kwargs):
    global task_id_counter
    if not title:
        return None
    task = {
        "id": task_id_counter,
        "title": title,
        "description": description,
        "type": task_type,
        "status": status
    }
    tasks.append(task)
    task_id_counter += 1
    return task

def get_tasks(status: str = None, task_type: str = None, sort_by: str = None):
    filtered = tasks
    if status:
        filtered = [t for t in filtered if t['status'] == status]
    if task_type:
        filtered = [t for t in filtered if t['type'] == task_type]
    
    if sort_by == "title":
        filtered = sorted(filtered, key=lambda x: x.get('title', "").lower())
    return filtered

def update_task(task_id: int, **updates):
    for task in tasks:
        if task['id'] == task_id:
            for k, v in updates.items():
                if k in task and v is not None:
                    task[k] = v
            return task
    return None

def delete_task(task_id: int):
    global tasks
    initial_len = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    return len(tasks) < initial_len