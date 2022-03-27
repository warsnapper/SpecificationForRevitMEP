import clr
clr.AddReference('RevitAPI')

# from ducts import Ducts
# from fittings import Fittings

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

list_shaped_elements = []
list_ducts = []

elements = selection

for element in elements:
    if element.Category.Name == 'Соединительные детали воздуховодов':
        list_shaped_elements.append(element)
    elif element.Category.Name == 'Воздуховоды':
        list_ducts.append(element)

class Ducts(object):
    def __init__(self, list_ducts):
        self._list_ducts = list_ducts
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
            + size + ' мм, ' + thick \
            + ', класс герметичности В'

    def _final_len(self, dict_ducts, multiple):
        for name in dict_ducts:
            dict_ducts[name] = round(dict_ducts[name] / multiple * 1.2 + 0.5) * multiple

    def _sort_ducts(self):
        for element in self._list_ducts:
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
            + 'м' + '\t' + str(dictionary[name])

class Fittings(object):
    def __init__(self, list_shaped_elements, list_ducts):
        self._shaped_elements = {}
        self._sort_shaped_elements(list_shaped_elements)
        self._nipples(list_ducts, 3)
        self._output(self._shaped_elements)

    def _sort_shaped_elements(self, list_shaped_elements):
        for element in list_shaped_elements:
            elementId = element.GetTypeId()
            typesize = doc.GetElement(elementId)
            comment = typesize.LookupParameter('Комментарии к типоразмеру').AsString()
            if comment == 'Ниппель круглого воздуховода':
                continue
            elif comment == None:
                comment = ''
            size = element.LookupParameter('Размер').AsString()
            name = comment + ' ' + size + ' мм.'
            if name in self._shaped_elements.keys():
                self._shaped_elements[name] += 1
            else:
                self._shaped_elements[name] = 1

    def _nipples(self, list_ducts, multiple):
        for element in list_ducts:
            try:
                diameter = element.LookupParameter('Диаметр').AsValueString()
                length = float(element.LookupParameter('Длина').AsValueString()) / 1000
                name = 'Ниппель круглого воздуховода ø' + diameter + ' мм.'
                if int(length / multiple):
                    if name in self._shaped_elements.keys():
                        self._shaped_elements[name] += int(length / multiple)
                    else:
                        self._shaped_elements[name] = int(length / multiple)
            except:
                pass

    def _output(self, dictionary):
        for name in sorted(dictionary):
            print name + '\t' + 'ГОСТ 14918-2020' + '\t' + '' + '\t' + '' + '\t' \
            + 'шт.' + '\t' + str(dictionary[name])

ducts = Ducts(list_ducts)
fittings = Fittings(list_shaped_elements, list_ducts)