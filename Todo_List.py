import datetime, time
from PIL import ImageDraw
from Fonts import Fonts

class Todos_List():
    def __init__(self):
        self.__screen_height = 320
        self.todo_response = dict()
        self.do_screen_update = 0
        self.__point_to_shorten = 55
        self.__fonts= Fonts()
        self.__default_line_location = 20
        self.__max_number_todos_shown = 9
        self.__line_location = self.__default_line_location
        self.__line_start = 48 # Not sure what this TODO: Figure this out

    def __reset_line_location(self):
        self.__line_location = self.__default_line_location

    def get_todos(self) -> bool:
        print('-= Ping ToDo API =-')
        try:
            new_todo_response = requests.get(
                "https://beta.todoist.com/API/v8/tasks", params={"token": TODOIST_TOKEN}).json()
        except ValueError:
            print('-= ToDo API JSON Failed - Will Try Again =-')
            # time.sleep(todo_wait) #TODO: fix this
            return False
        except:
            print('-= ToDo API Too Many Pings - Will Try Again =-')
            #time.sleep(refresh_time) #TODO: Fix this
            return False

        if ((new_todo_response) != (todo_response)):
            print('-= Task List Change Detected =-')
            #do_screen_update = 1 #TODO: Screen update?
            todo_response = new_todo_response
            return True

    def __should_shorten(self, text: str) -> bool:
        return len(text) > self.__point_to_shorten

    def __get_todo_text(self, text: str)-> str:
        if (self.__should_shorten(text)):
            text = text[0:self.__point_to_shorten] + '...'

        return text 

    def ___get_current_date(self) -> int:
        return int(datetime.date.today().strftime('%j')) + (int(time.strftime("%Y")) * 365)

    def __has_due_date(self, todo: dict) -> bool:
        return 'due' in todo

    def __past_due_date(self, todo: dict) :#-> bool,int:
        if not self.__has_due_date(todo):
           return False, -1 

            # TODO: Rename `val1` & `val2`
        val1 = datetime.date(int(str(todo['due']['date']).split('-')[0]), int(str(todo['due']['date']).split('-')[1]), int(
            str(todo['due']['date']).split('-')[2])).strftime('%j')
        val2 = str(todo['due']['date']).split('-')[0]

        due_date = int(val1) + (int(val2) * 365)
        
        return True, due_date

    def __write_task_str(self, image:Image, item: str):
        task_postion = (
            256,
            self.__line_start + self.__line_location
             )
        image.text(task_postion, item,
                        font=self.__fonts.tasks_list, fill=0)  # Print task strings
    
    def __write_priority_circle(self, image:Image, priority: str):
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

    def __write_task_separating_line(self, image:Image):
        line_postion = (
            250,
            self.__line_start + 18 + self.__line_location,
            640, self.__line_start + 18 + self.__line_location
            )
        image.line(line_postion, fill=0)  # Draw the line below the task

    def __write_due_date(self, image:Image, due_date:str):
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

    def __write_number_of_extra_todos(self, image:Image, number_of_extra_todos: int):
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

    def refresh(self, red_image:Image, black_image:Image) -> None:
        self.__reset_line_location()
        for task in self.todo_response:
            item:str = str(task['content'])
            priority:str = str(task['priority'])

            item:str = self.__get_todo_text(item)
            _, due_date = self.__past_due_date(task)
            is_todo_past_due_date:bool = due_date < self.___get_current_date() and due_date > 0

            temp_image : Image = red_image if is_todo_past_due_date else black_image

            self.__write_task_str(temp_image, item)
            self.__write_priority_circle(temp_image, priority)
            self.__write_task_separating_line(temp_image)

            if self.__has_due_date(task):
                _due_date: str = str(task['due']['string'])
                self.__write_due_date(temp_image, _due_date)

            if (is_todo_past_due_date):
                red_image = temp_image
            else:
                black_image = temp_image

            self.__line_location += 26

            number_of_extra_todos: int = len(self.todo_response) - self.__max_number_todos_shown # the number of todos not able shown
            is_greater_screen_height: bool = self.__line_start + self.__line_location + 28 >= self.__screen_height

            if ( is_greater_screen_height and number_of_extra_todos> 0):
                self.__write_number_of_extra_todos(red_image,number_of_extra_todos)
                break
