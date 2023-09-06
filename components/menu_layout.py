import PySimpleGUI as sg

from lang.components.menu_layout import langText as text

def menu_layout(lang):
    langText = text[lang]

    return [
        ['&'+langText['options'], [
            langText['theme'], sg.theme_list(),
            langText['language'], ['es', 'en']
        ]],
        ['&'+langText['help'], ['&'+langText['contact'], '&'+langText['about']+'...']]
    ]

def menu_layout_functions(value, applyChanges, lang):
    langText = text[lang]

    if value in sg.theme_list():
        theme = value
        sg.theme(theme)
        applyChanges('')

    if value in ('es','en'):
        applyChanges(value)

    if ("...") in value:
        sg.popup(langText['about_message'], title="Acerca de")

    if ("Contac") in value:
        sg.popup("kotar.corp@company.com.ar", title="Contacto")