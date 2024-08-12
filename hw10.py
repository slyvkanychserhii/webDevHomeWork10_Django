from myapp.models import *
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Проект "Менеджер задач" — ORM запросы
# Цель:
# Освоение основных операций CRUD (Create, Read, Update, Delete) на примере заданных моделей.
# Выполните запросы:
# Создание записей:
# Task:
new_task = Task.objects.create(
    title='Prepare presentation',
    description='Prepare materials and slides for the presentation',
    status='New',
    deadline=timezone.now() + timedelta(days=3),
)

# SubTasks для "Prepare presentation":
new_subtasks = SubTask.objects.bulk_create([
    SubTask(
        title='Gather information',
        description='Find necessary information for the presentation',
        status='New',
        deadline=timezone.now() + timedelta(days=2),
        task = new_task,
    ),
    SubTask(
        title='Create slides',
        description='Create presentation slides',
        status='New',
        deadline = timezone.now() + timedelta(days=1),
        task = new_task,
    )
])

# Чтение записей:
# Tasks со статусом "New":
# Вывести все задачи, у которых статус "New".
Task.objects.filter(status='New')

# SubTasks с просроченным статусом "Done":
# Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
SubTask.objects.filter(Q(status='Done') & Q(deadline__lt=timezone.now()))

# Изменение записей:
# Измените статус "Prepare presentation" на "In progress".
Task.objects.filter(title='Prepare presentation').update(status='In progress')

# Измените срок выполнения для "Gather information" на два дня назад.
updated_subtask = SubTask.objects.filter(title='Gather information').update(deadline=F('deadline') - timedelta(days=2))

# или так:
# try:
#     updated_subtask = SubTask.objects.get(title='Gather information')
#     updated_subtask.deadline = updated_subtask.deadline - timedelta(days=2)
#     updated_subtask.save()
# except ObjectDoesNotExist:
#     print('ObjectDoesNotExist')
# except MultipleObjectsReturned:
#     print('MultipleObjectsReturned')

# Измените описание для "Create slides" на "Create and format presentation slides".
SubTask.objects.filter(title='Gather information').update(description='Create and format presentation slides')

# Удаление записей:
# Удалите задачу "Prepare presentation" и все ее подзадачи.
Task.objects.filter(title='Prepare presentation').delete()

# Оформите ответ: 
# Прикрепите все выполненные запросы (код) и скриншоты с консоли к ответу на домашнее задание.
