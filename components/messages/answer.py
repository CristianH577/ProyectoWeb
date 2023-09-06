import PySimpleGUI as sg

from components.analyze_answer import AnalyzeAnswer
from models.message_model import MessageClass as model

def View(id):
    labels_fields = model.columns

    # # ------ Elements ------ #
    col1 = []
    col2 = []

    for field in labels_fields:
        col1.append([sg.Text(field + ": ")])

    for field in labels_fields:
        col2.append([sg.Text(key=field)])
    # ------ Design ------ #
    layout = [
        [sg.Text('Responder', justification='center', font=("Helvetica", 25), expand_x=True)],

        [
        sg.Column(layout=col1),
        sg.Column(layout=col2),
        ],

        [sg.Multiline(key='new-answer', visible=False, size=(20,5), expand_x=True)],

        [sg.Text('', expand_x=True), sg.Button('Cancelar', key='exit'), sg.Button('Marcar', key='mark'), sg.Button('Responder', key='reply')]
    ]

    window = sg.Window('title', layout, finalize=True)


    # ------ FUNCTIONS ------ #
    def getData():
        msg_class = model()
        answer = msg_class.GetData("*", "id_msg='"+str(id)+"'")
        analyze = AnalyzeAnswer(answer)
        if analyze:
            data = analyze[0]
            for field in labels_fields:
                i = labels_fields.index(field)
                value = data[i]
                if field == 'allowed':
                    if value == 1:
                        value = "✓"
                    else:
                        value = ""
                elif field == 'answer':
                    if value == '':
                        window['answer'].update(visible=False)
                        window['new-answer'].update(visible=True)
                    else:
                        window['reply'].update(visible=False)

                window[field].update(value=value)

    # ------ EXECUTE FUNCTIONS ------ #
    getData()


    # ------ Events ------ #
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'exit'):
            break

        if event == "mark":
            mark = window['allowed'].get()
            if mark == "✓":
                bool = 0
            else:
                bool = 1
            msg_class = model()
            msg_class.set('id_msg',[id])
            msg_class.set('allowed',bool)
            update = msg_class.Update()
            analyze = AnalyzeAnswer(update)
            if analyze:
                sg.popup_notify("Realizado", title="Success")
                if bool == 1:
                    mark = "✓"
                else:
                    mark = ""
                window['allowed'].update(value=mark)

        if event == "reply":
            msg_class = model()
            msg_class.set('id_msg',[id])
            msg_class.set('allowed',1)
            msg_class.set('answer',values['new-answer'])
            update = msg_class.Update()
            analyze = AnalyzeAnswer(update)
            if analyze:
                window.close()
                sg.popup_notify("Realizado", title="Success")

    window.close()
