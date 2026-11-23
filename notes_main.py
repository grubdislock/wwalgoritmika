#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QTextEdit, QInputDialog
import json

app = QApplication([])

notes = { 'Футбол' : {
    'текст': "Матч России и Бразилии 21 апреля 2027 года в 19:89 по МСК",
    'теги': ['футбол','матч']
} }

with open('notes_data.json', 'w') as file:
    json.dump(notes, file)

notes_win = QWidget()
notes_win.setWindowTitle('Notes')
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

button_note_create = QPushButton('Добавить заметку')
button_note_save = QPushButton('Сохранить заметку')
button_note_rem = QPushButton('Удалить заметку')

list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')
find_tag = QLineEdit()
find_tag.setPlaceholderText('Введите тег..')

button_tag_add = QPushButton('Добавить к заметке')
button_tag_rem = QPushButton('Открепить заметку')
button_tag_search = QPushButton('Искать заметку по тегу')

field_text = QTextEdit()

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_rem)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(find_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_rem)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)


col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'Название заметки:')
    if ok and note_name != '':
        notes[note_name] = {'текст': '', 'теги':[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])
        print(notes)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print('Заметка для сохранения не выбрана!')

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print('Заметка для удаления не выбрана!')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = find_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            with open ('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print('Заметка для добавление тега не выбрана!')

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open ('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print('Тег для удаления не выбран')

def search_tag():
    print(button_tag_search.text())
    tag = find_tag.text()
    if button_tag_search.text() == 'Искать заметки по тегу' and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == 'Сбросить поиск':
        find_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')
        print(button_tag_search.text())
    else:
        pass


list_notes.itemClicked.connect(show_note)

button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_rem.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_rem.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
notes_win.show()

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()