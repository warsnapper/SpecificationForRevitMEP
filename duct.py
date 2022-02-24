# -*- coding: utf-8 -*-

class Duct(object):
    def __init__(self, list_elements_duct):
        self._list_elements_duct = list_elements_duct
        self._round_ducts = {}
        self._sort_ducts()
        self._output(self._round_ducts)

    def _calc_thickness_round_duct(self, diameter):
        if int(diameter) >= 1000:
            self._thickness = 'δ=1,0 мм'
        elif 315 <= int(diameter) < 1000:
            self._thickness = 'δ=0,7 мм'
        else:
            self._thickness = 'δ=0,5 мм'
        return self._thickness

    def _name_for_round_duct(self, diameter):
        thickness = self._calc_thickness_round_duct(diameter)
        return 'Воздуховод из тонколистовой оцинкованной стали ø' \
            + str(diameter) + ' мм, ' + thickness \
            + ', класс герметичности В'

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
                print self._width, 'x', self._height 

    def form_dict_ducts(self):
        for element in self._list_elements_duct:
            self._k = 'Воздуховод из тонколистовой оцинкованной стали ' \
            + element.LookupParameter('Размер').AsString() + ' мм'
            self._v = float(element.LookupParameter('Длина').AsValueString()) / 1000
            if self._k in self._dict_ducts.keys():
                self._dict_ducts[self._k] += self._v
            else:
                self._dict_ducts[self._k] = self._v

    def _output(self, dictionary):
        for k in dictionary:
            print k, ' ', dictionary[k]


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
