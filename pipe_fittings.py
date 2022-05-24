# -*- coding: utf-8 -*-

doc = __revit__.ActiveUIDocument.Document

class PipeFittings(object):
    def __init__(self, list_pipe_fittings):
        self._pipe_fittings = {}
        self._sort_fittings(list_pipe_fittings)
        self._output(self._pipe_fittings)

    def _take_parameter_value(self, element, name_parameter):
        try:
            value_parameter = element.LookupParameter(name_parameter).AsString()
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

    def _sort_fittings(self, list_pipe_fittings):
        for element in list_pipe_fittings:
            size = self._take_parameter_value(element, 'Размер')
            comment = self._take_parameter_value(element, 'Комментарии к типоразмеру')
            if comment == 'Отвод стальной':
                mark = 'ГОСТ 17375-2001'
            elif comment == 'Переход стальной':
                mark = 'ГОСТ 17378-2001'
            elif comment == 'Тройник стальной':
                mark = 'ГОСТ 17376-2001'
            elif comment == 'Заглушка стальная':
                mark = 'ГОСТ 17379-2001'
            else:
                mark = ''
            name = comment + ' Ø' + size + ' мм' + '\t' + mark + '\t' + '' + '\t' + '' \
                + '\t' + 'шт.' + '\t' + '{}'
            if name in self._pipe_fittings.keys():
                self._pipe_fittings[name] += 1
            else:
                self._pipe_fittings[name] = 1

    def _output(self, dictionary):
        for name in sorted(dictionary):
            print name.format(dictionary[name])

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

    list_pipe_fittings = []

    for element in selection:
        if element.Category.Name == 'Соединительные детали трубопроводов':
            list_pipe_fittings.append(element)

    pipe_fittings = PipeFittings(list_pipe_fittings)