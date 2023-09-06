import PySimpleGUI as sg

# ------ Functions ------ #
from components.analyze_answer import AnalyzeAnswer

# ------ Libs ------ #
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def View(lang, model):
    if lang == 'en':
        from lang.components.table_data.graph import en as langText
    else:
        lang = 'es'
        from lang.components.table_data.graph import es as langText

    key = model.table
    fields = model.columns
    fields_labels = langText['fields-labels-'+key]
    fields_dicc = {"":""}
    fields_labels_dicc = {"":""}
    for i in range(len(fields)):
        fields_dicc[fields[i]] = fields_labels[i]
    for i in range(len(fields_labels)):
        fields_labels_dicc[fields_labels[i]] = fields[i]

    type_graph = ['plot', 'bar', 'pie']
    type_graph_labels = langText['graph-types']
    type_graph_dicc = {"":""}
    type_graph_labels_dicc = {"":""}
    for i in range(len(type_graph)):
        type_graph_dicc[type_graph[i]] = type_graph_labels[i]
    for i in range(len(type_graph_labels)):
        type_graph_labels_dicc[type_graph_labels[i]] = type_graph[i]

    # ------ Elements ------ #
    # ------ Design ------ #
    layout = [
        [
        sg.Text(langText['label-select-type']),
        sg.Combo(type_graph_labels, key='type', readonly=True, enable_events=True, default_value=''),
        sg.Text(langText['label-select-data1'], key='text_data1', visible=False),
        sg.Combo(values=[], key='combo_data1', readonly=True, enable_events=True, default_value='', visible=False, size=(10,1)),
        sg.Text(langText['label-select-data2'], key='text_data2', visible=False),
        sg.Combo(values=[], key='combo_data2', readonly=True, default_value='', visible=False, size=(10,1)),
        ],

        [
        sg.Column(layout=[
            [sg.Canvas(key='canvas', size=(600, 400))],
        ]),

        sg.Column(layout=[
            [sg.Table(
                values=[],
                headings=langText['graph-cols-headings'],
                key='table',
                alternating_row_color='gray',
                expand_y=True,
            )],
        ], expand_y=True),

        sg.Column(layout=[
            [sg.Text(langText['describe'], key='text_table_describe', size=(30,None), expand_y=True)],
        ], expand_y=True, element_justification='center'),
        ],

        [sg.Text(expand_x=True), sg.Button(langText['cancel'], key='exit'), sg.Button(langText['graphing'], key='graphing')]
    ]

    window = sg.Window(langText['title-window']+langText[key], layout, finalize=True)



    # ------ Functions ------ #
    canvas = window['canvas'].TKCanvas
    figure = Figure()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)

    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    ax = {}
    for t in type_graph:
        ax[t] = figure.add_subplot()
        ax[t].set_visible(False)

    # ------ EXECUTE Functions ------ #


    # ------ Events ------ #
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'exit'):
            break

        # ------ Define combo data 1 ------ #
        #quito columnas que no puedo graficar respecto al grafico
        if event == 'type':
            elements = ['text_data1','combo_data1','text_data2','combo_data2']
            for e in elements:
                window[e].update(visible=False)
                
            fields = ['id_item','id_user','info','detail']

            type = type_graph_labels_dicc[values['type']]
            if type == 'plot':
                fields = ['date_register']

            fields_labels = []
            for f in fields:
                fields_labels.append(fields_dicc[f])

            window['combo_data1'].update(values=fields_labels)
            window['text_data1'].update(visible=True)
            window['combo_data1'].update(visible=True)

        # ------ Define combo data 2 ------ #
        #quito columnas que no puedo graficar respecto a la columna anterior
        if event == 'combo_data1':
            type = type_graph_labels_dicc[values['type']]
            if not type in ('pie', 'plot'):
                fields = []

                if type == 'bar':
                    data1 = fields_labels_dicc[values['combo_data1']]
                    if data1 in ('id_item','id_user'):
                        fields = ['','info','detail']
                        
                fields_labels = []
                for f in fields:
                    fields_labels.append(fields_dicc[f])

                window['combo_data2'].update(values=fields_labels)
                window['text_data2'].update(visible=True)
                window['combo_data2'].update(visible=True)

        if event == 'graphing':
            if values['type'] == '':
                sg.popup(langText['notify-select-type'])
            elif values['combo_data1'] == '':
                sg.popup(langText['notify-select-data1'])
            else:
                graphing()

        def graphing():
            model_class = model()
            x = []
            y = []
            datax = []
            datay = []

            col1 = fields_labels_dicc[values['combo_data1']]
            col2 = fields_labels_dicc[values['combo_data2']]
            cols = [col1, col2]

            # ------ Get Data ------ #
            select = ", ".join(cols)
            select = select.rstrip(", ")
            answer = model_class.GetData(select, '')
            analyze = AnalyzeAnswer(answer)

            columns = cols.copy()
            if '' in columns:
                columns.remove('')
            df = pd.DataFrame(data=analyze, columns=columns)

            if cols[0] in ('info', 'detail'):
                df[cols[0]] = df[cols[0]].apply(lambda x: "Si" if x in ("", "-") else "No")
            if cols[1] in ('info', 'detail'):
                df[cols[1]] = df[cols[1]].apply(lambda x: "Si" if x in ("", "-") else "No")

            for t in type_graph:
                ax[t].set_visible(False)
                ax[t].clear()
            table_values = []

            type = type_graph_labels_dicc[values['type']]
            axes = ax[type]
            axes.set_visible(True)

            desc_x = fields_dicc[cols[0]]
            desc_y = langText['total-articles']

            if type == 'plot':
                df1 = df[cols[0]].value_counts()
                df2 = df1.reset_index()
                df2.columns = [cols[0], 'counts']
                df2 = df2.sort_values(cols[0])
                x = list(df2[cols[0]])
                y = list(df2['counts'])

                axes.plot(x, y)
                axes.set_xlabel(fields_dicc[cols[0]])
                axes.set_ylabel('Total')

                datax = x
                datay = y

            if type == 'bar':
                if cols[1] == '':
                    df1 = df[cols[0]].value_counts()
                    y = list(df1)
                    x = list(df1.index.astype('string'))

                    axes.bar(x, y)
                    axes.set_xlabel(fields_dicc[cols[0]])
                    axes.set_ylabel(fields_dicc[cols[1]])

                    datax = x
                    datay = y

                else:
                    df1 = df.groupby([cols[0]]).value_counts()
                    df2 = df1.reset_index()
                    df2.columns = [cols[0], cols[1], 'counts']
                    df_0 = df2[df2[cols[1]] == 0]
                    df_1 = df2[df2[cols[1]] == 1]

                    x = list(df_1[cols[0]].astype('string'))
                    y = list(df_1['counts'])

                    x_0 = list(df_0[cols[0]].astype('string'))
                    y_0 = list(df_0['counts'])

                    axes.bar(x, y, width=0.5)
                    axes.bar(x_0, y_0, align='edge', width=0.5)
                    axes.legend(labels=langText['graph-bar-legends'])

                    datax = list(df[cols[0]])
                    datay = list(df[cols[1]])

            if type == 'pie':
                df1 = df[cols[0]].value_counts()
                y = list(df1)
                x = list(df1.index)

                axes.pie(x=y, labels=x)
                axes.set_xlabel(fields_dicc[cols[0]])

                datax = x
                datay = y

                desc_x = 'ID'
                if cols[0] in ('info', 'detail'):
                    desc_x = langText['graph-pie-descx']

            table_values = list(zip(datax,datay))

            window['table'].update(values=table_values)
            window['text_table_describe'].update(
                langText['label-select-data1'] + ": " + desc_x + "\n" +
                langText['label-select-data2'] + ": " + desc_y + " \n\n" +
                langText['analyze'] + ": " + langText['analyze-'+type]
            )

            # ------ Desing Graph ------ #
            figure_canvas_agg.draw()

    window.close()