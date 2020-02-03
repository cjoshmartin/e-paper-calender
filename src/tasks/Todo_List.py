import datetime
import time
import logging
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
        self.__text_max_length = 55
        self.__max_number_todos_shown = 9

        logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Todo List  : Setup correctly")

        get_todos_thread = threading.Thread(target=self.get_todos, daemon=True)
        get_todos_thread.start()

    def get_todos(self) -> None:
        mins_to_sleep = 3
        seconds_to_sleep = mins_to_sleep * 60

        while True:
            if self.__display.has_internet:
                print('-= Ping ToDo API =-')
                new_todo_response = get_tasks()
                if ((new_todo_response) != (self.todo_response)):
                    logging.info('Todo List     : Task List Change Detected ')
                    self.todo_response = new_todo_response
                    self.__display.should_update_display  = True

            logging.info('Todo List  :`get_todo` thread is going to sleep for {}s💤'.format(seconds_to_sleep))
            time.sleep(seconds_to_sleep)

    def __should_shorten(self, text) -> bool:
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

    def __write_task_str(self, image, item) -> None:
        task_postion = (
            256,
            self.__display.starting_vertical_position_of_tasks + self.__display.line_location
             )
        image.text(task_postion, item, font=self.__fonts.tasks_list, fill=0)  # Print task strings

    def __write_priority_circle(self, image, priority) -> None:
        cirle_background_postion = (
            247.5,
            self.__display.starting_vertical_position_of_tasks + 2 + self.__display.line_location,
            257.5,
            self.__display.starting_vertical_position_of_tasks + 12 + self.__display.line_location
            )
        circle_forground_postion = (
            250,
            self.__display.starting_vertical_position_of_tasks + 2 + self.__display.line_location
        )
        image.chord(cirle_background_postion, 0, 360, fill=0)  # Draw circle for task priority
        image.text(circle_forground_postion, priority,
                        font=self.__fonts.tasks_priority, fill=255)  # Print task priority string

    def __write_task_separating_line(self, image) -> None:
        line_postion = (
            250,
            self.__display.starting_vertical_position_of_tasks + 18 + self.__display.line_location,
            self.__display.width,
            self.__display.starting_vertical_position_of_tasks + 18 + self.__display.line_location
            )
        image.line(line_postion, fill=0)  # Draw the line below the task

    def __write_due_date(self, image:ImageDraw, due_date) -> None:
        start_of_due_date_box = 580
        rectangle_background_postion = (
            start_of_due_date_box,
            self.__display.starting_vertical_position_of_tasks + 2 + self.__display.line_location,
            self.__display.width,
            self.__display.starting_vertical_position_of_tasks + 18 + self.__display.line_location
            )
        rectangle_forground_postion = (
            rectangle_background_postion[0] + 5.5,
            self.__display.starting_vertical_position_of_tasks + 3.5 + self.__display.line_location
            )
        image.rectangle(rectangle_background_postion, fill=0)
        image.text(rectangle_forground_postion, due_date, font=self.__fonts.tasks_due_date, fill=255)  # Print the due date of task

    def refresh(self) -> None:
        logging.info("Todo List  :  Refreshing Todo section of display")
        self.__display.reset_line_location()
        self.__display.header_title('Tasks')

        for task in self.todo_response:
            # priority:str = str(task['priority'])

            title = self.__get_todo_text(task)
            _is_todo_past_due_date = self.__is_todo_past_due_date(task)

            temp_image  = self.__display.draw_red if _is_todo_past_due_date else self.__display.draw_black

            self.__write_task_str(temp_image, title)
            # self.__write_priority_circle(temp_image, priority)
            self.__write_task_separating_line(temp_image)

            if self.__has_due_date(task):
                meta_data = task["due-meta"]
                month = meta_data["month"]
                day = meta_data["day"]
                year = meta_data["year"]

                # NOTE: Due date format is here
                _due_date = datetime.date(year, month, day).strftime('%b %e')
                if 'time' in meta_data:
                    _due_date = "{}, {}".format(meta_data['time'], _due_date)

                self.__write_due_date(temp_image, _due_date)

            if _is_todo_past_due_date:
                self.__display.draw_red = temp_image
            else:
                self.__display.draw_black = temp_image

            self.__display.increment_line_location()

            number_of_extra_todos = len(self.todo_response) - self.__max_number_todos_shown # the number of todos not able shown
            is_greater_screen_height = self.__display.starting_vertical_position_of_tasks + self.__display.line_location + 28 >= self.__screen_height

            if is_greater_screen_height and number_of_extra_todos > 0:
                self.__display.context_bar_title("... & {} more ...".format(number_of_extra_todos))
                break
