from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivymd.uix.filemanager import MDFileManager

from os import listdir

import rq
import dw


def AddSymbol(string, value):
    while len(string) != value:
        string += " "

    return string


class MyTab(MDFloatLayout, MDTabsBase):
    pass


class FileNameEnter(MDTextFieldRect):

    def insert_text(self, substring, from_undo=False):
        if substring in ("'", "\"", "<", ">", "\\", "|", "/", ".", ",", "?", "!", ":", ";", "+", "-", "*"):
            substring = ""

        MDTextFieldRect.insert_text(self, substring, from_undo)


class Path(MDFileManager):
    pass


class AttentionPopup(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.title = "Внимание!"
        self.size_hint = (None, None)
        self.size = (550, 250)
        self.title_color = (0, 0, 0)
        self.background_color = (255, 255, 255)
        self.auto_dismiss = False


class CurrentKKT(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.title = "Рег. номер ККТ"
        self.size_hint = (None, None)
        self.size = (550, 250)
        self.title_color = (0, 0, 0)
        self.background_color = (255, 255, 255)
        self.auto_dismiss = False
        self.parrent = ObjectProperty()

    def Clear(self):
        self.ids.Date.text = ""
        self.ids.reg.text = ""
        self.parrent.ids.curkkt.text = ""

    def PostValue(self):
        self.parrent.ids.curkkt.text = self.ids.reg.text + ("/" if self.ids.reg.text != "" and self.ids.Date.text != ""
                                                            else "") + self.ids.Date.text
        self.dismiss()


class DeReg(Popup):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.title = "Причина снятия ккт с учета"
        self.size_hint = (None, None)
        self.size = (550, 250)
        self.title_color = (0, 0, 0)
        self.background_color = (255, 255, 255)
        self.auto_dismiss = False


class Time(MDTextField):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.time = MDTimePicker()

    def on_focus(self, *args):
        self.time.bind(on_save=self.GetTime)
        if self.focus:
            self.time.open()
        MDTextField.on_focus(self, *args)

    def GetTime(self, instance, time):
        StTime = str(time).split(":")
        self.text = StTime[0] + ":" + StTime[1]
        self.time.dismiss()


class Date(MDTextField):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.date = MDDatePicker()

    def on_focus(self, *args):
        self.date.elem = self
        self.date.bind(on_save=self.on_save)
        if self.focus:
            self.date.open()

        MDTextField.on_focus(self, *args)

    def on_save(self, instance, value, date_range):
        date = str(value).split("-")
        monthlist = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября",
                     "октября", "ноября", "декабря")
        self.text = date[2] + " " + monthlist[int(date[1]) - 1] + " " + date[0]

        self.date.dismiss()


class OFDMenu(MDTextField):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.parrent = ObjectProperty()
        self.menu = MDDropdownMenu()
        self.menu.caller = self
        self.menu.width_mult = 100
        self.menu.max_height = 300
        self.menu.position = "bottom"
        self.menu.ver_growth = "down"

    def set_text(self, instance_text_field, text: str) -> None:
        self.menu.items = [
            {
                "text": f'{i}',
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'{i}': self.Menu_callback(x)
            } for i in dw.GetOFD() if self.text.lower() in str(i).lower()
        ]

        if self.focus:
            self.menu.dismiss()
            self.menu.open()

        MDTextField.set_text(self, instance_text_field, text)

    def Menu_callback(self, text):
        items = dw.GetOFD()
        self.parrent.ids.OFD.text = text
        self.parrent.ids.ofdn1.text = items[text][0][0] if items[text][0][0] is not None else ""
        self.parrent.ids.ofdn2.text = items[text][0][1] if items[text][0][1] is not None else ""
        self.parrent.ids.ofdn3.text = items[text][0][2] if items[text][0][2] is not None else ""
        self.parrent.ids.ofdn4.text = items[text][0][3] if items[text][0][3] is not None else ""
        self.parrent.ids.ofdinn.text = items[text][1] if items[text][1] is not None else ""

        self.menu.dismiss()


class RegionMenu(MDTextField):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu = MDDropdownMenu()
        self.menu.caller = self
        self.menu.width_mult = 7
        self.menu.max_height = 300
        self.menu.position = "bottom"
        self.menu.ver_growth = "down"

    def set_text(self, instance_text_field, text: str) -> None:
        self.menu.items = [
            {
                "text": f'{i}',
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'{i}': self.Menu_callback(x)
            } for i in dw.GetRegions() if self.text.lower() in str(i).lower()
        ]

        if self.focus:
            self.menu.dismiss()
            self.menu.open()

        MDTextField.set_text(self, instance_text_field, text)

    def Menu_callback(self, text):
        self.text = text
        self.menu.dismiss()


class MenuFN(MDTextField):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.parrent = ObjectProperty()
        self.menu = MDDropdownMenu()
        self.menu.caller = self
        self.menu.width_mult = 100
        self.menu.max_height = 300
        self.menu.position = "bottom"
        self.menu.ver_growth = "down"

    def set_text(self, instance_text_field, text: str) -> None:
        self.menu.items = [
            {
                "text": f'{i}',
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'{i}': self.Menu_callback(x)
            } for i in dw.GetFN() if self.text.lower() in i.lower()
        ]

        if self.focus:
            self.menu.dismiss()
            self.menu.open()

        MDTextField.set_text(self, instance_text_field, text)

    def Menu_callback(self, text):
        items = dw.GetFN()
        self.text = text
        self.parrent.ids.fn1.text = items[text][0] if items[text][0] is not None else ""
        self.parrent.ids.fn2.text = items[text][1] if items[text][1] is not None else ""
        self.parrent.ids.fn3.text = items[text][2] if items[text][2] is not None else ""
        self.parrent.ids.fn4.text = items[text][3] if items[text][3] is not None else ""
        self.parrent.ids.fn5.text = items[text][4] if items[text][4] is not None else ""
        self.parrent.ids.fn6.text = items[text][5] if items[text][5] is not None else ""

        self.menu.dismiss()


class MenuKKT(MDTextField):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu = MDDropdownMenu()
        self.menu.caller = self
        self.menu.width_mult = 3.7
        self.menu.max_height = 300
        self.menu.position = "bottom"
        self.menu.ver_growth = "down"

    def set_text(self, instance_text_field, text: str) -> None:
        self.menu.items = [
            {
                "text": f'{i}',
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'{i}': self.Menu_callback(x)
            } for i in dw.GetKKT() if self.text.lower() in i.lower()
        ]

        if self.focus:
            self.menu.dismiss()
            self.menu.open()

        MDTextField.set_text(self, instance_text_field, text)

    def Menu_callback(self, text):
        self.text = text
        self.menu.dismiss()


class MyInput(MDTextFieldRect):
    max_len = 0

    def insert_text(self, substring, from_undo=False):
        if len(self.text) == self.max_len > 0:
            substring = ""
        MDTextFieldRect.insert_text(self, substring, from_undo)


class AutoCalcDevice(Screen):

    def GetPostIndex(self, district, city, village, ZipCode):
        if district.text == "":
            text = city.text
        else:
            text = district.text + "," + village.text

        ZipCode.text = rq.GetIndex(text) if rq.GetIndex(text) is not False else ""

    def CloseWindow(self):
        self.manager.current = "Doc"


class DocFill(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.DockMenu = MDDropdownMenu(position="bottom")
        self.UsersMenu = MDDropdownMenu(position="bottom")
        self.DeRegPop = DeReg()
        self.CurrKKT = CurrentKKT()
        self.CurrKKT.parrent = self
        self.SavePath = Path(exit_manager=self.exit_manager,
                             select_path=self.select_path)
        self.Attention = AttentionPopup()

    def select_path(self, path):
        name = self.SavePath.ids.FName.text
        try:
            filename = name if name[len(name) - 1] != " " else name[:-1]
        except IndexError:
            pass
        else:
            if filename + ".xlsx" in listdir(path):
                self.Attention.ids.msg.text = f"Файл с именем {filename}.xlsx уже существует!"
                self.Attention.open()
                return

            pathtosave = path + "\\" + filename + ".xlsx"
            self.GenerateXLSX(pathtosave)
            self.exit_manager()

    def exit_manager(self, *args):
        self.SavePath.close()

    def OpenPath(self):
        self.SavePath.show_disks()

    def ULActive(self):
        self.ids.inn.max_len = 10
        self.ids.ogrn.max_len = 13
        self.ids.kpp.readonly = False
        self.ids.kpp.background_color = MDTextFieldRect().background_color

    def FLActive(self):
        self.ids.inn.max_len = 12
        self.ids.ogrn.max_len = 15
        self.ids.kpp.readonly = True
        self.ids.kpp.background_color = 0, 0, 0, .4

    def request(self, inn):
        info = rq.EgrulRq(inn)
        self.ids.ogrn.text = ""
        self.ids.kpp.text = ""
        if info:
            self.ids.ogrn.text = info[2]
            if info[0] == "fl":
                self.ids.name1.text = "ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ"
                self.ids.name2.text = info[1]
            else:
                self.ids.kpp.text = info[3]
                if "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ" in info[1].upper():
                    self.ids.name1.text = "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ"
                    self.ids.name2.text = info[1][41:] if len(info[1]) < 80 else info[1][41:80]
                    self.ids.name3.text = "" if len(info[1]) < 80 else info[1][81:]
                elif "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО" in info[1].upper():
                    self.ids.name1.text = "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО"
                    self.ids.name2.text = info[1][31:] if len(info[1]) < 71 else info[1][31:71]
                    self.ids.name3.text = "" if len(info[1]) < 71 else info[1][72:]
                elif "АКЦИОНЕРНОЕ ОБЩЕСТВО" in info[1]:
                    self.ids.name1.text = "АКЦИОНЕРНОЕ ОБЩЕСТВО"
                    self.ids.name2.text = info[1][21:] if len(info[1]) < 61 else info[1][21:61]
                    self.ids.name3.text = "" if len(info[1]) < 61 else info[1][62:]

    def MenuDock(self):

        self.DockMenu.caller = self.ids.DockType
        self.DockMenu.items = [
            {
                "text": f'{i}',
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'{i}': self.MenuDock_callback(x)
            } for i in ("Регистрация", "Перерегистрация", "Снятие с учета")
        ]
        self.DockMenu.width_mult = 2.69
        self.DockMenu.max_height = 150

        self.DockMenu.open()

    def UserMenu(self):
        self.UsersMenu.caller = self.ids.User
        self.UsersMenu.items = [
            {
                "text": f'{i}',
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'{i}': self.MenuUser_callback(x)
            } for i in ("Пользователь", "Представитель")
        ]
        self.UsersMenu.width_mult = 2.5
        self.UsersMenu.max_height = 100

        self.UsersMenu.open()

    def MenuUser_callback(self, text):
        self.ids.User.text = text

        for i in (self.ids.d1, self.ids.d2, self.ids.d3):
            if text == "Представитель":
                i.readonly = False
                i.background_color = MDTextFieldRect().background_color
            else:
                i.readonly = True
                i.text = ""
                i.background_color = 0, 0, 0, .4

        self.UsersMenu.dismiss()

    def MenuDock_callback(self, text):
        self.ids.DockType.text = text
        for i in (self.ids.r1, self.ids.r2, self.ids.r3, self.ids.r4,
                  self.ids.r5, self.ids.r6, self.ids.r7, self.ids.r8):

            if text == "Регистрация" or text == "Снятие с учета":
                i.disabled = True
            else:
                i.disabled = False

        elems = {"TextFiled": (self.ids.FN, self.ids.OFD, self.ids.region),
                 "TextInput": (self.ids.ogrn, self.ids.fn1, self.ids.fn2, self.ids.fn3, self.ids.fn4, self.ids.fn5,
                               self.ids.fn6, self.ids.serialFN, self.ids.ZipCode, self.ids.district, self.ids.city,
                               self.ids.village, self.ids.street, self.ids.house, self.ids.campus, self.ids.room,
                               self.ids.exp1, self.ids.exp2, self.ids.exp3, self.ids.ofdn1, self.ids.ofdn2,
                               self.ids.ofdn3, self.ids.ofdn4, self.ids.ofdinn),
                 "ChekBoxes": (self.ids.ofd1, self.ids.ofd2, self.ids.ofd3, self.ids.ofd4, self.ids.ofd5,
                               self.ids.ofd7, self.ids.ofd8, self.ids.ofd9, self.ids.ofd10, self.ids.ofd11,
                               self.ids.ofd12)
                 }
        for i, j in elems.items():
            for e in j:
                if text == "Снятие с учета":
                    if i == "TextFiled" or i == "ChekBoxes":
                        e.disabled = True

                    else:
                        e.readonly = True
                        e.background_color = 0, 0, 0, .4
                        e.text = ""
                    self.ids.AL1.disabled, self.ids.AL1.active = True, False
                    self.ids.AL2.disabled, self.ids.AL2.active = True, False
                else:
                    if i == "TextFiled" or i == "ChekBoxes":
                        e.disabled = False

                    else:
                        e.readonly = False
                        e.background_color = MDTextFieldRect().background_color

        if text == "Перерегистрация":
            self.CurrKKT.open()

        elif text == "Снятие с учета":
            self.DeRegPop.open()

        self.DockMenu.dismiss()

    def GetPostIndex(self):
        if self.ids.district.text == "":
            text = self.ids.city.text
        else:
            text = self.ids.district.text + "," + self.ids.village.text

        self.ids.ZipCode.text = rq.GetIndex(text) if rq.GetIndex(text) is not False else ""

    def GenerateXLSX(self, path):
        if self.ids.Date.text == "":
            self.Attention.ids.msg.text = "Укажите дату документа!"
            self.Attention.open()
            return

        elif not self.ids.RegRep.active and (self.ids.DateReg.text == "" or self.ids.TimeReg.text == ""):
            dateortime = "дату" if self.ids.DateReg.text == "" else "время"
            self.Attention.ids.msg.text = f"Укажите {dateortime} отчета о регистрации!"
            self.Attention.open()
            return

        elif not self.ids.RegClose.active and (self.ids.Dateclos.text == "" or self.ids.Timeclos.text == ""):
            dateortime = "дату" if self.ids.Dateclos.text == "" else "время"
            self.Attention.ids.msg.text = f"Укажите {dateortime} отчета о закрытии ФН!"
            self.Attention.open()
            return

        data = {"Primary": {"TypeUser": (self.ids.TG1.active, self.ids.TG2.active),
                            "TypeDock": self.ids.DockType.text,
                            "CurKkt": self.ids.curkkt.text,
                            "DateDock": self.ids.Date.text,
                            "User": self.ids.User.text,
                            "Resons": (self.ids.r1.active, self.ids.r2.active, self.ids.r3.active,
                                       self.ids.r4.active, self.ids.r5.active, self.ids.r6.active,
                                       self.ids.r7.active, self.ids.r8.active)
                            },
                "KKTandFN": {},
                "Address": {"index": self.ids.ZipCode.text,
                            "RegionCode": self.ids.region.text[:2]},
                "OFD": {"Using": (self.ids.ofd1.active, self.ids.ofd2.active, self.ids.ofd3.active,
                                  self.ids.ofd4.active, self.ids.ofd5.active, self.ids.ofd7.active,
                                  self.ids.ofd6.active, self.ids.ofd12.active, self.ids.ofd8.active,
                                  self.ids.ofd9.active, self.ids.ofd10.active, self.ids.ofd11.active)},
                "Raports": {"FNBroken": self.ids.FNBroken.active,
                            "RegRep": {"OnRegRep": self.ids.RegRep.active,
                                       "Date": self.ids.DateReg.text,
                                       "Time": self.ids.TimeReg.text
                                       },
                            "ClosReg": {"OnRegClose": self.ids.RegClose.active,
                                        "Date": self.ids.Dateclos.text,
                                        "Time": self.ids.Timeclos.text
                                        }
                            },
                "DeReg": (self.DeRegPop.ids.Thief.active, self.DeRegPop.ids.Lost.active),
                "AutoCalcDevice": {"device1": {"index": self.manager.get_screen("ACD").ids.ZipCode1.text,
                                               "regioncode": self.manager.get_screen("ACD").ids.region1.text[:2]
                                               },
                                   "device2": {"index": self.manager.get_screen("ACD").ids.ZipCode2.text,
                                               "regioncode": self.manager.get_screen("ACD").ids.region2.text[:2]
                                               }
                                   },
                "NumberOfSheets": (self.ids.AL1.active, self.ids.AL2.active)
                }

        data["Primary"]["OGRN"] = AddSymbol(self.ids.ogrn.text, 15)
        data["Primary"]["INN"] = AddSymbol(self.ids.inn.text, 12)
        data["Primary"]["KPP"] = AddSymbol(self.ids.kpp.text, 9)

        data["Primary"]["FullName"] = (AddSymbol(self.ids.name1.text, 40), AddSymbol(self.ids.name2.text, 40),
                                       AddSymbol(self.ids.name3.text, 40))

        data["Primary"]["UserFIO"] = (AddSymbol(self.ids.f.text, 20), AddSymbol(self.ids.i.text, 20),
                                      AddSymbol(self.ids.o.text, 20))

        data["Primary"]["Document"] = (AddSymbol(self.ids.d1.text, 20), AddSymbol(self.ids.d2.text, 20),
                                       AddSymbol(self.ids.d3.text, 20))

        data["KKTandFN"]["Model"] = AddSymbol(self.ids.KKT.text, 20)
        data["KKTandFN"]["SerialKKT"] = AddSymbol(self.ids.seriesKKT.text, 20)
        data["KKTandFN"]["SerialFN"] = AddSymbol(self.ids.serialFN.text, 20)

        data["KKTandFN"]["FNName"] = (AddSymbol(self.ids.fn1.text, 20), AddSymbol(self.ids.fn2.text, 20),
                                      AddSymbol(self.ids.fn3.text, 20), AddSymbol(self.ids.fn4.text, 20),
                                      AddSymbol(self.ids.fn5.text, 20), AddSymbol(self.ids.fn6.text, 20))

        data["Address"]["District"] = AddSymbol(self.ids.district.text, 30)
        data["Address"]["City"] = AddSymbol(self.ids.city.text, 30)
        data["Address"]["Village"] = AddSymbol(self.ids.village.text, 30)
        data["Address"]["Street"] = AddSymbol(self.ids.street.text, 30)
        data["Address"]["House"] = AddSymbol(self.ids.house.text, 8)
        data["Address"]["Campus"] = AddSymbol(self.ids.campus.text, 8)
        data["Address"]["Room"] = AddSymbol(self.ids.room.text, 8)

        data["Address"]["Place"] = (AddSymbol(self.ids.exp1.text, 20), AddSymbol(self.ids.exp2.text, 20),
                                    AddSymbol(self.ids.exp3.text, 20))

        data["OFD"]["OFDName"] = (AddSymbol(self.ids.ofdn1.text, 20), AddSymbol(self.ids.ofdn2.text, 20),
                                  AddSymbol(self.ids.ofdn3.text, 20), AddSymbol(self.ids.ofdn4.text, 20))

        data["OFD"]["OFDInn"] = AddSymbol(self.ids.ofdinn.text, 12)

        data["Raports"]["RegRep"]["Nrep"] = AddSymbol(self.ids.Nregrep.text, 8)
        data["Raports"]["ClosReg"]["Nrep"] = AddSymbol(self.ids.Nregclos.text, 8)
        data["Raports"]["RegRep"]["FP"] = AddSymbol(self.ids.FPDockreg.text, 10)
        data["Raports"]["ClosReg"]["FP"] = AddSymbol(self.ids.FPDockclos.text, 10)

        if self.ids.ofd6.active:
            ACD = self.manager.get_screen('ACD')
            data["AutoCalcDevice"]["device1"]["district"] = AddSymbol(ACD.ids.district1.text, 30)
            data["AutoCalcDevice"]["device1"]["city"] = AddSymbol(ACD.ids.city1.text, 30)
            data["AutoCalcDevice"]["device1"]["village"] = AddSymbol(ACD.ids.village1.text, 30)
            data["AutoCalcDevice"]["device1"]["street"] = AddSymbol(ACD.ids.street1.text, 30)
            data["AutoCalcDevice"]["device1"]["house"] = AddSymbol(ACD.ids.house1.text, 8)
            data["AutoCalcDevice"]["device1"]["campus"] = AddSymbol(ACD.ids.campus1.text, 8)
            data["AutoCalcDevice"]["device1"]["room"] = AddSymbol(ACD.ids.room1.text, 8)
            data["AutoCalcDevice"]["device1"]["place"] = (AddSymbol(ACD.ids.expd1_1.text, 20),
                                                          AddSymbol(ACD.ids.expd1_2.text, 20),
                                                          AddSymbol(ACD.ids.expd1_3.text, 20))
            data["AutoCalcDevice"]["device1"]["number"] = AddSymbol(ACD.ids.n1.text, 20)

            data["AutoCalcDevice"]["device2"]["district"] = AddSymbol(ACD.ids.district2.text, 30)
            data["AutoCalcDevice"]["device2"]["city"] = AddSymbol(ACD.ids.city2.text, 30)
            data["AutoCalcDevice"]["device2"]["village"] = AddSymbol(ACD.ids.village2.text, 30)
            data["AutoCalcDevice"]["device2"]["street"] = AddSymbol(ACD.ids.street2.text, 30)
            data["AutoCalcDevice"]["device2"]["house"] = AddSymbol(ACD.ids.house2.text, 8)
            data["AutoCalcDevice"]["device2"]["campus"] = AddSymbol(ACD.ids.campus2.text, 8)
            data["AutoCalcDevice"]["device2"]["room"] = AddSymbol(ACD.ids.room2.text, 8)
            data["AutoCalcDevice"]["device2"]["place"] = (AddSymbol(ACD.ids.expd2_1.text, 20),
                                                          AddSymbol(ACD.ids.expd2_2.text, 20),
                                                          AddSymbol(ACD.ids.expd2_3.text, 20))
            data["AutoCalcDevice"]["device2"]["number"] = AddSymbol(ACD.ids.n2.text, 20)

        dw.excelwork(data, path)


class MyApp(MDApp):
    def build(self):
        self.title = "DocFill"
        self.theme_cls.accent_palette = "Red"
        self.load_kv("interface.kv")
        sm = ScreenManager()
        sm.add_widget(DocFill(name='Doc'))
        sm.add_widget(AutoCalcDevice(name='ACD'))

        return sm


if __name__ == "__main__":
    MyApp().run()
