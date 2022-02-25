# -*- coding: utf-8 -*-

class Duct(object):
    def __init__(self, list_elements_duct):
        self._list_elements_duct = list_elements_duct
        self._round_ducts = {}
        self._rect_ducts = {}
        self._sort_ducts()
        self._final_len(self._round_ducts, 3)
        self._final_len(self._rect_ducts, 1.5)
        self._output(self._rect_ducts)
        self._output(self._round_ducts)

    def _calc_thick_round_duct(self, diameter):
        if int(diameter) >= 1000:
            thick = 'δ=1.0 мм'
        elif 315 <= int(diameter) < 1000:
            thick = 'δ=0.7 мм'
        else:
            thick = 'δ=0.5 мм'
        return thick

    def _calc_thick_rect_duct(self, width, height):
        if int(width) >= 1000 or int(height) >= 1000:
            thick = 'δ=1.0 мм'
        elif 300 <= int(width) < 1000 or 300 <= int(width) < 1000:
            thick = 'δ=0.7 мм'
        else:
            thick = 'δ=0.5 мм'
        return thick

    def _name_for_round_duct(self, diameter):
        thick = self._calc_thick_round_duct(diameter)
        return 'Воздуховод из тонколистовой оцинкованной стали ø' \
            + str(diameter) + ' мм, ' + thick \
            + ', класс герметичности В'

    def _name_for_rect_duct(self, width, height):
        thick = self._calc_thick_rect_duct(width, height)
        if int(width) >= int(height):
            size = width + 'x' + height
        else:
            size = height + 'x' + width
        return 'Воздуховод из тонколистовой оцинкованной стали ' \
            + size + ' мм' + thick \
            + ', класс герметичности В'

    def _final_len(self, dict_ducts,  multiple):
        for name in dict_ducts:
            dict_ducts[name] = round(dict_ducts[name] / multiple * 1.2 + 0.5) * multiple

    def _sort_ducts(self):
        for element in self._list_elements_duct:
            try:
                self._diameter = element.LookupParameter('Диаметр').AsValueString()
                self._length = float(element.LookupParameter('Длина').AsValueString()) / 1000
                name = self._name_for_round_duct(self._diameter)
                if name in self._round_ducts.keys():
                    self._round_ducts[name] += self._length
                else:
                    self._round_ducts[name] = self._length
            except:
                self._width = element.LookupParameter('Ширина').AsValueString()
                self._height = element.LookupParameter('Высота').AsValueString()
                self._length = float(element.LookupParameter('Длина').AsValueString()) / 1000
                name = self._name_for_rect_duct(self._width, self._height)
                if name in self._rect_ducts.keys():
                    self._rect_ducts[name] += self._length
                else:
                    self._rect_ducts[name] = self._length

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

    list_elements_duct = []

    for element in selection:
        if element.Category.Name == 'Воздуховоды':
            list_elements_duct.append(element)

    ducts = Duct(list_elements_duct)# -*- coding: utf-8 -*-

class Duct(object):
    def __init__(self, list_elements_duct):
        self._list_elements_duct = list_elements_duct
        self._round_ducts = {}
        self._rect_ducts = {}
        self._sort_ducts()
        self._final_len(self._round_ducts, 3)
        self._final_len(self._rect_ducts, 1.5)
        self._output(self._rect_ducts)
        self._output(self._round_ducts)

    def _calc_thick_round_duct(self, diameter):
        if int(diameter) >= 1000:
            thick = 'δ=1.0 мм'
        elif 315 <= int(diameter) < 1000:
            thick = 'δ=0.7 мм'
        else:
            thick = 'δ=0.5 мм'
        return thick

    def _calc_thick_rect_duct(self, width, height):
        if int(width) >= 1000 or int(height) >= 1000:
            thick = 'δ=1.0 мм'
        elif 300 <= int(width) < 1000 or 300 <= int(width) < 1000:
            thick = 'δ=0.7 мм'
        else:
            thick = 'δ=0.5 мм'
        return thick

    def _name_for_round_duct(self, diameter):
        thick = self._calc_thick_round_duct(diameter)
        return 'Воздуховод из тонколистовой оцинкованной стали ø' \
            + str(diameter) + ' мм, ' + thick \
            + ', класс герметичности В'

    def _name_for_rect_duct(self, width, height):
        thick = self._calc_thick_rect_duct(width, height)
        if int(width) >= int(height):
            size = width + 'x' + height
        else:
            size = height + 'x' + width
        return 'Воздуховод из тонколистовой оцинкованной стали ' \
            + size + ' мм' + thick \
            + ', класс герметичности В'

    def _final_len(self, dict_ducts,  multiple):
        for name in dict_ducts:
            dict_ducts[name] = round(dict_ducts[name] / multiple * 1.2 + 0.5) * multiple

    def _sort_ducts(self):
        for element in self._list_elements_duct:
            try:
                self._diameter = element.LookupParameter('Диаметр').AsValueString()
                self._length = float(element.LookupParameter('Длина').AsValueString()) / 1000
                name = self._name_for_round_duct(self._diameter)
                if name in self._round_ducts.keys():
                    self._round_ducts[name] += self._length
                else:
                    self._round_ducts[name] = self._length
            except:
                self._width = element.LookupParameter('Ширина').AsValueString()
                self._height = element.LookupParameter('Высота').AsValueString()
                self._length = float(element.LookupParameter('Длина').AsValueString()) / 1000
                name = self._name_for_rect_duct(self._width, self._height)
                if name in self._rect_ducts.keys():
                    self._rect_ducts[name] += self._length
                else:
                    self._rect_ducts[name] = self._length

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

    list_elements_duct = []

    for element in selection:
        if element.Category.Name == 'Воздуховоды':
            list_elements_duct.append(element)

    ducts = Duct(list_elements_duct)
