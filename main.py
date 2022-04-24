import sys
sys.path.append(r'd:\Dropbox\programming\Python')
import clr
clr.AddReference('RevitAPI')

from ducts import Ducts
from duct_fittings import DuctFittings
from equipment import Equipment
from flex_ducts import FlexDucts
from insulation_ducts import InsulationDucts

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

list_equipment = []
list_duct_accessories = []
list_air_distributors = []
list_ducts = []
list_duct_fittings = []
list_flex_ducts = []

for element in selection:
    if element.Category.Name == 'Оборудование':
        list_equipment.append(element)
    elif element.Category.Name == 'Арматура воздуховодов':
        list_duct_accessories.append(element)
    elif element.Category.Name == 'Воздухораспределители':
        list_air_distributors.append(element)
    elif element.Category.Name == 'Воздуховоды':
        list_ducts.append(element)
    elif element.Category.Name == 'Соединительные детали воздуховодов':
        list_duct_fittings.append(element)
    elif element.Category.Name == 'Гибкие воздуховоды':
        list_flex_ducts.append(element)

list_name_parameters = ['ADSK_Наименование', 
                        'ADSK_Марка',
                        'ADSK_Код изделия',
                        'ADSK_Завод-изготовитель'
                        ]

list_closing_parameters = ['ADSK_Масса_Текст',
                           'ADSK_Примечание'
                           ]

equipment = Equipment(list_equipment, list_name_parameters, list_closing_parameters)
duct_accessories = Equipment(list_duct_accessories, list_name_parameters, list_closing_parameters)
air_distributors = Equipment(list_air_distributors, list_name_parameters, list_closing_parameters)
ducts = Ducts(list_ducts)
duct_fittings = DuctFittings(list_duct_fittings, list_ducts)
flex_ducts = FlexDucts(list_flex_ducts)
insulation_ducts = InsulationDucts(list_ducts, 1.35)