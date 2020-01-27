import datetime
import time
from PIL import ImageDraw
from Fonts import Fonts

from tasks.google_tasks import get_tasks


class Todos_List():
    def __init__(self):
        self.__screen_height = 320
        self.todo_response = dict()
        self.do_screen_update = 0
        self.__text_max_length = 55
        self.__fonts = Fonts()
        self.__default_line_location = 20
        self.__max_number_todos_shown = 9
        self.__line_location = self.__default_line_location
        self.__line_start = 48  # Not sure what this TODO: Figure this out

    def __reset_line_location(self):
        self.__line_location = self.__default_line_location

    def get_todos(self) -> bool:
        print('-= Ping ToDo API =-')
        todo_response = get_tasks()
        if ((new_todo_response) != (todo_response)):
            print('-= Task List Change Detected =-')
            #do_screen_update = 1 #TODO: Screen update?
            todo_response = new_todo_response
            return True

    def __should_shorten(self, text: str) -> bool:
        return len(text) > self.__text_max_length

    def __get_todo_text(self, task: dict) -> str:
        text = task['title']
        if (self.__should_shorten(text)):
            text = text[0:self.__text_max_length] + '...'

        return text

    def ___get_current_date(self) -> int:
        return int(datetime.date.today().strftime('%j')) + (int(time.strftime("%Y")) * 365)

    def __has_due_date(self, todo: dict) -> bool:
        return 'due' in todo

    def __is_todo_past_due_date(self, todo: dict) -> bool:
        if not self.__has_due_date(todo):
            return False

        return todo['due'] < self.___get_current_date() and due_date > 0

    def __write_task_str(self, image: ImageDraw, item: str):
        task_postion = (
            256,
            self.__line_start + self.__line_location
             )
        image.text(task_postion, item, font=self.__fonts.tasks_list, fill=0)  # Print task strings

    def __write_priority_circle(self, image: ImageDraw, priority: str):
        cirle_background_postion = (
            247.5,
            self.__line_start + 2 + self.__line_location,
            257.5,
            self.__line_start + 12 + self.__line_location
            )
        circle_forground_postion = (
            250,
            self.__line_start + 2 + self.__line_location
        )
        image.chord(cirle_background_postion, 0, 360, fill=0)  # Draw circle for task priority
        image.text(circle_forground_postion, priority,
                        font=self.__fonts.tasks_priority, fill=255)  # Print task priority string

    def __write_task_separating_line(self, image:ImageDraw):
        line_postion = (
            250,
            self.__line_start + 18 + self.__line_location,
            640, self.__line_start + 18 + self.__line_location
            )
        image.line(line_postion, fill=0)  # Draw the line below the task

    def __write_due_date(self, image:ImageDraw, due_date:str):
        rectangle_background_postion = (
            525,
            self.__line_start + 2 + self.__line_location,
            640,
            self.__line_start + 18 + self.__line_location
            )
        rectangle_forground_postion = (
            530.5,
            self.__line_start + 3.5 + self.__line_location
            )
        image.rectangle(rectangle_background_postion, fill=0)
        image.text(rectangle_forground_postion, due_date, font=self.__fonts.tasks_due_date, fill=255)  # Print the due date of task

    def __write_number_of_extra_todos(self, image:ImageDraw, number_of_extra_todos: int):
        extra_todos_background_position = (
            550,
            self.__line_start + 2 + self.__line_location,
            640,
            self.__line_start + 18 + self.__line_location
            )

        notshown_tasks: str = "... & {} more ...".format(number_of_extra_todos)
        w_notshown_tasks, h_notshown_tasks = self.__fonts.tasks_due_date.getsize(notshown_tasks)
        x_nowshown_tasks = 550 + \
            ((640 - 550) / 2) - (w_notshown_tasks / 2) # TODO:???, figure out what this is

        extra_todos_forground_position = (
            x_nowshown_tasks,
            self.__line_start + 3.5 + self.__line_location
            )

        # Print larger rectangle for more tasks
        image.rectangle(extra_todos_background_position, fill=0)
        # The placement for extra tasks not shown
        image.text(extra_todos_forground_position, notshown_tasks,
                        font=self.__fonts.tasks_due_date, fill=255)  # Print identifier that there are tasks not shown

    def refresh(self, red_image:ImageDraw, black_image:ImageDraw) -> None:
        self.__reset_line_location()
        for task in self.todo_response:
            # priority:str = str(task['priority'])

            title:str = self.__get_todo_text(task)
            _is_todo_past_due_date:bool = self._is_todo_past_due_date(task)

            temp_image : ImageDraw = red_image if _is_todo_past_due_date else black_image

            self.__write_task_str(temp_image, title)
            # self.__write_priority_circle(temp_image, priority)
            self.__write_task_separating_line(temp_image)

            if self.__has_due_date(task):
                _due_date: str = str(task['due'])
                self.__write_due_date(temp_image, _due_date)

            if (_is_todo_past_due_date):
                red_image = temp_image
            else:
                black_image = temp_image

            self.__line_location += 26

            number_of_extra_todos: int = len(self.todo_response) - self.__max_number_todos_shown # the number of todos not able shown
            is_greater_screen_height: bool = self.__line_start + self.__line_location + 28 >= self.__screen_height

            if (is_greater_screen_height and number_of_extra_todos> 0):
                self.__write_number_of_extra_todos(red_image,number_of_extra_todos)
                break
