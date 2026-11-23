from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QRadioButton, QGroupBox, QButtonGroup
from random import shuffle, randint

app = QApplication([])

win = QWidget()
win.setWindowTitle('Memory Card')

btn_ok = QPushButton('Ответить')
lb_question = QLabel('В каком году основано село Молочное?')

RadioGroupBox = QGroupBox('Варианты ответа')
rbtn1 = QRadioButton('1677')
rbtn2 = QRadioButton('1760')
rbtn3 = QRadioButton('1924')
rbtn4 = QRadioButton('9999')

RadioGroup = QButtonGroup()
RadioGroup.addButton(rbtn1)
RadioGroup.addButton(rbtn2)
RadioGroup.addButton(rbtn3)
RadioGroup.addButton(rbtn4)

layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn1)
layout_ans2.addWidget(rbtn2)
layout_ans3.addWidget(rbtn3)
layout_ans3.addWidget(rbtn4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)

RadioGroupBox.setLayout(layout_ans1)

AnsGroupBox = QGroupBox('Результат теста')
lb_result = QLabel('Правильно/Неправильно')
lb_correct = QLabel('9999')

layout_res = QVBoxLayout()
layout_res.addWidget(lb_result, alignment = (Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_correct, alignment = Qt.AlignHCenter, stretch = 2)
AnsGroupBox.setLayout(layout_res)

layout_line1 = QHBoxLayout()
layout_line2 = QHBoxLayout()
layout_line3 = QHBoxLayout()

layout_line1.addWidget(lb_question, alignment = (Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide()
layout_line3.addStretch(1)
layout_line3.addWidget(btn_ok, stretch = 2)
layout_line3.addStretch(1)

layout_card = QVBoxLayout()
layout_card.addLayout(layout_line1, stretch = 2)
layout_card.addLayout(layout_line2, stretch = 8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch = 1)
layout_card.addStretch(1)
layout_card.setSpacing(5)

class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

questions_list = []
questions_list.append(Question('В каком году основано Село Молочное?', "6767", "1864", "9376", "8376"))
questions_list.append(Question('Какая функция отвечает за печать текста?', "print", "input", "break", "write"))
questions_list.append(Question('Квадратный корень из 9 = ?', "3", "81", "169", "18"))
questions_list.append(Question('К какой части речи относится слово сделанный?', "прилагательное", "существительное", "глагол", "наречие"))
questions_list.append(Question('Вам нравятся уроки алгоритмики?', "да", "нет", "совсем нет", "абсолютно нет"))

def show_result():
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_ok.setText('Следующий вопрос')

def show_question():
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_ok.setText('Ответить')

    RadioGroup.setExclusive(False)
    rbtn1.setChecked(False)
    rbtn2.setChecked(False)
    rbtn3.setChecked(False)
    rbtn4.setChecked(False)
    RadioGroup.setExclusive(True)

def start_test():
    if "Ответить" == btn_ok.text():
        show_result()
    else:
        show_question()

answers = [rbtn1, rbtn2, rbtn3, rbtn4]

def ask(q: Question):
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_question.setText(q.question)
    lb_correct.setText(q.right_answer)
    show_question()

def showcor(res):
    lb_correct.setText(res)
    show_result()

def check_answer():
    if answers[0].isChecked():
        showcor('Правильно!')
        win.score += 1
        print('Статистика\n-Всего вопросов: ', win.total, '\n-Правильных ответов: ', win.score)
        print('Рейтинг: ', (win.score/win.total*100), '%')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            showcor('Неверно!')
            print('Рейтинг: ', (win.score/win.total*100), '%')

def next_question():
    win.total += 1
    print('Статистика\n-Всего вопросов: ', win.total, '\n-Правильных ответов: ', win.score)
    cur_question = randint(0, len(questions_list)-1)
    q = questions_list[cur_question]
    ask(q)

def click_OK():
    if btn_ok.text() == 'Ответить':
        check_answer()
    else:
        next_question()

win.setLayout(layout_card)
win.resize(300,200)
win.cur_question = -1
win.score = 0
win.total = 0
btn_ok.clicked.connect(click_OK)
next_question()
win.show()
app.exec()

