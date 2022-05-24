# -*- coding: utf-8 -*-

doc = __revit__.ActiveUIDocument.Document

class Pipes(object):
    def __init__(self, list_pipes, unaccountable_length = 0.1, additional_coefficient = 1.2):
        self._pipes = {}
        self._name_formation(list_pipes, unaccountable_length)
        self._output(self._pipes, additional_coefficient)

    def _take_parameter_value(self, element, name_parameter):
        try:
            value_parameter = element.LookupParameter(name_parameter).AsValueString()
        except:
            try:
                elementId = element.GetTypeId()
                typesize = doc.GetElement(elementId)
                value_parameter = typesize.LookupParameter(name_parameter).AsString()
            except:
                print 'для элемента ', element.Id, ' не удалось получить параметр: ', name_parameter
                value_parameter = None
        if value_parameter == None:
            value_parameter = ''
        return value_parameter

    def _name_formation(self, list_pipes, unaccountable_length):
        for element in list_pipes:
            comment = self._take_parameter_value(element, 'Комментарии к типоразмеру')
            diameter = self._take_parameter_value(element, 'Диаметр')
            lentgth = self._take_parameter_value(element, 'Длина')
            lentgth = float(lentgth) / 1000
            if lentgth < unaccountable_length:
                continue
            outer_diameter = self._take_parameter_value(element, 'Внешний диаметр')
            inner_diameter = self._take_parameter_value(element, 'Внутренний диаметр')
            mark = self._take_parameter_value(element, 'ADSK_Марка')
            dimention = self._take_parameter_value(element, 'ADSK_Единица измерения')
            thickness = round((float(outer_diameter) - float(inner_diameter)) / 2, 1)
            if 'водогаз' in comment:
                name = comment + ' Ду' + diameter + 'x' + str(thickness) + ' мм' \
                    + '\t' + mark + '\t' + '' + '\t' + '' + '\t' + dimention + '\t' + '{}'
            elif 'электросвар' in comment:
                name = comment + ' Дн' + outer_diameter + 'x' + str(thickness) + ' мм' \
                    + '\t' + mark + '\t' + '' + '\t' + '' + '\t' + dimention + '\t' + '{}'
            else:
                name = comment + ' Ø' + diameter + ' мм' \
                    + '\t' + mark + '\t' + '' + '\t' + '' + '\t' + dimention + '\t' + '{}'
            if name in self._pipes.keys():
                self._pipes[name] += lentgth
            else:
                self._pipes[name] = lentgth

    def _output(self, dictionary, additional_coefficient):
        for name in sorted(dictionary):
            print name.format(str(round(dictionary[name] * additional_coefficient + 0.5)))



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

    list_pipes = []

    for element in selection:
        if element.Category.Name == 'Трубы':
            list_pipes.append(element)

    pipes = Pipes(list_pipes, unaccountable_length = 0.1, additional_coefficient = 1.2)