import sys
sys.path.append(r'd:\Dropbox\programming\Python')
import clr
clr.AddReference('RevitAPI')

from ducts import Ducts
from fittings import Fittings

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

list_fittings = []
list_ducts = []

elements = selection

for element in elements:
    if element.Category.Name == 'Соединительные детали воздуховодов':
        list_fittings.append(element)
    elif element.Category.Name == 'Воздуховоды':
        list_ducts.append(element)

ducts = Ducts(list_ducts)
fittings = Fittings(list_fittings, list_ducts)