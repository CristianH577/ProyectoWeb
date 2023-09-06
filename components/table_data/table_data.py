import PySimpleGUI as sg

def View(lang, key, headings, values):
    if lang == 'en':
        from lang.components.table_data.table_data import en as langText
    else:
        lang = 'es'
        from lang.components.table_data.table_data import es as langText

    # ------ Elements ------ #
    btn_graph = []
    if key == "articles":
        btn_graph = [sg.Button(langText['graph'], key="tabledata-graph")]
    
    if key == "items":
        right_click_menu = ['&Right', [langText['delete'], langText['edit']]]
    else:
        right_click_menu = ['&Right', [langText['delete']]]
    # ------ Design ------ #
    layout = [
        [
        sg.Button("φ", font=(1), key='tabledata-refresh-'+key),
        sg.Text("", expand_x=True),
        sg.Input(key='input-search-'+key, size=(30,1)),
        sg.Combo(values=[''] + headings, key='combo-search-'+key, readonly=True),
        sg.Button("🔍", key='tabledata-search-'+key, font=(1)),
        ],

        [sg.Table(
            values=values,
            headings=headings,
            key='tabledata-'+key,
            right_click_menu=right_click_menu,
            right_click_selects=True,
            alternating_row_color='gray',
            pad=(0,0),
            num_rows=20,
            expand_x=True,
        )],

        [
        sg.Button(langText['add'], key='tabledata-add-'+key),
        sg.Text("", expand_x=True),
        ] + btn_graph,

    ]

    return layout