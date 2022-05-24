# -*- coding: utf-8 -*-

doc = __revit__.ActiveUIDocument.Document

class FlexDucts(object):
    def __init__(self, list_flex_ducts):
        self._flex_ducts = {}
        self._sort(list_flex_ducts)
        self._output(self._flex_ducts)

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

    def _sort(self, list_flex_ducts):
        for element in list_flex_ducts:
            diameter = self._take_parameter_value(element, 'Диаметр')
            lentgth = self._take_parameter_value(element, 'Длина')
            lentgth = float(lentgth) / 1000
            comment = self._take_parameter_value(element, 'Комментарии к типоразмеру')
            mark = self._take_parameter_value(element, 'ADSK_Марка')
            maker = self._take_parameter_value(element, 'ADSK_Завод-изготовитель')
            dimention = self._take_parameter_value(element, 'ADSK_Единица измерения')
            name = comment + ' ' + 'ø' + diameter + ' мм.' + '\t' + mark + '\t' \
                   + '' + '\t' + maker + '\t' + dimention + '\t' + '{}'
            if name in self._flex_ducts.keys():
                self._flex_ducts[name] += lentgth
            else:
                self._flex_ducts[name] = lentgth

    def _output(self, dictionary):
        for name in sorted(dictionary):
            print name.format(str(round(dictionary[name] * 1.25 + 0.5)))


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

    list_flex_ducts = []

    for element in selection:
        if element.Category.Name == 'Гибкие воздуховоды':
            list_flex_ducts.append(element)

    flex_ducts = FlexDucts(list_flex_ducts)
