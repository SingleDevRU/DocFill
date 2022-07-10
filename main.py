from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import rq
import dw


def AddSymbol(string, value):
    while len(string) != value:
        string += " "

    return string


class MyTab(MDFloatLayout, MDTabsBase):
    pass


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

    def PostValue(self):
        self.parrent.ids.curkkt.text = self.ids.reg.text + "/" + self.ids.Date.text
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
        self.time.ids.input_clock_switch.disabled = True

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
        self.date.ids.edit_icon.disabled = True

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

    def on_focus(self, *args):
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

        MDTextField.on_focus(self, *args)

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
        self.menu.width_mult = 100
        self.menu.max_height = 300
        self.menu.position = "bottom"
        self.menu.ver_growth = "down"

    def on_focus(self, *args):
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

        MDTextField.on_focus(self, *args)

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

    def on_focus(self, *args):
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

        MDTextField.on_focus(self, *args)

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
        self.menu.width_mult = 4
        self.menu.max_height = 300
        self.menu.position = "bottom"
        self.menu.ver_growth = "down"

    def on_focus(self, *args):
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

        MDTextField.on_focus(self, *args)

    def Menu_callback(self, text):
        self.text = text
        self.menu.dismiss()


class MyInput(MDTextFieldRect):
    max_len = 0

    def insert_text(self, substring, from_undo=False):
        if len(self.text) == self.max_len > 0:
            substring = ""
        MDTextFieldRect.insert_text(self, substring, from_undo)


# class CurrentKKT(Screen):

# def RegN(self):
# self.manager.get_screen("Doc").ids.curkkt.text = self.ids.reg.text + "/" + self.ids.Date.text
# self.manager.current = "Doc"


