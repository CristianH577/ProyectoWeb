import PySimpleGUI as sg

# ------ Elements ------ #
from components.menu_layout import menu_layout

# ------ Views ------ #
from components.table_data.table_data import View as view_tableData

from components.table_data.add import View as view_add
from components.table_data.edit import View as view_edit
from components.table_data.graph import View as view_graph

from components.messages.answer import View as view_answer

# ------ Models ------ #
from models.user_model import UserClass as model_user
from models.item_model import ItemClass as model_item
from models.article_model import ArticleClass as model_article
from models.todo_model import ToDoClass as model_todo
from models.message_model import MessageClass as model_message

# ------ Functions ------ #
from components.analyze_answer import AnalyzeAnswer
from components.menu_layout import menu_layout_functions

# ------ Libs ------ #
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def View(lang):
    if lang == 'en':
        from lang.main import en as langText
    else:
        lang = 'es'
        from lang.main import es as langText

    # ------ Vars ------ #
    current = {
        "section": "home",
        "model": {}
    }

    # ------ Menu lat ------ #
    sections = ["home", "users", "articles", "items", "", "exit"]
    sectionsTitles = langText['sectionsTitles']

    sections_menu_layout = []
    sections_menu_layout += [
        [sg.Text('', size=(13, 2), pad=(0,0), expand_x=True)],
    ]
    for s,t in zip(sections, sectionsTitles):
        if s == "":
            x = [sg.Text(expand_y=True)]
        else:
            x = [
                sg.Button(button_text=t, key='section-'+s, pad=(0,0), expand_x=True),
                sg.Button("", size=(1,None), key='mark-'+s, disabled=True, pad=(0,0), border_width=0, visible=False)
            ]

        sections_menu_layout += [x]

    # ------ To does ------ #
    todoes_layout = [
        [
            sg.Input(key='new-todo', size=(20,None), expand_x=True),
            sg.Button(langText['add'], key='todoes-add'),
            sg.Button(langText['mark'], key='todoes-mark'),
            sg.Button(langText['delete'], key='todoes-delete'),
            sg.Button("φ", font=(1), key='todoes-refresh')
        ],
        [sg.Table(
            values=[],
            headings=langText['table-heading-todoes'],
            expand_x=True,
            key='table-todoes',
            auto_size_columns=False,
            col_widths=(0,1,30),
            justification='center',
            visible_column_map=[False,True,True],
            alternating_row_color='gray',
        )],
    ]

    # ------ Messages ------ #
    messages_layout = [
        [
            sg.Text(expand_x=True),
            sg.Button(langText['add'], key='messages-add'),
            sg.Button(langText['reply'], key='messages-reply'),
            sg.Button(langText['mark'], key='messages-mark'),
            sg.Button(langText['delete'], key='messages-delete'),
            sg.Button("φ", font=(1), key='messages-refresh')
        ],
        [sg.Table(
            values=[],
            headings=langText['table-heading-messages'],
            expand_x=True,
            expand_y=True,
            key='table-messages',
            auto_size_columns=False,
            col_widths=(0,1,2,16,2),
            justification='center',
            visible_column_map=[False,True,True,True,True],
            alternating_row_color='gray',
        )],
    ]

    # ------ Articles ------ #
    articles_layout = [
        [sg.Text("", font=(15), key='text-articles-total'),sg.Text(expand_x=True), sg.Button("φ", font=(1), key='articles-refresh')]
    ]
    # ------ Adena ------ #
    adena_layout = [
        [sg.Text("", font=(15), key='text-adena-price', expand_x=True)],
        [sg.Text(expand_x=True), sg.Button("φ", font=(1), key='adena-refresh')],
    ]
    # ------ Users ------ #
    users_layout = [
        [sg.Canvas(key='canvas')],
        [sg.Text(expand_x=True), sg.Button("φ", font=(1), key='users-refresh')],
    ]

    # ------ Design ------ #
    layout = [
        [sg.Menu(menu_layout(lang), key='menu')],

        [
        sg.Column(
            layout=sections_menu_layout,
            expand_y=True,
            pad=(0,0),
        ),

        sg.Column(
            layout=[
                [sg.Column(layout=[
                    [sg.Frame(layout=todoes_layout, title=langText['title-todoes'], size=(400,200))],
                    [sg.Frame(layout=messages_layout, title=langText['title-messages'], expand_y=True, expand_x=True)],
                ], expand_y=True),

                sg.Column(layout=[
                    [sg.Frame(layout=articles_layout, title=langText['title-articles'], expand_x=True)],

                    [sg.Frame(layout=adena_layout, title="Adena", expand_x=True)],

                    [sg.Frame(layout=users_layout, title=langText['title-users'])],
                ], expand_y=True)],
            ],
            key="col_content_home", expand_y=True
        ),

        sg.Column(layout=
            view_tableData(lang, "users", langText['table-heading-users'], []),
            key="col_content_users", expand_y=True, visible=False
        ),
        sg.Column(layout=
            view_tableData(lang, "items", langText['table-heading-items'], []),
            key="col_content_items", expand_y=True, visible=False
        ),
        sg.Column(layout=
            view_tableData(lang, "articles", langText['table-heading-articles'], []),
            key="col_content_articles", expand_y=True, visible=False
        ),
        ],

    ]

    window = sg.Window("Main", layout, finalize=True, margins=(0,0))


    # ------ FUNCTIONS ------ #
    # ------ Menu lat ------ #
    def getValues():
        model = current['model']()
        answer = model.GetData('*', '')
        analyze = AnalyzeAnswer(answer)
        if analyze or analyze == []:
            refreshTable(analyze)

    def refreshTable(values):
        table = window['tabledata-'+current['section']]
        table_widget = table.Widget
        table.update(values=values)
        headings = langText['table-heading-'+current['section']]

        #Resize table
        if values != []:
            char_width = int(sg.Text.char_width_in_pixels('t')/2)
            table_widget.pack_forget()
            test = [list(map(str, i)) for i in values]
            all_data = [headings] + test
            col_widths = [(max(map(len, i))+1)*char_width for i in list(zip(*all_data))]
            for col, width in zip(headings, col_widths):
                table_widget.column(col, width=width)
            table_widget.pack(side='left', fill='both', expand=True)

    def mark_button_selected():
        for s in ["home", "users", "articles", "items"]:
            if (s == current['section']):
                bool = True
            else:
                bool = False

            window['mark-'+s].update(visible=bool)

    def updateMainView(currentSection):
        current['section'] = currentSection
        mark_button_selected()

        for section in ("home", "users", "items", "articles"):
            if section != currentSection:
                window['col_content_'+section].update(visible=False)
            else:
                window['col_content_'+section].update(visible=True)

        if currentSection in ("users", "items", "articles"):
            if currentSection == "users":
                current['model'] = model_user
            if currentSection == "items":
                current['model'] = model_item
            if currentSection == "articles":
                current['model'] = model_article

            getValues()

    # ------ To does ------ #
    def getToDoes():
        todo_class = model_todo()
        getdata = todo_class.GetData("*", "")
        analyze = AnalyzeAnswer(getdata)
        if analyze or analyze == []:
            analyze = np.array(analyze)
            for i in range(len(analyze)):
                if analyze[i][1] == '1':
                    analyze[i][1] = "✓"
                else:
                    analyze[i][1] = ""
            analyze = tuple(map(tuple, analyze))
            window['table-todoes'].update(values=analyze)

    # ------ Messages ------ #
    def getMessages():
        msg_class = model_message()
        getdata = msg_class.GetData("id_msg,allowed,id_user,subject,answer", "")
        analyze = AnalyzeAnswer(getdata)
        if analyze or analyze == []:
            analyze = np.array(analyze)
            for i in range(len(analyze)):
                #marco el visto
                if analyze[i][1] == '1':
                    analyze[i][1] = "✓"
                else:
                    analyze[i][1] = ""

                #marco si tiene respuesta
                if analyze[i][4] != '':
                    analyze[i][4] = "✓"
                else:
                    analyze[i][4] = ""
            analyze = tuple(map(tuple, analyze))
            window['table-messages'].update(values=analyze)

    # ------ Articles ------ #
    def getTotalArt():
        article_class = model_article()
        count = article_class.Count("*", "")
        analyze = AnalyzeAnswer(count)
        if analyze or analyze == '0':
            window['text-articles-total'].update(analyze)

    # ------ Adena ------ #
    def getAdenaPrices():
        article_class = model_article()
        count = article_class.GetData("price", "id_item=26")
        analyze = AnalyzeAnswer(count)
        describe = ""
        if analyze or analyze == []:
            df = pd.DataFrame(analyze)
            describe = df.describe()[0]
            describe = str(describe)
            describe = describe.replace("Name: 0, dtype: float64", "")
            describe = describe.rstrip()
            describe = describe.upper()
        window['text-adena-price'].update(describe)

    # ------ Users ------ #
    def draw_user_graph():
        count = []
        user_class = model_user()
        count0 = user_class.Count("*", "active='0'")
        answer0 = AnalyzeAnswer(count0)
        count.append(answer0)
        count1 = user_class.Count("*", "active='1'")
        answer1 = AnalyzeAnswer(count1)
        count.append(answer1)

        total = count[0] + count[1]

        canvas = window['canvas'].TKCanvas
        figure = Figure(
            facecolor=sg.theme_background_color(),
            constrained_layout=True,
            figsize=[2,2]
        )
        axes = figure.add_subplot()

        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

        x1=[0.5]
        x2=[1]
        y1=[count[0]]
        y2=[count[1]]
        w=0.5
        axes.bar(x1, y1, width=w, color=['red'])
        axes.bar(x2, y2, width=w, color=['green'])

        axes.set_xlabel('Total: ' + str(total), color=sg.theme_text_color())
        axes.set_xticklabels([])
        axes.tick_params(bottom = False)

        axes.yaxis.set_ticks([])
        axes.set_title(langText['graph-title'], pad=15, color=sg.theme_text_color())

        axes.spines['right'].set_visible(False)
        axes.spines['top'].set_visible(False)
        axes.spines['bottom'].set_visible(False)
        axes.spines['left'].set_visible(False)

        axes.set_facecolor(sg.theme_background_color())

        #valor sobre las barras
        for bar in axes.patches:
            axes.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height()+0.25 + bar.get_y(),
            round(bar.get_height()), ha = 'center',
            color = 'w', weight = 'bold', size = 10)

        figure_canvas_agg.draw()


    # ------ EXECUTE FUNCTIONS ------ #
    # ------ Menu lat ------ #
    mark_button_selected()
    # ------ To does ------ #
    # ------ Messages ------ #
    # ------ Articles ------ #
    # ------ Adena ------ #


    # ------ Events ------ #
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'exit'):
            break

        # ------ Menu sup ------ #
        if values['menu']:
            def applyChanges(lan):
                # window.close()
                window.Close()
                if lan:
                    View(lan)
                else:
                    View(lang)

            menu_layout_functions(values['menu'], applyChanges, lang)
        else:
            event = event.split('-')
            # ------ Menu lat ------ #
            if event[0] == "section":
                if event[1] in ("home", "users", "items", "articles"):
                    updateMainView(event[1])

                if event[1] == "exit":
                    break


            # ------ HOME ------ #
            # ------ To does ------ #
            if event[0] == "todoes":
                if event[1] == "refresh":
                    getToDoes()

                if event[1] == "add":
                    if values['new-todo'] != "":
                        newTodo = values['new-todo']
                        todo_class = model_todo()
                        todo_class.set('content',newTodo)
                        add = todo_class.Add()
                        analyze = AnalyzeAnswer(add)
                        if analyze:
                            getToDoes()
                            sg.popup_notify(langText['notify-add'], title="Success")

                if event[1] == "delete":
                    if values['table-todoes']:
                        todoes_values = window['table-todoes'].get()
                        todoes_values = np.array(todoes_values)

                        id = []
                        for i in range(len(values['table-todoes'])):
                            id.append(todoes_values[values['table-todoes'][i]][0])

                        todo_class = model_todo()
                        todo_class.set('id_todo',id)
                        delete = todo_class.Delete()
                        answer = AnalyzeAnswer(delete)
                        if answer:
                            getToDoes()
                            sg.popup_notify(langText['notify-delete'], title="Success")

                if event[1] == "mark":
                    if values['table-todoes']:
                        todoes_values = window['table-todoes'].get()
                        todoes_values = np.array(todoes_values)

                        id_mark = []
                        id_unmark = []
                        for i in range(len(values['table-todoes'])):
                            doit = todoes_values[values['table-todoes'][i]][1]
                            if doit == "✓":
                                id_unmark.append(todoes_values[values['table-todoes'][i]][0])
                            else:
                                id_mark.append(todoes_values[values['table-todoes'][i]][0])

                        todo_class = model_todo()
                        if id_mark != []:
                            todo_class.set('id_todo',id_mark)
                            todo_class.set('doit','1')
                            update = todo_class.Update()
                            analyze = AnalyzeAnswer(update)
                            
                        if id_unmark != []:
                            todo_class.set('id_todo',id_unmark)
                            todo_class.set('doit','0')
                            update = todo_class.Update()
                            analyze = AnalyzeAnswer(update)

                        getToDoes()

            # ------ Messages ------ #
            if event[0] == "messages":
                if event[1] == "refresh":
                    getMessages()

                if event[1] == "add":
                    msg_class = model_message()
                    msg_class.set('id_user',0)
                    for f in ('email','subject','content'):
                        msg_class.set(f,'test')

                    add = msg_class.Add()
                    answer = AnalyzeAnswer(add)
                    if answer:
                        getMessages()
                        sg.popup_notify(langText['notify-add'], title="Success")

                if event[1] == "delete":
                    if values['table-messages']:
                        msgs_values = window['table-messages'].get()
                        msgs_values = np.array(msgs_values)

                        id = []
                        for i in range(len(values['table-messages'])):
                            id.append(msgs_values[values['table-messages'][i]][0])

                        msg_class = model_message()
                        msg_class.set('id_msg',id)
                        delete = msg_class.Delete()
                        answer = AnalyzeAnswer(delete)
                        if answer:
                            getMessages()
                            sg.popup_notify(langText['notify-delete'], title="Success")

                if event[1] == "mark":
                    if values['table-messages']:
                        msgs_values = window['table-messages'].get()
                        msgs_values = np.array(msgs_values)

                        id_mark = []
                        id_unmark = []
                        for i in range(len(values['table-messages'])):
                            doit = msgs_values[values['table-messages'][i]][1]
                            if doit == "✓":
                                id_unmark.append(msgs_values[values['table-messages'][i]][0])
                            else:
                                id_mark.append(msgs_values[values['table-messages'][i]][0])

                        msg_class = model_message()
                        if id_mark != []:
                            msg_class.set('id_msg',id_mark)
                            msg_class.set('allowed','1')
                            update = msg_class.Update()
                            analyze = AnalyzeAnswer(update)
                            
                        if id_unmark != []:
                            msg_class.set('id_msg',id_unmark)
                            msg_class.set('allowed','0')
                            update = msg_class.Update()
                            analyze = AnalyzeAnswer(update)

                        getMessages()

                if event[1] == "reply":
                    if values['table-messages']:
                        msgs_values = window['table-messages'].get()
                        row = values['table-messages'][0]
                        id = msgs_values[row][0]
                        view_answer(id)
           

            # ------ Articles ------ #
            if event[0] == "articles":
                if event[1] == "refresh":
                    getTotalArt()

            # ------ Adena ------ #
            if event[0] == "adena":
                if event[1] == "refresh":
                    getAdenaPrices()

            # ------ Users ------ #
            if event[0] == "users":
                if event[1] == "refresh":
                    draw_user_graph()


            # ------ SECTIONS ------ #
            if event[0] == "tabledata":
                if event[1] == "refresh":
                    getValues()

                if event[1] == "search":
                    input = values['input-search-'+current['section']]
                    combo = values['combo-search-'+current['section']]

                    if input != '':
                        if combo == '':
                            k = " LIKE '%" + str(input) + "%' OR "
                            where = str(k.join(current['model'].columns))
                        else:
                            where = str(combo)

                        where = where + " LIKE '%" + str(input) + "%'"

                        model = current['model']()
                        answer = model.GetData('*', where)
                        analyze = AnalyzeAnswer(answer)
                        if analyze or analyze == []:
                            refreshTable(analyze)
                    else:
                        getValues()

                if event[1] == "add":
                    view_add(lang, current['model'])

                if event[1] == "graph":
                    view_graph(lang, current['model'])

            if event[0] == langText['delete']:
                table = 'tabledata-'+current['section']
                if values[table]:
                    data = window[table].Get()

                    rows = values[table]
                    id = []
                    for i in rows:
                        id.append(data[i][0])
                    pop = sg.popup_yes_no(langText['notify-delete-ask']+": #"+str(id)+"?", title=langText['notify-delete-ask'])

                    if pop == 'Yes':
                        model = current['model']()
                        if current['section'] == "users":
                            set = "user"
                        elif current['section'] == "articles":
                            set = "art"
                        elif current['section'] == "items":
                            set = "item"
                        model.set("id_"+set, id)

                        answer = model.Delete()
                        analyze = AnalyzeAnswer(answer)
                        if analyze:
                            getValues()
                            sg.popup(langText['notify-delete'])

            if event[0] == langText['edit']:
                table = 'tabledata-'+current['section']
                if (values[table] and len(values[table]) == 1):
                    data = window[table].Get()
                    row = values[table][0]
                    model = current['model']()

                    headings = model.columns
                    for i in range(len(headings)):
                        model.set(headings[i], data[row][i])
                    view_edit(lang,current['model'])

    window.close()

View('')