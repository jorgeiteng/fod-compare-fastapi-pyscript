# fod-compare-fastapi-pyscript service
from datetime import datetime as dt

from utils import add_class, remove_class, get_JSON_Fetch
import asyncio

tasks = []

# define the task template that will be use to render new templates to the page
task_template = Element("task-template").select(".task", from_content=True)
task_list = Element("list-tasks-container")
new_task_content = Element("new-task-content")
releaseid1 = Element("releaseid1") 
releaseid2 = Element("releaseid2") 

async def fill_tasks(*ags, **kws):
    files_list = await req_differences(releaseid1.element.value, releaseid2.element.value)

    for file_name in files_list:
        add_task(file_name)
    
    releaseid1.clear()
    releaseid2.clear()

def add_task(content):
    # ignore empty task
    #if not releaseid1.element.value:
    #    return None

    # create task
    task_id = f"task-{len(tasks)}"
    task = {
        "id": task_id,
        "content": content,
        "done": False,
        "created_at": dt.now(),
    }

    tasks.append(task)
    
    # add the task element to the page as new node in the list by cloning from a
    # template
    task_html = task_template.clone(task_id)
    task_html_content = task_html.select("p")
    task_html_content.element.innerText = task["content"]
    task_html_check = task_html.select("input")
    task_list.element.appendChild(task_html.element)

    def check_task(evt=None):
        task["done"] = not task["done"]
        if task["done"]:
            add_class(task_html_content, "line-through")
        else:
            remove_class(task_html_content, "line-through")

    task_html_check.element.onclick = check_task


def add_task_event(e):
    if e.key == "Enter":
        fill_tasks()

def req_differences(rid1, rid2):
    #print("[+] Requested "+rid1+" and "+rid2)
    #get_JSON_Fetch(rid1, rid2)
    #asyncio.ensure_future(get_JSON_Fetch(rid1, rid2))
    diff = get_JSON_Fetch(rid1, rid2)
    return diff

releaseid1.element.onkeypress = add_task_event
