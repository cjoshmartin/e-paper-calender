import datetime
import time
import threading

from PIL import ImageDraw
from Display import Display

from tasks.google_tasks import get_tasks


class Todos_List():
    def __init__(self, display: Display):

        self.__display = display
        self.__screen_height = display.height
        self.__fonts = display.fonts

        self.todo_response = dict()
        self.do_screen_update = 0
        self.__text_max_length = 55
        self.__max_number_todos_shown = 9
        self.__starting_vertical_position_of_tasks = 48

        self.__default_line_location = 20
        self.__line_location = self.__default_line_location

        get_todos_thread = threading.Thread(target=self.get_todos, args=(1,), daemon=True)
        get_todos_thread.start()

    def __reset_line_location(self) -> None:
        self.__line_location = self.__default_line_location

    def get_todos(self, arg1) -> None:
        mins_to_sleep = 3
        seconds_to_sleep = mins_to_sleep * 60
        while True:
            print('-= Ping ToDo API =-')
            new_todo_response = get_tasks()
            if ((new_todo_response) != (self.todo_response)):
                print('-= Task List Change Detected =-')
                #do_screen_update = 1 #TODO: Screen update?
                self.todo_response = new_todo_response

            print('`get_todo` thread is going to sleep for {}s💤'.format(seconds_to_sleep))
            time.sleep(30)

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

        return todo['due'] < self.___get_current_date() and  todo['due'] > 0

    def __write_task_str(self, image: ImageDraw, item: str) -> None:
        task_postion = (
            256,
            self.__starting_vertical_position_of_tasks + self.__line_location
             )
        image.text(task_postion, item, font=self.__fonts.tasks_list, fill=0)  # Print task strings

    def __write_priority_circle(self, image: ImageDraw, priority: str) -> None:
        cirle_background_postion = (
            247.5,
            self.__starting_vertical_position_of_tasks + 2 + self.__line_location,
            257.5,
            self.__starting_vertical_position_of_tasks + 12 + self.__line_location
            )
        circle_forground_postion = (
            250,
            self.__starting_vertical_position_of_tasks + 2 + self.__line_location
        )
        image.chord(cirle_background_postion, 0, 360, fill=0)  # Draw circle for task priority
        image.text(circle_forground_postion, priority,
                        font=self.__fonts.tasks_priority, fill=255)  # Print task priority string

    def __write_task_separating_line(self, image: ImageDraw) -> None:
        line_postion = (
            250,
            self.__starting_vertical_position_of_tasks + 18 + self.__line_location,
            self.__display.width,
            self.__starting_vertical_position_of_tasks + 18 + self.__line_location
            )
        image.line(line_postion, fill=0)  # Draw the line below the task

    def __write_due_date(self, image:ImageDraw, due_date: str) -> None:
        start_of_due_date_box = 580
        rectangle_background_postion = (
            start_of_due_date_box,
            self.__starting_vertical_position_of_tasks + 2 + self.__line_location,
            self.__display.width,
            self.__starting_vertical_position_of_tasks + 18 + self.__line_location
            )
        rectangle_forground_postion = (
            rectangle_background_postion[0] + 5.5,
            self.__starting_vertical_position_of_tasks + 3.5 + self.__line_location
            )
        image.rectangle(rectangle_background_postion, fill=0)
        image.text(rectangle_forground_postion, due_date, font=self.__fonts.tasks_due_date, fill=255)  # Print the due date of task

    def __write_number_of_extra_todos(self, image:ImageDraw, number_of_extra_todos: int) -> None:
        unknown_constent = 550 # TODO: Find out what this is
        extra_todos_background_position = (
            unknown_constent,
            self.__starting_vertical_position_of_tasks + 2 + self.__line_location,
            self.__display.width,
            self.__starting_vertical_position_of_tasks + 18 + self.__line_location
            )

        notshown_tasks: str = "... & {} more ...".format(number_of_extra_todos)
        w_notshown_tasks, h_notshown_tasks = self.__fonts.tasks_due_date.getsize(notshown_tasks)
        x_nowshown_tasks = unknown_constent + \
            ((self.__display.width - unknown_constent) / 2) - (w_notshown_tasks / 2) # TODO:???, figure out what this is

        extra_todos_forground_position = (
            x_nowshown_tasks,
            self.__starting_vertical_position_of_tasks + 3.5 + self.__line_location
            )

        # Print larger rectangle for more tasks
        image.rectangle(extra_todos_background_position, fill=0)
        # The placement for extra tasks not shown
        image.text(extra_todos_forground_position, notshown_tasks,
                        font=self.__fonts.tasks_due_date, fill=255)  # Print identifier that there are tasks not shown

    def refresh(self) -> None:
        self.__reset_line_location()
        self.__display.header_title('Tasks')

        for task in self.todo_response:
            # priority:str = str(task['priority'])

            title:str = self.__get_todo_text(task)
            _is_todo_past_due_date:bool = self.__is_todo_past_due_date(task)

            temp_image : ImageDraw = self.__display.draw_red if _is_todo_past_due_date else self.__display.draw_black

            self.__write_task_str(temp_image, title)
            # self.__write_priority_circle(temp_image, priority)
            self.__write_task_separating_line(temp_image)

            if self.__has_due_date(task):
                meta_data = task["due-meta"]
                month = meta_data["month"]
                day = meta_data["day"]
                year = meta_data["year"]

                # NOTE: Due date format is here
                _due_date: str = datetime.date(year, month, day).strftime('%b %e')
                self.__write_due_date(temp_image, _due_date)

            if (_is_todo_past_due_date):
                self.__display.draw_red = temp_image
            else:
                self.__display.draw_black = temp_image

            self.__line_location += 26

            number_of_extra_todos: int = len(self.todo_response) - self.__max_number_todos_shown # the number of todos not able shown
            is_greater_screen_height: bool = self.__starting_vertical_position_of_tasks + self.__line_location + 28 >= self.__screen_height

            if (is_greater_screen_height and number_of_extra_todos> 0):
                self.__write_number_of_extra_todos(self.__display.draw_red, number_of_extra_todos)
                break
