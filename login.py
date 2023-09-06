import PySimpleGUI as sg

# ------ Views ------ #
from main import View as view_main

# ------ Elements ------ #
from components.menu_layout import menu_layout

# ------ Libs ------ #
from components.analyze_answer import AnalyzeAnswer

# ------ Models ------ #
from models.user_model import UserClass as model_user

def View(lang):
    if lang == 'en':
        from lang.login import en as langText
    else:
        lang = 'es'
        from lang.login import es as langText

    # ------ Design ------ #
    layout = [
        [sg.Menu(menu_layout(lang), key='menu')],

        [sg.Text(langText['welcome'], justification='center', font=("Helvetica", 25), expand_x=True)],


        [sg.Text(langText['user'], justification='center', expand_x=True)],
        [sg.InputText(key="input_user", size=(35, None), justification='center')],

        [sg.Text(langText['password'], justification='center', expand_x=True)],
        [sg.InputText(key="input_pass", size=(35, None), justification='center')],

        # [sg.Checkbox(langText['keep-sesion'], key='keep')],

        [sg.Text(key="text_error", text_color='yellow', expand_x=True, justification='center', visible=False, pad=(5,0))],

        [sg.Text('', expand_x=True), sg.Button(langText['exit'], key='exit'), sg.Button(langText['login'], key='login')]
    ]

    window = sg.Window(langText['window-title'], layout, margins=(20, 10))


    # ------ FUNCTIONS ------ #
    def validate_user(username, password):
        if username == '':
            window["text_error"].update(langText['notify-user-none'], visible=True)
        elif password == '':
            window["text_error"].update(langText['notify-pass-none'], visible=True)
        else:
            user_class = model_user()
            select = 'id_user'
            where = "username='" + username + "'"
            answer = user_class.GetData(select, where)
            analyze = AnalyzeAnswer(answer)

            if analyze:
                select = 'rol'
                where = "username='" + username + "' AND password='" + password + "'"
                answer = user_class.GetData(select, where)
                analyze = AnalyzeAnswer(answer)
                if analyze:
                    if analyze[0][0] == "admin":
                        return True
                    else:
                        sg.popup(langText['notify-rol-wrong'])
                else:
                    window["text_error"].update(langText['notify-pass-wrong'], visible=True)
            else:
                window["text_error"].update(langText['notify-user-wrong'], visible=True)

        return False


    # ------ Events ------ #
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'exit'):
            break

        if event == "login":
            user = values['input_user']
            password = values['input_pass']

            if validate_user(user, password):
                window.close()
                view_main(lang)

    window.close()