#!/usr/bin/python3
"""
    Ray's Bible Game
    Raymond Hernandez
    November 20, 2020

"""
from tkinter import *
from tkinter import ttk
import pandas as pd
import random


class BibleGame(Frame):

    def __init__(self, root=None):
        Frame.__init__(self, root)

        self.root = root
        self.description = "Please enter your name"
        self.label_credit = "2020 Raymond Hernandez raymondhernandez@outlook.com"
        self.bg_color = "#5b3c88"
        self.button_color = "#af3c88"
        self.fg_color = "#ffffff"
        self.font = "Tahoma"
        self.active_button_color = "#bf3c88"
        self.game_size = "300x600"
        self.window_title = "The Bible Trivia Game"
        self.game_over_message = "Game Over"
        self.restart_message = "Re-enter a new name. Press to play again"

        self.question_index = []

        self.MASTER_TIMER = 120
        self.timer = self.MASTER_TIMER

        self.high_score = 0
        self.score = 0
        self.save_timer = 0
        self.top_five_players = [""] * 5

        """ Loads questions from data bank """
        self.questions = pd.read_excel(r'data.xlsx')
        self.questions.values  # Questions as arrays
        self.total_question_bank = len(self.questions) - 1  # First column is not counted
        self.number_of_questions = 5
        self.display_question = [0] * self.number_of_questions
        self.key = [0] * self.number_of_questions
        self.a = [0] * self.number_of_questions
        self.b = [0] * self.number_of_questions
        self.c = [0] * self.number_of_questions
        self.d = [0] * self.number_of_questions
        self.last_question = False

        """ String Variables """
        self.final = StringVar()
        self.right_wrong = StringVar()
        self.dynamic_h_score = StringVar()
        self.dynamic_y_score = StringVar()
        self.dynamic_a = StringVar()
        self.dynamic_b = StringVar()
        self.dynamic_c = StringVar()
        self.dynamic_d = StringVar()
        self.dynamic_score = StringVar()
        self.dynamic_question = StringVar()
        self.dynamic_questions_left = StringVar()
        self.dynamic_timer = StringVar()
        self.top_1_var = StringVar()
        self.top_2_var = StringVar()
        self.top_3_var = StringVar()
        self.top_4_var = StringVar()
        self.top_5_var = StringVar()

        """ Entry box """
        self.name_entry = Entry(root, text="Raymond",
                                bg=self.fg_color,
                                fg=self.bg_color,
                                font=(self.font, 12),
                                justify=CENTER)

        """ Photos """
        self.logo = PhotoImage(file='parch.png')
        self.logo_label = Label(root, image=self.logo,
                                borderwidth=0, highlightthickness=0)
        self.logo_label.image = self.logo

        self.logo2 = PhotoImage(file='bible_logo.png')
        self.logo2_label = Label(root, image=self.logo2,
                                 borderwidth=0, highlightthickness=0)
        self.logo2_label.image = self.logo2

        """ Labels """
        self.main_label = Label(root, text=self.description,
                                bg=self.bg_color,
                                fg=self.fg_color,
                                font=(self.font, 12),
                                wraplength=280,
                                justify=CENTER)

        self.title_label = Label(root, text="The Bible Trivia Game",
                                 bg=self.bg_color,
                                 fg=self.fg_color,
                                 font=(self.font, 16, "bold"),
                                 wraplength=280,
                                 justify=CENTER)

        self.credit_label = Label(root, text=self.label_credit,
                                  bg=self.bg_color,
                                  fg=self.fg_color,
                                  font=(self.font, 8),
                                  justify=CENTER)

        self.h_score_label = Label(root, text="TOP 5 SCORES",
                                   bg=self.bg_color,
                                   fg=self.fg_color,
                                   font=(self.font, 12, "bold"),
                                   justify=CENTER)

        self.top_1 = Label(root, textvariable=self.top_1_var,
                           bg=self.bg_color,
                           fg=self.fg_color,
                           font=(self.font, 12),
                           justify=CENTER)

        self.top_2 = Label(root, textvariable=self.top_2_var,
                           bg=self.bg_color,
                           fg=self.fg_color,
                           font=(self.font, 12),
                           justify=CENTER)

        self.top_3 = Label(root, textvariable=self.top_3_var,
                           bg=self.bg_color,
                           fg=self.fg_color,
                           font=(self.font, 12),
                           justify=CENTER)

        self.top_4 = Label(root, textvariable=self.top_4_var,
                           bg=self.bg_color,
                           fg=self.fg_color,
                           font=(self.font, 12),
                           justify=CENTER)

        self.top_5 = Label(root, textvariable=self.top_5_var,
                           bg=self.bg_color,
                           fg=self.fg_color,
                           font=(self.font, 12),
                           justify=CENTER)

        self.h_score = Label(root, textvariable=self.dynamic_h_score,
                             bg=self.bg_color,
                             fg=self.fg_color,
                             font=(self.font, 12),
                             justify=CENTER)

        self.y_score_label = Label(root, text="YOUR SCORE",
                                   bg=self.bg_color,
                                   fg=self.fg_color,
                                   font=(self.font, 12, "bold"),
                                   justify=CENTER)

        self.y_score = Label(root, textvariable=self.dynamic_y_score,
                             bg=self.bg_color,
                             fg=self.fg_color,
                             font=(self.font, 12),
                             justify=CENTER)

        self.correct = Label(self.root, textvariable=self.right_wrong,
                             bg=self.bg_color,
                             fg=self.fg_color,
                             font=(self.font, 10),
                             wraplength=280,
                             justify=CENTER)

        self.scoreboard = Label(self.root, textvariable=self.dynamic_score,
                                bg=self.bg_color,
                                fg=self.bg_color,
                                font=(self.font, 12),
                                wraplength=280,
                                justify=CENTER)

        self.time_left = Label(self.root, textvariable=self.dynamic_timer,
                               bg=self.bg_color,
                               fg=self.fg_color,
                               font=(self.font, 12),
                               wraplength=280,
                               justify=CENTER)
        self.question = Label(self.root, textvariable=self.dynamic_question,
                              bg=self.bg_color,
                              fg=self.fg_color,
                              font=(self.font, 12),
                              wraplength=280,
                              justify=CENTER)

        self.question_left = Label(self.root, textvariable=self.dynamic_questions_left,
                                   bg=self.bg_color,
                                   fg=self.fg_color,
                                   font=(self.font, 12),
                                   wraplength=280,
                                   justify=CENTER)

        """ Buttons """
        self.start_button = Button(root, text="Start Game",
                                   height=2,
                                   width=10,
                                   bg=self.button_color,
                                   fg=self.fg_color,
                                   activebackground=self.active_button_color,
                                   font=(self.font, 16))

        self.dynamic_final = Button(self.root, textvariable=self.final,
                                    height=4,
                                    width=30,
                                    wraplength=280,
                                    bg=self.button_color,
                                    fg=self.fg_color,
                                    activebackground=self.active_button_color,
                                    font=(self.font, 12))

        self.choice_a = Button(self.root, textvariable=self.dynamic_a,
                               height=2,
                               width=30,
                               bg=self.button_color,
                               fg=self.fg_color,
                               activebackground=self.active_button_color,
                               font=(self.font, 12))

        self.choice_b = Button(self.root, textvariable=self.dynamic_b,
                               height=2,
                               width=30,
                               bg=self.button_color,
                               fg=self.fg_color,
                               activebackground=self.active_button_color,
                               font=(self.font, 12))

        self.choice_c = Button(self.root, textvariable=self.dynamic_c,
                               height=2,
                               width=30,
                               bg=self.button_color,
                               fg=self.fg_color,
                               activebackground=self.active_button_color,
                               font=(self.font, 12))

        self.choice_d = Button(self.root, textvariable=self.dynamic_d,
                               height=2,
                               width=30,
                               bg=self.button_color,
                               fg=self.fg_color,
                               activebackground=self.active_button_color,
                               font=(self.font, 12))

        self.front_page()

    def front_page(self):
        """ Packs the front page """
        self.root.geometry(self.game_size)
        self.root.configure(background=self.bg_color)
        self.winfo_toplevel().title(self.window_title)
        self.logo_label.pack(padx=10, pady=10)
        self.title_label.pack()
        self.main_label.pack(side=TOP, padx=2, pady=2)
        self.name_entry.pack()
        self.credit_label.pack(side=BOTTOM)
        self.start_button.pack(side=TOP, padx=50, pady=50)
        self.start_button.config(command=self.start_game)
        self.logo2_label.pack(side=BOTTOM, padx=10, pady=1)

    def pack_choices(self):
        """ Packs the question page """
        self.dynamic_questions_left.set("Question " + str(self.current_question + 1) + " of 5")
        self.question_left.pack(side=TOP, padx=2, pady=10)

        self.dynamic_question.set(self.display_question[self.current_question])
        self.question.pack(side=TOP, padx=2, pady=10)

        self.time_left.pack(side=BOTTOM, padx=2, pady=2)

        self.dynamic_score.set("Score: " + str(self.score))
        self.scoreboard.pack(side=BOTTOM, padx=2, pady=2)

        """ Choices a, b, c, & d """
        self.dynamic_d.set(self.d[self.current_question])
        self.choice_d.pack(side=BOTTOM, padx=2, pady=0)
        self.choice_d.config(command=self.picked_d)

        self.dynamic_c.set(self.c[self.current_question])
        self.choice_c.pack(side=BOTTOM, padx=2, pady=0)
        self.choice_c.config(command=self.picked_c)

        self.dynamic_b.set(self.b[self.current_question])
        self.choice_b.pack(side=BOTTOM, padx=2, pady=0)
        self.choice_b.config(command=self.picked_b)

        self.dynamic_a.set(self.a[self.current_question])
        self.choice_a.pack(side=BOTTOM, padx=2, pady=0)
        self.choice_a.config(command=self.picked_a)

        """ Displays if correct or not """
        self.correct.pack(side=BOTTOM, padx=2, pady=2)

        """ Game over message with the restart button """
        self.final.set(self.restart_message)

    def start_game(self):
        """ Load questions """
        self.player_name = self.name_entry.get()
        self.current_question = 0
        self.shuffle_questions()
        self.load_questions()

        """ Clears the start screen """
        self.start_button.pack_forget()
        self.logo_label.pack_forget()
        self.logo2_label.pack_forget()
        self.title_label.pack_forget()
        self.main_label.pack_forget()
        self.name_entry.pack_forget()

        """ Loads timer, question, and choices """
        self.right_wrong.set("")
        self.last_question = False
        self.countdown()
        self.pack_choices()

    def shuffle_questions(self):
        """ Removes duplicates """
        while len(set(self.question_index)) < self.number_of_questions:
            self.question_index.append(random.randint(0, self.total_question_bank))
            self.question_index = list(set(self.question_index))

    def load_questions(self):
        """ Rearrange the random questions to iterable (1 to max questions)"""
        for i, index in enumerate(self.question_index):
            self.display_question[i] = self.questions.iloc[index, 0]
            self.key[i] = self.questions.iloc[index, 1]
            self.a[i] = self.questions.iloc[index, 2]
            self.b[i] = self.questions.iloc[index, 3]
            self.c[i] = self.questions.iloc[index, 4]
            self.d[i] = self.questions.iloc[index, 5]

    def picked_a(self):
        """ Button event when A is pressed """
        self.evaluate_answer(self.a[self.current_question])

    def picked_b(self):
        """ Button event when B is pressed """
        self.evaluate_answer(self.b[self.current_question])

    def picked_c(self):
        """ Button event when C is pressed """
        self.evaluate_answer(self.c[self.current_question])

    def picked_d(self):
        """ Button event when D is pressed """
        self.evaluate_answer(self.d[self.current_question])

    def evaluate_answer(self, answer):
        """ Scoring system """
        if answer == self.key[self.current_question]:
            self.score += 10000
            self.correct_flag = True
        else:
            self.score -= 2000
            self.correct_flag = False

        """ Flags ig previous question is correct/wrong """
        if self.correct_flag:
            self.right_wrong.set("The answer is correct")
        else:
            self.right_wrong.set("The answer is wrong")

        """ Loads the next question """
        self.current_question += 1
        self.next_question()

    def next_question(self):
        """ Makes sure game doesn't go out of bounds """
        if self.current_question < self.number_of_questions:
            self.dynamic_questions_left.set("Question " + str(self.current_question + 1) + " of 5")
            self.dynamic_question.set(self.display_question[self.current_question])
            # self.dynamic_score.set("Score: " + str(self.score))

            self.dynamic_d.set(self.d[self.current_question])
            self.dynamic_c.set(self.c[self.current_question])
            self.dynamic_b.set(self.b[self.current_question])
            self.dynamic_a.set(self.a[self.current_question])
        else:
            self.save_timer = self.timer

            self.display_results()

    def display_results(self):
        """
            Final score is changed in static to avoid bug that calculates
            score while clock still running
        """
        self.last_question = True
        self.timer = 0
        self.static_score = self.score

        self.static_score = int(self.static_score * (self.save_timer / self.MASTER_TIMER))
        if self.static_score < 0:
            self.static_score = 0

        self.dynamic_y_score.set(self.static_score)

        # if self.static_score > self.high_score:
        #     self.high_score = self.static_score

        self.dynamic_h_score.set(self.high_score)

        self.question.pack_forget()
        self.question_left.pack_forget()
        self.choice_a.pack_forget()
        self.choice_b.pack_forget()
        self.choice_c.pack_forget()
        self.choice_d.pack_forget()

        self.dynamic_final.pack(side=BOTTOM, padx=2, pady=2)
        self.name_entry.pack(side=BOTTOM)
        self.correct.pack(side=BOTTOM, padx=2, pady=2)

        self.logo_label.pack(padx=10, pady=10)
        self.title_label.pack()

        self.y_score_label.pack(side=TOP)
        self.y_score.pack(side=TOP)
        self.h_score_label.pack(side=TOP)
        self.top_1.pack(side=TOP)
        self.top_2.pack(side=TOP)
        self.top_3.pack(side=TOP)
        self.top_4.pack(side=TOP)
        self.top_5.pack(side=TOP)

        self.load_top_scores()
        self.dynamic_final.config(command=self.restart_game)

    def restart_game(self):
        """ Restarts timer and score"""
        self.timer = self.MASTER_TIMER
        self.score = 0

        """ Deletes scoreboard, timer, right/wrong, and restart button """
        self.scoreboard.pack_forget()
        self.time_left.pack_forget()
        self.correct.pack_forget()
        self.dynamic_final.pack_forget()
        self.h_score_label.pack_forget()
        self.h_score.pack_forget()
        self.y_score_label.pack_forget()
        self.y_score.pack_forget()
        self.top_1.pack_forget()
        self.top_2.pack_forget()
        self.top_3.pack_forget()
        self.top_4.pack_forget()
        self.top_5.pack_forget()

        """ Deletes used questions """
        self.question_index = []

        self.start_game()

    def countdown(self):
        if self.timer > 0 and not self.last_question:
            self.timer -= 1
            self.dynamic_timer.set("Time Left: " + str(self.timer) + " seconds")
            self.root.after(1000, lambda: self.countdown())
        elif self.timer == 0 and not self.last_question:
            self.dynamic_timer.set(self.game_over_message)
            self.display_results()

    def load_top_scores(self):
        """ Saves all scores and displays TOP 5 """
        previous_top_scores = pd.read_excel(r'top_scores.xlsx')
        previous_top_scores.values  # Previous scores as arrays

        temp_new_score = self.static_score
        if self.player_name == "":
            self.player_name = "<none>"
        temp_current_player = self.player_name

        excel_limit = 10    # To avoid overloading Excel file
        temp_names = [""] * excel_limit
        temp_scores = [0] * excel_limit

        """ Loads scores into temp list """
        for i in range(excel_limit):
            temp_names[i] = previous_top_scores.iloc[i, 0]
            temp_scores[i] = previous_top_scores.iloc[i, 1]

        """ Sorts if current score is worth saving for Top 5 """
        for i in range(len(previous_top_scores)):
            if temp_new_score > temp_scores[i]:
                temp_names.insert(i, temp_current_player)
                temp_scores.insert(i, temp_new_score)
                break

        for i in range(5):
            self.top_five_players[i] = temp_names[i] + " " + str(temp_scores[i])

        self.top_1_var.set("(1) " + self.top_five_players[0])
        self.top_2_var.set("(2) " + self.top_five_players[1])
        self.top_3_var.set("(3) " + self.top_five_players[2])
        self.top_4_var.set("(4) " + self.top_five_players[3])
        self.top_5_var.set("(5) " + self.top_five_players[4])

        updated_top_scores = pd.DataFrame({'NAME': temp_names,
                                           'SCORE': temp_scores})
        updated_top_scores.to_excel('top_scores.xlsx', index=False)


def main():
    root = Tk()
    app = BibleGame(root)
    root.mainloop()
    # test_area()


def test_area():
    pass


if __name__ == "__main__":
    main()
