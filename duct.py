# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import Category, Parameter

class Duct(object):
    def __init__(self, list_elements_duct):
        self._list_elements_duct = list_elements_duct
        self._dict_ducts = {}

    def form_dict_ducts(self):
        for element in self._list_elements_duct:
            self._k = 'Воздуховод из тонколистовой оцинкованной стали ' \
            + element.LookupParameter('Размер').AsString() + ' мм'
            self._v = float(element.LookupParameter('Длина').AsValueString()) / 1000
            if self._k in self._dict_ducts.keys():
                self._dict_ducts[self._k] += self._v
            else:
                self._dict_ducts[self._k] = self._v

    def output(self):
        for k in self._dict_ducts:
            print k, ' ', self._dict_ducts[k]
        
        # for element in self._list_elements_duct:
        #     print 'Воздуховод из тонколистовой оцинкованной стали ', \
        #     element.LookupParameter('Размер').AsString() + ' мм', \
        #     float(element.LookupParameter('Длина').AsValueString()) / 1000