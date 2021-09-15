import pyttsx3
import time
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from PyQt5.uic import loadUi
import threading
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore
from PyQt5.QtGui import QColor


class Fitness(QMainWindow):
    def __init__(self):
        super(Fitness, self).__init__()
        loadUi("fitness.ui", self)

        self.InitUi()

    def InitUi(self):
        self.start_btn.setStyleSheet("background-color:blue;")
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[0].id)
        self.executor = ThreadPoolExecutor(max_workers=8)

        self.seconds_duration.setRange(0, 59)
        self.break_seconds_duration.setRange(0, 59)

        self.seconds_duration.setValue(50)
        self.break_seconds_duration.setValue(20)
        self.number_of_drills.setValue(13)

        self.start_btn.clicked.connect(self.starting_thread)

        self.all_workouts = [
            "High Knee Jumps",
            "Mountain climbers",
            "Burpees",
            "Left high side Plank raises",
            "Right high side Plank Raises",
            "Russian twist in v-up position",
            "Jumping Lunges",
            "Jumping Jacks",
            "In and outs",
            "Side to side jump squats",
            "Star jump",
            "Fast feet",
            "London Bridge",
        ]

        self.all_gifs = [
            "all_gifs/high knee.gif",
            "all_gifs/mountain_climbers.gif",
            "all_gifs/burpees.gif",
            "all_gifs/left high side plank raises.gif",
            "all_gifs/right_high_side_plank_raises.gif",
            "all_gifs/russian twist.gif",
            "all_gifs/jumping_lunges.gif",
            "all_gifs/jumping_jacks.gif",
            "all_gifs/in_and_outs.gif",
            "all_gifs/side to side jump squats.gif",
            "all_gifs/star jump.gif",
            "all_gifs/fast feet.gif",
            "all_gifs/london_bridge.gif",
        ]

        for i, j in enumerate(self.all_workouts):
            self.all_drills.insertItem(i, j)

    def set_gif(self):
        self.now_drill = QMovie(self.all_gifs[0])
        self.current_drill_image.setMovie(self.now_drill)
        self.now_drill.start()

    def tell(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def starting_thread(self):
        self.executor.submit(self.start_timer)

    def start_timer(self):
        if self.minutes_duration.value() == 0 and self.seconds_duration.value() == 0:
            self.info.setText("Invalid time limit selected")
        elif (
            self.break_seconds_duration.value() == 0
            and self.break_minutes_duration.value() == 0
        ):
            self.info.setText("Invalid break time limit selected")
        elif self.number_of_drills.value() == 0:
            self.info.setText("Invalid number of drills selected")
        else:

            self.info.setText("")
            self.start_btn.setEnabled(False)
            self.tell("Get ready to start")

            break_minutes = self.break_minutes_duration.value()
            break_seconds = self.break_seconds_duration.value()

            total_break = (break_minutes * 60) + break_seconds

            minutes = self.minutes_duration.value()
            seconds = self.seconds_duration.value()
            total = (minutes * 60) + seconds

            number_of_drills = self.number_of_drills.value()

            for i in range(number_of_drills):
                self.current_drill.setText(self.all_workouts[i])

                self.now_drill = QMovie(self.all_gifs[i])
                self.current_drill_image.setMovie(self.now_drill)
                self.now_drill.start()

                if i == number_of_drills - 1:
                    self.next_drill.setText("")

                else:
                    self.next_drill_name = QMovie(self.all_gifs[i + 1])
                    self.next_drill_image.setMovie(self.next_drill_name)
                    self.next_drill_name.start()

                    self.next_drill.setText(self.all_workouts[i + 1])

                try:
                    self.engine.endLoop()
                except:
                    pass
                if i != 0:
                    self.item = self.all_drills.findItems(
                        self.all_workouts[i - 1], QtCore.Qt.MatchRegExp
                    )[0]
                    self.item.setSelected(True)
                    self.all_drills.scrollToItem(self.item)
                    self.item.setBackground(QColor("green"))

                    self.item = self.all_drills.findItems(
                        self.all_workouts[i], QtCore.Qt.MatchRegExp
                    )[0]
                    self.item.setSelected(True)
                    self.all_drills.scrollToItem(self.item)
                    self.item.setBackground(QColor("red"))
                else:
                    self.item = self.all_drills.findItems(
                        self.all_workouts[0], QtCore.Qt.MatchRegExp
                    )[0]
                    self.item.setSelected(True)
                    self.all_drills.scrollToItem(self.item)
                    self.item.setBackground(QColor("red"))

                self.executor.submit(self.tell, f"Begin exercise number {i+1}")
                self.info.setText(f"Exercise number {i+1}")

                i = total

                while i >= 0:
                    self.lcdNumber.display(i)
                    time.sleep(1)
                    if i == (int(total / 2)) + 2:
                        try:
                            self.engine.endLoop()
                        except:
                            pass
                        self.executor.submit(self.tell, "Half way through")
                    i -= 1

                self.executor.submit(self.tell, f"Stop! {total_break} seconds rest")
                self.lcdNumber.display(20)
                self.info.setText("Break")

                j = total_break
                while j > 0:
                    self.lcdNumber.display(j)
                    time.sleep(1)
                    j -= 1
            self.lcdNumber.display(0)
            self.item = self.all_drills.findItems(
                self.all_workouts[-1], QtCore.Qt.MatchRegExp
            )[0]
            self.item.setSelected(True)
            self.all_drills.scrollToItem(self.item)
            self.item.setBackground(QColor("green"))

            self.tell("Congratulations you have successfully completed your workout")


app = QApplication(sys.argv)
window = Fitness()
window.show()

app.exec_()
