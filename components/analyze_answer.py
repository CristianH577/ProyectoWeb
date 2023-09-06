import PySimpleGUI as sg

def AnalyzeAnswer(answer):
    # print('AnalyzeAnswer')
    bool = answer['bool']

    if bool:
        return answer['value']
    else:
        sg.popup_error(
            "Class: " + answer['class'] + "\n" +
            "Function: " + answer['function'] + "\n" + 
            "Detail: " + answer['detail'] + "\n"
            "Value: " + answer['value'] + "\n",
            title="ERROR"
        )
    
    return False