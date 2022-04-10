# -*- coding: utf-8 -*-

doc = __revit__.ActiveUIDocument.Document

class DuctFittings(object):
    def __init__(self, list_duct_fittings, list_ducts):
        self._duct_fittings = {}
        self._sort_fittings(list_duct_fittings)
        self._nipples(list_ducts, 3)
        self._output(self._duct_fittings)

    def _sort_fittings(self, list_duct_fittings):
        for element in list_duct_fittings:
            elementId = element.GetTypeId()
            typesize = doc.GetElement(elementId)
            comment = typesize.LookupParameter('Комментарии к типоразмеру').AsString()
            if comment == 'Ниппель круглого воздуховода':
                continue
            elif comment == None:
                comment = ''
            size = element.LookupParameter('Размер').AsString()
            name = comment + ' ' + size + ' мм.'
            if name in self._duct_fittings.keys():
                self._duct_fittings[name] += 1
            else:
                self._duct_fittings[name] = 1

    def _nipples(self, list_ducts, multiple):
        for element in list_ducts:
            try:
                diameter = element.LookupParameter('Диаметр').AsValueString()
                length = float(element.LookupParameter('Длина').AsValueString()) / 1000
                name = 'Ниппель круглого воздуховода ø' + diameter + ' мм.'
                if int(length / multiple):
                    if name in self._duct_fittings.keys():
                        self._duct_fittings[name] += int(length / multiple)
                    else:
                        self._duct_fittings[name] = int(length / multiple)
            except:
                pass

    def _output(self, dictionary):
        for name in sorted(dictionary):
            print name + '\t' + 'ГОСТ 14918-2020' + '\t' + '' + '\t' + '' + '\t' \
            + 'шт.' + '\t' + str(dictionary[name])


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

    list_duct_fittings = []
    list_ducts = []

    elements = selection

    for element in elements:
        if element.Category.Name == 'Соединительные детали воздуховодов':
            list_duct_fittings.append(element)
        elif element.Category.Name == 'Воздуховоды':
            list_ducts.append(element)

    fittings = DuctFittings(list_duct_fittings, list_ducts)


