import PySimpleGUI as sg

# ------ Libs ------ #
from components.analyze_answer import AnalyzeAnswer
import io
import os
from PIL import Image
import shutil


def View(lang, model):
    if lang == 'en':
        from lang.components.table_data.edit import en as langText
    else:
        lang = 'es'
        from lang.components.table_data.edit import es as langText
        
    key = model.table
    # ------ Elements ------ #
    col1 = []
    col2 = []

    labels_fields = langText['labels-fields-'+key]
    img_path = ''

    if key == "users":
        fields = ['id_user','email','password','username','server','region','charname','date_register','verify','active','discord', 'rol']

        values_combos = {
            "server": ['giran', 'ti'],
            "region": ['na','sa','eu','oc'],
            "active": ['0', '1'],
            "rol": ['user', 'admin']
        }

        for field in labels_fields:
            col1.append([sg.Text(field)])
        
        for field in fields:
            if field in ('id_user','verify','date_register'):
                col2.append([sg.Text(model.model[field])])
            elif field in ('email','password','username','charname','discord'):
                col2.append([sg.Input(default_text=model.model[field], key=field)])
            elif field in ('server','region','active', 'rol'):
                col2.append([sg.Combo(values=values_combos[field], key=field, readonly=True,default_value=model.model[field])])

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
        
        col2.append([sg.Text(model.model['id_item']),sg.Input(key='id_item', default_text=model.model['id_item'], visible=False)])
        col2.append([sg.Input(default_text=model.model['name_item'], key='name_item')])
        col2.append([sg.Combo(values=combo_values, key='class_item', readonly=True, default_value=model.model['class_item'])])
        col2.append([sg.Input(key='input_img', size=(30,1), default_text=model.model['img']), sg.FileBrowse(key='img', file_types=(("ALL Files", "*.png"),))])

        img = model.model['img']
        if img:
            img_path = "assets/icons/"+ model.model['img'] +".png"

    if key == "articles":
        fields = ['id_art','id_item','id_user','price','amount','info','detail', 'date_register']

        combo_values ={
            "id_item": [],
            "id_user": [],
        }

        for field in labels_fields:
            col1.append([sg.Text(field)])

        for field in fields:
            if field in ('id_art', 'date_register'):
                col2.append([sg.Text(model.model[field])])
            elif field in ('price','amount','info','detail'):
                col2.append([sg.Input(default_text=model.model[field], key=field)])
            elif field in ('id_item','id_user'):
                col2.append([sg.Combo(values=combo_values[field], key=field, readonly=True,default_value=model.model[field])])

    # ------ Design ------ #
    layout = [
        [sg.Image(img_path, expand_x=True, key='img-preview')],

        [
        sg.Column(layout=col1),
        sg.Column(layout=col2),
        ],

        [sg.Text('', expand_x=True), sg.Button(langText['cancel'], key='exit'), sg.Button(langText['save'], key='save'), sg.Button(langText['preview'], key='preview', visible=(key=="items"))]
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

        if event == 'save':
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

                answer = model_class.Update()
                analyze = AnalyzeAnswer(answer)
                if analyze:
                    sg.popup(langText['notify-save'])
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