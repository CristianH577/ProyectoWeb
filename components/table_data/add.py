import PySimpleGUI as sg

# ------ Libs ------ #
from components.analyze_answer import AnalyzeAnswer
import io
import os
from PIL import Image
import shutil


def View(lang, model):
    if lang == 'en':
        from lang.components.table_data.add import en as langText
    else:
        lang = 'es'
        from lang.components.table_data.add import es as langText
        
    key = model.table
    # ------ Elements ------ #
    col1 = []
    col2 = []

    labels_fields = langText['labels-fields-'+key]

    if key == "users":
        fields = ['id_user','email','password','username','server','region','charname','date_register','verify','discord', 'rol']

        values_combos = {
            "server": ['giran', 'ti'],
            "region": ['na','sa','eu','oc'],
            "rol": ['user', 'admin']
        }

        for field in labels_fields:
            col1.append([sg.Text(field)])

        for field in fields:
            if field in ('server','region', 'rol'):
                col2.append([sg.Combo(values=values_combos[field], key=field, readonly=True)])
            else:
                col2.append([sg.Input(key=field)])
    
    if key == "items":
        class_items = {
            'Armor': 'equipment,armor',
            'Weapon': 'equipment,weapon',
            'Accessory': 'equipment,accessory',
            'Equipment - Misc': 'equipment,misc',
            'Enchant Scroll': 'enchant,enchant_scroll',
            'Soul Crystal': 'enchant,soul_crystal',
            'Augment Stone': 'enchant,augment_stone',
            'Dyes': 'enchant,dyes',
            'Spellbook': 'enchant,spellbook',
            'Enchant - Misc': 'enchant,misc',
            'Potion/Scroll': 'misc,potion_scroll',
            'Tickets': 'misc,tickets',
            'Box/Crafting': 'misc,box_crafting',
            'Misc': 'misc,misc'
        }

        combo_values = list(class_items.keys())

        for field in labels_fields:
            col1.append([sg.Text(field)])

        col2.append([sg.Input(key='name_item', size=(30,1))])
        col2.append([sg.Combo(values=combo_values, key='class_item', readonly=True)])
        col2.append([sg.Input(key='input_img', size=(30,1), readonly=True), sg.FileBrowse(key='img', file_types=(("ALL Files", "*.png"),))])

    if key == "articles":
        fields = ['id_item','id_user','price','amount','info','detail']
        for field in labels_fields:
            col1.append([sg.Text(field)])

        for field in fields:
            col2.append([sg.Input(key=field)])


    # ------ Design ------ #
    layout = [
        [sg.Image('', expand_x=True, key='img-preview')],

        [
            sg.Column(layout=col1),
            sg.Column(layout=col2),
        ],

        [sg.Text('', expand_x=True), sg.Button('Cancelar', key='exit'), sg.Button(langText['add'], key='add'), sg.Button(langText['preview'], key='preview', visible=(key=="items"))]
    ]

    window = sg.Window(langText['title-window']+langText[key], layout)


    # ------ FUNCTIONS ------ #
    def validation():
        for k,v in values.items():
            if v == '': 
                sg.popup(langText['notify-complete'])
                return False
        return True
    
    def moveImg(current, new):
        path = ".../ProyectowebPy/assets/icons/"
        new_path = path + new + ".png"
        copy = shutil.copy(current, new_path)

        if not os.path.isdir(current):
            sg.PopupError("Error")
        elif not os.path.isdir(new_path):
            sg.PopupError("Error")
        elif not copy:
            sg.PopupError("Error")
    
    def moveImgToServer(current, new):
        path = ".../ProyectowebAPI/assets/icons/"
        new_path = path + new + ".png"
        copy = shutil.copy(current, new_path)

        if not os.path.isdir(current):
            sg.PopupError("Error")
        elif not os.path.isdir(new_path):
            sg.PopupError("Error")
        elif not copy:
            sg.PopupError("Error")

    # ------ Events ------ #
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'exit'):
            break

        if event == 'add':
            if validation():
                #muevo img a la
                # current = values['input_img']
                # new_name = values['name_item']

                #carpeta del programa
                # moveImg(current, new_name)

                #carpeta del servidor
                # moveImgToServer(current, new_name)
                
                #guardo data
                model_class = model()
                for k,v in values.items():
                    model_class.set(k,v)

                answer = model_class.Add()
                analyze = AnalyzeAnswer(answer)
                if analyze:
                    sg.popup(langText['notify-added'])
                    window.close()
            
        if event == 'preview':
            img_path = values['input_img']
            
            if os.path.exists(img_path):
                image = Image.open(img_path)
                image.thumbnail((32, 32))
                bio = io.BytesIO()
                image.save(bio, format="png")
                window['img-preview'].update(data=bio.getvalue())

    window.close()