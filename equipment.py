# -*- coding: utf-8 -*-

import clr
clr.AddReference('RevitAPI')

from Autodesk.Revit import DB

doc = __revit__.ActiveUIDocument.Document

class Equipment(object):
    def __init__(self, list_equipment, list_name_parameters, list_closing_parameters):
        self._equipment = {}
        self._sort(list_equipment, list_name_parameters, list_closing_parameters)
        self._output(self._equipment)

    def _take_parameter_value(self, element, name, list_parameters):
        for name_pararmeter in list_parameters:
            try:
                elementId = element.GetTypeId()
                typesize = doc.GetElement(elementId)
                value_pararmeter = typesize.LookupParameter(name_pararmeter).AsString()
                if value_pararmeter == None:
                    value_pararmeter = ''
                name = name + value_pararmeter + '\t'
            except:
                try:
                    value_pararmeter = element.LookupParameter(name_pararmeter).AsString()
                    if value_pararmeter == None:
                        value_pararmeter = ''
                    name = name + value_pararmeter + '\t'
                except:
                    print 'для элемента ', element.Id, ' не удалось получить параметр: ', name_pararmeter
        return name

    def _sort(self, list_equipment, list_name_parameters, list_closing_parameters):
        for element in list_equipment:
            name = self._take_parameter_value(element, '', list_name_parameters)
            name += 'шт.' + '\t' + '{}' + '\t'
            name = self._take_parameter_value(element, name, list_closing_parameters)
            if name in self._equipment.keys():
                self._equipment[name] += 1
            else:
                self._equipment[name] = 1

    def _output(self, dictionary):
        for name in sorted(dictionary):
            print name[:-1].format(str(dictionary[name]))

if __name__ == '__main__':

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

    elements = selection

    for element in elements:
        if element.Category.Name == 'Оборудование':
            list_equipment.append(element)
        elif element.Category.Name == 'Арматура воздуховодов':
            list_duct_accessories.append(element)
        elif element.Category.Name == 'Воздухораспределители':
            list_air_distributors.append(element)

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