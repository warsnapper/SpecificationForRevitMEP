# -*- coding: utf-8 -*-

class InsulationDucts(object):
    def __init__(self, list_ducts, quotient):
        self._instulation = {}
        self._sort(list_ducts)
        self._final_square(self._instulation, quotient)
        self._output(self._instulation)

    def _name(self, type_insulation):
        if 'EI' in type_insulation:
            first_part = 'Покрытие огнезащитное'
        else:
            first_part = 'Теплоизоляция'
        maker = ''
        if 'Firestill' in type_insulation:
            maker = 'Лигресс'
        if 'K-Flex' in type_insulation:
            maker = 'K-Flex'
        name = first_part + '\t' + type_insulation + '\t' + '' + '\t' \
               + maker +'\t' + 'м²' + '\t'
        return name

    def _sort(self, list_ducts):
        for element in list_ducts:
            type_insulation = element.LookupParameter('Тип изоляции').AsString()
            if type_insulation:
                square = element.LookupParameter('Площадь').AsValueString()
                square = float(square.replace(',', '.'))
                name = self._name(type_insulation)
                if name in self._instulation.keys():
                    self._instulation[name] += square
                else:
                    self._instulation[name] = square

    def _final_square(self, dictionary, quotient):
        for elem in dictionary:
            dictionary[elem] = int(round(dictionary[elem] * quotient + 0.5))

    def _output(self, dictionary):
        for name in sorted(dictionary):
            print name + str(dictionary[name])

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

    list_ducts = []

    for element in selection:
        if element.Category.Name == 'Воздуховоды':
            list_ducts.append(element)

    insulation_ducts = InsulationDucts(list_ducts, 1.35)