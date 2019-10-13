from ..models import tasks

def createTask(task):
    tasks.objects.create(name=task.name, about=task.about, date=task.date, priority=task.priority, user=task.user)

def listTask(user):
    return tasks.objects.filter(user=user).all()

def listTaskID(id):
    return tasks.objects.get(id=id)

def updateTask(taskDB, newTask):
    taskDB.name = newTask.name
    taskDB.about = newTask.about
    taskDB.date = newTask.date
    taskDB.priority = newTask.priority
    taskDB.save(force_update=True)

def removeTask(taskDB):
    taskDB.delete()