class DocFill(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.DockMenu = MDDropdownMenu()
        self.UsersMenu = MDDropdownMenu()
        self.DeRegPop = DeReg()
        self.CurrKKT = CurrentKKT()
        self.CurrKKT.parrent = self

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
        if info:
            self.ids.ogrn.text = info[2]
            if info[0] == "fl":
                self.ids.name1.text = "ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ"
                self.ids.name2.text = info[1]
            else:
                self.ids.kpp.text = info[3]
                if "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ" in info[1]:
                    self.ids.name1.text = info[1][:40]
                    self.ids.name2.text = info[1][41:]
                elif "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО" in info[1]:
                    self.ids.name1.text = info[1][:30]
                    self.ids.name2.text = info[1][31:]
                elif "АКЦИОНЕРНОЕ ОБЩЕСТВО" in info[1]:
                    self.ids.name1.text = info[1][:20]
                    self.ids.name2.text = info[1][21:]

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
                 "ChekBoxes": (self.ids.ofd1, self.ids.ofd2, self.ids.ofd3, self.ids.ofd4, self.ids.ofd5, self.ids.ofd6,
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
                else:
                    if i == "TextFiled" or i == "ChekBoxes":
                        e.disabled = False

                    else:
                        e.readonly = False
                        e.background_color = MDTextFieldRect().background_color

        if text == "Перерегистрация":
            self.CurrKKT.open()

        if text == "Снятие с учета":
            self.DeRegPop.open()

        self.DockMenu.dismiss()

    def GetPostIndex(self):
        if self.ids.district.text == "":
            text = self.ids.city.text
        else:
            text = self.ids.district.text + "," + self.ids.village.text

        self.ids.ZipCode.text = rq.GetIndex(text) if rq.GetIndex(text) is not False else ""

    def GenerateXLSX(self):
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
                "DeReg": (self.DeRegPop.ids.Thief.active, self.DeRegPop.ids.Lost.active)
                }

        ogrn = self.ids.ogrn.text
        if len(ogrn) < 15:
            ogrn = AddSymbol(ogrn, 15)

        data["Primary"]["OGRN"] = ogrn

        inn = self.ids.inn.text
        if len(inn) != 12:
            inn = AddSymbol(inn, 12)

        data["Primary"]["INN"] = inn

        kpp = self.ids.kpp.text
        if len(kpp) != 9:
            kpp = AddSymbol(kpp, 9)

        data["Primary"]["KPP"] = kpp

        name1 = self.ids.name1.text
        if len(name1) != 40:
            name1 = AddSymbol(name1, 40)

        name2 = self.ids.name2.text
        if len(name2) != 40:
            name2 = AddSymbol(name2, 40)

        name3 = self.ids.name3.text
        if len(name3) != 40:
            name3 = AddSymbol(name3, 40)

        data["Primary"]["FullName"] = (name1, name2, name3)

        userf = self.ids.f.text
        if len(userf) != 20:
            userf = AddSymbol(userf, 20)

        useri = self.ids.i.text
        if len(useri) != 20:
            useri = AddSymbol(useri, 20)

        usero = self.ids.o.text
        if len(usero) != 20:
            usero = AddSymbol(usero, 20)

        data["Primary"]["UserFIO"] = (userf, useri, usero)

        doc1 = self.ids.d1.text
        if len(doc1) != 20:
            doc1 = AddSymbol(doc1, 20)

        doc2 = self.ids.d2.text
        if len(doc2) != 20:
            doc2 = AddSymbol(doc2, 20)

        doc3 = self.ids.d3.text
        if len(doc3) != 20:
            doc3 = AddSymbol(doc3, 20)

        data["Primary"]["Document"] = (doc1, doc2, doc3)

        model = self.ids.KKT.text
        if len(model) != 20:
            model = AddSymbol(model, 20)

        data["KKTandFN"]["Model"] = model

        KKTs = self.ids.seriesKKT.text
        if len(KKTs) != 20:
            KKTs = AddSymbol(KKTs, 20)

        data["KKTandFN"]["SerialKKT"] = KKTs

        FNs = self.ids.serialFN.text
        if len(FNs) != 20:
            FNs = AddSymbol(FNs, 20)

        data["KKTandFN"]["SerialFN"] = FNs

        FNname1 = self.ids.fn1.text
        if len(FNname1) != 20:
            FNname1 = AddSymbol(FNname1, 20)

        FNname2 = self.ids.fn2.text
        if len(FNname2) != 20:
            FNname2 = AddSymbol(FNname2, 20)

        FNname3 = self.ids.fn3.text
        if len(FNname3) != 20:
            FNname3 = AddSymbol(FNname3, 20)

        FNname4 = self.ids.fn4.text
        if len(FNname4) != 20:
            FNname4 = AddSymbol(FNname4, 20)

        FNname5 = self.ids.fn5.text
        if len(FNname5) != 20:
            FNname5 = AddSymbol(FNname5, 20)

        FNname6 = self.ids.fn6.text
        if len(FNname6) != 20:
            FNname6 = AddSymbol(FNname6, 20)

        data["KKTandFN"]["FNName"] = (FNname1, FNname2, FNname3, FNname4, FNname5, FNname6)

        distr = self.ids.district.text
        if len(distr) != 30:
            distr = AddSymbol(distr, 30)

        data["Address"]["District"] = distr

        city = self.ids.city.text
        if len(city) != 30:
            city = AddSymbol(city, 30)

        data["Address"]["City"] = city

        vill = self.ids.village.text
        if len(vill) != 30:
            vill = AddSymbol(vill, 30)

        data["Address"]["Village"] = vill

        Street = self.ids.street.text
        if len(Street) != 30:
            Street = AddSymbol(Street, 30)

        data["Address"]["Street"] = Street

        house = self.ids.house.text
        if len(house) != 8:
            house = AddSymbol(house, 8)

        data["Address"]["House"] = house

        camp = self.ids.campus.text
        if len(camp) != 8:
            camp = AddSymbol(camp, 8)

        data["Address"]["Campus"] = camp

        room = self.ids.room.text
        if len(room) != 8:
            room = AddSymbol(room, 8)

        data["Address"]["Room"] = room

        place1 = self.ids.exp1.text
        if len(place1) != 20:
            place1 = AddSymbol(place1, 20)

        place2 = self.ids.exp2.text
        if len(place2) != 20:
            place2 = AddSymbol(place2, 20)

        place3 = self.ids.exp3.text
        if len(place3) != 20:
            place3 = AddSymbol(place3, 20)

        data["Address"]["Place"] = (place1, place2, place3)

        OFDName1 = self.ids.ofdn1.text
        if len(OFDName1) != 20:
            OFDName1 = AddSymbol(OFDName1, 20)

        OFDName2 = self.ids.ofdn2.text
        if len(OFDName2) != 20:
            OFDName2 = AddSymbol(OFDName2, 20)

        OFDName3 = self.ids.ofdn3.text
        if len(OFDName3) != 20:
            OFDName3 = AddSymbol(OFDName3, 20)

        OFDName4 = self.ids.ofdn4.text
        if len(OFDName4) != 20:
            OFDName4 = AddSymbol(OFDName4, 20)

        data["OFD"]["OFDName"] = (OFDName1, OFDName2, OFDName3, OFDName4)

        OFDInn = self.ids.ofdinn.text
        if len(OFDInn) != 12:
            OFDInn = AddSymbol(OFDInn, 12)

        data["OFD"]["OFDInn"] = OFDInn

        Nreg = self.ids.Nregrep.text
        if len(Nreg) != 8:
            Nreg = AddSymbol(Nreg, 8)

        Nclos = self.ids.Nregclos.text
        if len(Nclos) != 8:
            Nclos = AddSymbol(Nclos, 8)

        data["Raports"]["RegRep"]["Nrep"] = Nreg

        data["Raports"]["ClosReg"]["Nrep"] = Nclos

        FPReg = self.ids.FPDockreg.text
        if len(FPReg) != 10:
            FPReg = AddSymbol(FPReg, 10)

        FPClos = self.ids.FPDockclos.text
        if len(FPClos) != 10:
            FPClos = AddSymbol(FPClos, 10)

        data["Raports"]["RegRep"]["FP"] = FPReg

        data["Raports"]["ClosReg"]["FP"] = FPClos

        dw.excelwork(data)


class MyApp(MDApp):
    def build(self):
        self.load_kv("interface.kv")
        # sm = ScreenManager()
        # sm.add_widget(DocFill(name='Doc'))
        # sm.add_widget(CurrentKKT(name='KKT'))

        return DocFill()


if __name__ == "__main__":
    MyApp().run()
