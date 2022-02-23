import clr
clr.AddReference('RevitAPI')

from Autodesk.Revit.DB import Category, Parameter
from duct import Duct

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

selection = get_selected_elements(doc)

def bprint(array='', depth=0):
    '''Функция beautiful print
    Вывод в консоль массива данных построчно.
    Так же поддерживается рекурсивный вывод словарей

    Пример:
    d = {
        1: 10,
        2: [
            [200, 201],
            [210, 211],
            [220, 221]
        ],
        3: {
            30: {
                300: [301, 302, 303],
                310: [311, 312, 313]
            },
            31: [310, 320, 330]
        }
    }
    '''
    start_symbol = '\t' * depth
    if isinstance(array, dict):
        for key, value in array.items():
            bprint(key, depth)
            bprint(value, depth + 1)
    elif hasattr(array, '__iter__') and not isinstance(array, str):
        for element in array:
            bprint(element, depth)
    else:
        print '{}{}'.format(start_symbol, array)

list_elements_duct = []

for element in selection:
    if element.Category.Name == 'Воздуховоды':
        list_elements_duct.append(element)

ducts = Duct(list_elements_duct)
ducts.form_dict_ducts()
ducts.output()




