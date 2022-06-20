import xml.etree.ElementTree as ET
import openpyxl as opx


def FormatDate(date):
    dates = date.split(" ")

    datel = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября",
             "октября", "ноября", "декабря")

    month = datel.index(dates[1].lower()) + 1

    return dates[0] + ("0" + str(month) if len(str(month)) < 2 else str(month)) + dates[2]


def GetKKT():
    xml = ET.parse('./stuff/models.list')
    return tuple((model.text for model in xml.findall('Models/Model')))


def GetFN():
    FN = ET.parse("./stuff/fns.list")
    FNList = {}
    for i in FN.findall("FN"):
        FNList[i.find("Model").text] = [i.find(f'String{j}').text for j in range(1, 7)]

    return FNList


def GetRegions():
    rg = ET.parse("./stuff/regions.list")
    rglist = []
    for i in rg.findall("Regions"):
        rglist.append(i.find("Code").text + " " + i.find("Name").text)

    return rglist


def GetOFD():
    ofd = ET.parse("./stuff/ofd.list")
    ofdlist = {}
    for i in ofd.findall("OFD"):
        ofdlist[i.find("Name").text] = [i.find(f"String{j}").text for j in range(1, 5)], i.find("INN").text
    return ofdlist


def excelwork(data):
    f = opx.load_workbook("./stuff/2.xlsx")
    c = 0
    for i in f.sheetnames:
        c += 1
        f[i]["BX6"].value = "0"
        f[i]["CA6"].value = str(c)[0] if len(str(c)) == 2 else "0"
        f[i]["CD6"].value = str(c)[1] if len(str(c)) == 2 else str(c)

        ogrnl = (f[i]["AN1"], f[i]["AQ1"], f[i]["AT1"], f[i]["AW1"],
                 f[i]["AZ1"], f[i]["BC1"], f[i]["BF1"], f[i]["BI1"],
                 f[i]["BL1"], f[i]["BO1"], f[i]["BR1"], f[i]["BU1"],
                 f[i]["BX1"], f[i]["CA1"], f[i]["CD1"])

        for j in range(len(data["Primary"]["OGRN"])):
            ogrnl[j].value = data["Primary"]["OGRN"][j]

        innl = (f[i]["AN4"], f[i]["AQ4"], f[i]["AT4"], f[i]["AW4"],
                f[i]["AZ4"], f[i]["BC4"], f[i]["BF4"], f[i]["BI4"],
                f[i]["BL4"], f[i]["BO4"], f[i]["BR4"], f[i]["BU4"])

        for j in range(len(data["Primary"]["INN"])):
            innl[j].value = data["Primary"]["INN"][j]

        kppl = (f[i]["AN6"], f[i]["AQ6"], f[i]["AT6"], f[i]["AW6"],
                f[i]["AZ6"], f[i]["BC6"], f[i]["BF6"], f[i]["BI6"],
                f[i]["BL6"])

        for j in range(len(data["Primary"]["KPP"])):
            kppl[j].value = data["Primary"]["KPP"][j]

    f["стр.1"]["AA12"].value = "1" if data["Primary"]["TypeDock"] == "Регистрация" else "2"

    resonsl = (f["стр.1"]["AG15"], f["стр.1"]["AM15"], f["стр.1"]["AS15"], f["стр.1"]["AY15"],
               f["стр.1"]["BE15"], f["стр.1"]["BK15"], f["стр.1"]["BQ15"], f["стр.1"]["BW15"])

    if data["Primary"]["TypeDock"] == "Перерегистрация":
        for j in range(len(data["Primary"]["Resons"])):
            resonsl[j].value = "1" if data["Primary"]["Resons"][j] else "2"

        regn = data["Primary"]["CurKkt"].split("/")
        n = regn[0]
        if len(n) < 20:
            while len(n) != 20:
                n += " "
        regnl = (f["стр.2"]["V21"], f["стр.2"]["Y21"], f["стр.2"]["AB21"], f["стр.2"]["AE21"],
                 f["стр.2"]["AH21"], f["стр.2"]["AK21"], f["стр.2"]["AN21"], f["стр.2"]["AQ21"],
                 f["стр.2"]["AT21"], f["стр.2"]["AW21"], f["стр.2"]["AZ21"], f["стр.2"]["BC21"],
                 f["стр.2"]["BF21"], f["стр.2"]["BI21"], f["стр.2"]["BL21"], f["стр.2"]["BO21"],
                 f["стр.2"]["BR21"], f["стр.2"]["BU21"], f["стр.2"]["BX21"], f["стр.2"]["CA21"])

        for j in range(len(n)):
            regnl[j].value = n[j]

        regd = FormatDate(regn[1])

        datel = (f["стр.2"]["CM21"], f["стр.2"]["CP21"], f["стр.2"]["CV21"], f["стр.2"]["CY21"],
                 f["стр.2"]["DE21"], f["стр.2"]["DH21"], f["стр.2"]["DK21"], f["стр.2"]["DN21"])

        for j in range(len(regd)):
            datel[j].value = regd[j]

    fname1 = (f["стр.1"]["A17"], f["стр.1"]["D17"], f["стр.1"]["G17"], f["стр.1"]["J17"],
              f["стр.1"]["M17"], f["стр.1"]["P17"], f["стр.1"]["S17"], f["стр.1"]["V17"],
              f["стр.1"]["Y17"], f["стр.1"]["AB17"], f["стр.1"]["AE17"], f["стр.1"]["AH17"],
              f["стр.1"]["AK17"], f["стр.1"]["AN17"], f["стр.1"]["AQ17"], f["стр.1"]["AT17"],
              f["стр.1"]["AW17"], f["стр.1"]["AZ17"], f["стр.1"]["BC17"], f["стр.1"]["BF17"],
              f["стр.1"]["BI17"], f["стр.1"]["BL17"], f["стр.1"]["BO17"], f["стр.1"]["BR17"],
              f["стр.1"]["BU17"], f["стр.1"]["BX17"], f["стр.1"]["CA17"], f["стр.1"]["CD17"],
              f["стр.1"]["CG17"], f["стр.1"]["CJ17"], f["стр.1"]["CM17"], f["стр.1"]["CP17"],
              f["стр.1"]["CS17"], f["стр.1"]["CV17"], f["стр.1"]["CY17"], f["стр.1"]["DB17"],
              f["стр.1"]["DE17"], f["стр.1"]["DH17"], f["стр.1"]["DK17"], f["стр.1"]["DN17"])

    for j in range(len(data["Primary"]["FullName"][0])):
        fname1[j].value = data["Primary"]["FullName"][0][j]

    fname2 = (f["стр.1"]["A19"], f["стр.1"]["D19"], f["стр.1"]["G19"], f["стр.1"]["J19"],
              f["стр.1"]["M19"], f["стр.1"]["P19"], f["стр.1"]["S19"], f["стр.1"]["V19"],
              f["стр.1"]["Y19"], f["стр.1"]["AB19"], f["стр.1"]["AE19"], f["стр.1"]["AH19"],
              f["стр.1"]["AK19"], f["стр.1"]["AN19"], f["стр.1"]["AQ19"], f["стр.1"]["AT19"],
              f["стр.1"]["AW19"], f["стр.1"]["AZ19"], f["стр.1"]["BC19"], f["стр.1"]["BF19"],
              f["стр.1"]["BI19"], f["стр.1"]["BL19"], f["стр.1"]["BO19"], f["стр.1"]["BR19"],
              f["стр.1"]["BU19"], f["стр.1"]["BX19"], f["стр.1"]["CA19"], f["стр.1"]["CD19"],
              f["стр.1"]["CG19"], f["стр.1"]["CJ19"], f["стр.1"]["CM19"], f["стр.1"]["CP19"],
              f["стр.1"]["CS19"], f["стр.1"]["CV19"], f["стр.1"]["CY19"], f["стр.1"]["DB19"],
              f["стр.1"]["DE19"], f["стр.1"]["DH19"], f["стр.1"]["DK19"], f["стр.1"]["DN19"])

    for j in range(len(data["Primary"]["FullName"][1])):
        fname2[j].value = data["Primary"]["FullName"][1][j]

    fname3 = (f["стр.1"]["A21"], f["стр.1"]["D21"], f["стр.1"]["G21"], f["стр.1"]["J21"],
              f["стр.1"]["M21"], f["стр.1"]["P21"], f["стр.1"]["S21"], f["стр.1"]["V21"],
              f["стр.1"]["Y21"], f["стр.1"]["AB21"], f["стр.1"]["AE21"], f["стр.1"]["AH21"],
              f["стр.1"]["AK21"], f["стр.1"]["AN21"], f["стр.1"]["AQ21"], f["стр.1"]["AT21"],
              f["стр.1"]["AW21"], f["стр.1"]["AZ21"], f["стр.1"]["BC21"], f["стр.1"]["BF21"],
              f["стр.1"]["BI21"], f["стр.1"]["BL21"], f["стр.1"]["BO21"], f["стр.1"]["BR21"],
              f["стр.1"]["BU21"], f["стр.1"]["BX21"], f["стр.1"]["CA21"], f["стр.1"]["CD21"],
              f["стр.1"]["CG21"], f["стр.1"]["CJ21"], f["стр.1"]["CM21"], f["стр.1"]["CP21"],
              f["стр.1"]["CS21"], f["стр.1"]["CV21"], f["стр.1"]["CY21"], f["стр.1"]["DB21"],
              f["стр.1"]["DE21"], f["стр.1"]["DH21"], f["стр.1"]["DK21"], f["стр.1"]["DN21"])

    for j in range(len(data["Primary"]["FullName"][2])):
        fname3[j].value = data["Primary"]["FullName"][2][j]

    f["стр.1"]["AJ26"].value, f["стр.1"]["AM26"].value, f["стр.1"]["AP26"].value = "0", "1", "0"
    f["стр.1"]["N28"].value, f["стр.1"]["Q28"].value, f["стр.1"]["T28"].value = "0", "1", "0"

    f["стр.1"]["B33"].value = "1" if data["Primary"]["User"] == "Пользователь" else "2"

    userfio1 = (f["стр.1"]["A36"], f["стр.1"]["D36"], f["стр.1"]["G36"], f["стр.1"]["J36"],
                f["стр.1"]["M36"], f["стр.1"]["P36"], f["стр.1"]["S36"], f["стр.1"]["V36"],
                f["стр.1"]["Y36"], f["стр.1"]["AB36"], f["стр.1"]["AE36"], f["стр.1"]["AH36"],
                f["стр.1"]["AK36"], f["стр.1"]["AN36"], f["стр.1"]["AQ36"], f["стр.1"]["AT36"],
                f["стр.1"]["AW36"], f["стр.1"]["AZ36"], f["стр.1"]["BC36"], f["стр.1"]["BF36"])

    for j in range(len(data["Primary"]["UserFIO"][0])):
        userfio1[j].value = data["Primary"]["UserFIO"][0][j]

    userfio2 = (f["стр.1"]["A38"], f["стр.1"]["D38"], f["стр.1"]["G38"], f["стр.1"]["J38"],
                f["стр.1"]["M38"], f["стр.1"]["P38"], f["стр.1"]["S38"], f["стр.1"]["V38"],
                f["стр.1"]["Y38"], f["стр.1"]["AB38"], f["стр.1"]["AE38"], f["стр.1"]["AH38"],
                f["стр.1"]["AK38"], f["стр.1"]["AN38"], f["стр.1"]["AQ38"], f["стр.1"]["AT38"],
                f["стр.1"]["AW38"], f["стр.1"]["AZ38"], f["стр.1"]["BC38"], f["стр.1"]["BF38"])

    for j in range(len(data["Primary"]["UserFIO"][1])):
        userfio2[j].value = data["Primary"]["UserFIO"][1][j]

    userfio3 = (f["стр.1"]["A40"], f["стр.1"]["D40"], f["стр.1"]["G40"], f["стр.1"]["J40"],
                f["стр.1"]["M40"], f["стр.1"]["P40"], f["стр.1"]["S40"], f["стр.1"]["V40"],
                f["стр.1"]["Y40"], f["стр.1"]["AB40"], f["стр.1"]["AE40"], f["стр.1"]["AH40"],
                f["стр.1"]["AK40"], f["стр.1"]["AN40"], f["стр.1"]["AQ40"], f["стр.1"]["AT40"],
                f["стр.1"]["AW40"], f["стр.1"]["AZ40"], f["стр.1"]["BC40"], f["стр.1"]["BF40"])

    for j in range(len(data["Primary"]["UserFIO"][2])):
        userfio3[j].value = data["Primary"]["UserFIO"][2][j]

    datedock = (f["стр.1"]["AB45"], f["стр.1"]["AE45"], f["стр.1"]["AK45"], f["стр.1"]["AN45"],
                f["стр.1"]["AT45"], f["стр.1"]["AW45"], f["стр.1"]["AZ45"], f["стр.1"]["BC45"])

    dated = FormatDate(data["Primary"]["DateDock"])

    for j in range(len(dated)):
        datedock[j].value = dated[j]

    dockinfo1 = (f["стр.2"]["A12"], f["стр.2"]["D12"], f["стр.2"]["G12"], f["стр.2"]["J12"],
                 f["стр.2"]["M12"], f["стр.2"]["P12"], f["стр.2"]["S12"], f["стр.2"]["V12"],
                 f["стр.2"]["Y12"], f["стр.2"]["AB12"], f["стр.2"]["AE12"], f["стр.2"]["AH12"],
                 f["стр.2"]["AK12"], f["стр.2"]["AN12"], f["стр.2"]["AQ12"], f["стр.2"]["AT12"],
                 f["стр.2"]["AW12"], f["стр.2"]["AZ12"], f["стр.2"]["BC12"], f["стр.2"]["BF12"])

    for j in range(len(data["Primary"]["Document"][0])):
        dockinfo1[j].value = data["Primary"]["Document"][0][j]

    dockinfo2 = (f["стр.2"]["A14"], f["стр.2"]["D14"], f["стр.2"]["G14"], f["стр.2"]["J14"],
                 f["стр.2"]["M14"], f["стр.2"]["P14"], f["стр.2"]["S14"], f["стр.2"]["V14"],
                 f["стр.2"]["Y14"], f["стр.2"]["AB14"], f["стр.2"]["AE14"], f["стр.2"]["AH14"],
                 f["стр.2"]["AK14"], f["стр.2"]["AN14"], f["стр.2"]["AQ14"], f["стр.2"]["AT14"],
                 f["стр.2"]["AW14"], f["стр.2"]["AZ14"], f["стр.2"]["BC14"], f["стр.2"]["BF14"])

    for j in range(len(data["Primary"]["Document"][1])):
        dockinfo2[j].value = data["Primary"]["Document"][1][j]

    dockinfo3 = (f["стр.2"]["A16"], f["стр.2"]["D16"], f["стр.2"]["G16"], f["стр.2"]["J16"],
                 f["стр.2"]["M16"], f["стр.2"]["P16"], f["стр.2"]["S16"], f["стр.2"]["V16"],
                 f["стр.2"]["Y16"], f["стр.2"]["AB16"], f["стр.2"]["AE16"], f["стр.2"]["AH16"],
                 f["стр.2"]["AK16"], f["стр.2"]["AN16"], f["стр.2"]["AQ16"], f["стр.2"]["AT16"],
                 f["стр.2"]["AW16"], f["стр.2"]["AZ16"], f["стр.2"]["BC16"], f["стр.2"]["BF16"])

    for j in range(len(data["Primary"]["Document"][2])):
        dockinfo3[j].value = data["Primary"]["Document"][2][j]

    KKTmodel = (f["стр.3_Разд.1"]["BC13"], f["стр.3_Разд.1"]["BF13"], f["стр.3_Разд.1"]["BI13"],
                f["стр.3_Разд.1"]["BL13"], f["стр.3_Разд.1"]["BO13"], f["стр.3_Разд.1"]["BR13"],
                f["стр.3_Разд.1"]["BU13"], f["стр.3_Разд.1"]["BX13"], f["стр.3_Разд.1"]["CA13"],
                f["стр.3_Разд.1"]["CD13"], f["стр.3_Разд.1"]["CG13"], f["стр.3_Разд.1"]["CJ13"],
                f["стр.3_Разд.1"]["CM13"], f["стр.3_Разд.1"]["CP13"], f["стр.3_Разд.1"]["CS13"],
                f["стр.3_Разд.1"]["CV13"], f["стр.3_Разд.1"]["CY13"], f["стр.3_Разд.1"]["DB13"],
                f["стр.3_Разд.1"]["DE13"], f["стр.3_Разд.1"]["DH13"])

    for j in range(len(data["KKTandFN"]["Model"])):
        KKTmodel[j].value = data["KKTandFN"]["Model"][j]

    KKTs = (f["стр.3_Разд.1"]["BC17"], f["стр.3_Разд.1"]["BF17"], f["стр.3_Разд.1"]["BI17"],
            f["стр.3_Разд.1"]["BL17"], f["стр.3_Разд.1"]["BO17"], f["стр.3_Разд.1"]["BR17"],
            f["стр.3_Разд.1"]["BU17"], f["стр.3_Разд.1"]["BX17"], f["стр.3_Разд.1"]["CA17"],
            f["стр.3_Разд.1"]["CD17"], f["стр.3_Разд.1"]["CG17"], f["стр.3_Разд.1"]["CJ17"],
            f["стр.3_Разд.1"]["CM17"], f["стр.3_Разд.1"]["CP17"], f["стр.3_Разд.1"]["CS17"],
            f["стр.3_Разд.1"]["CV17"], f["стр.3_Разд.1"]["CY17"], f["стр.3_Разд.1"]["DB17"],
            f["стр.3_Разд.1"]["DE17"], f["стр.3_Разд.1"]["DH17"])

    for j in range(len(data["KKTandFN"]["SerialKKT"])):
        KKTs[j].value = data["KKTandFN"]["SerialKKT"][j]

    FNname1 = (f["стр.3_Разд.1"]["BC21"], f["стр.3_Разд.1"]["BF21"], f["стр.3_Разд.1"]["BI21"],
               f["стр.3_Разд.1"]["BL21"], f["стр.3_Разд.1"]["BO21"], f["стр.3_Разд.1"]["BR21"],
               f["стр.3_Разд.1"]["BU21"], f["стр.3_Разд.1"]["BX21"], f["стр.3_Разд.1"]["CA21"],
               f["стр.3_Разд.1"]["CD21"], f["стр.3_Разд.1"]["CG21"], f["стр.3_Разд.1"]["CJ21"],
               f["стр.3_Разд.1"]["CM21"], f["стр.3_Разд.1"]["CP21"], f["стр.3_Разд.1"]["CS21"],
               f["стр.3_Разд.1"]["CV21"], f["стр.3_Разд.1"]["CY21"], f["стр.3_Разд.1"]["DB21"],
               f["стр.3_Разд.1"]["DE21"], f["стр.3_Разд.1"]["DH21"])

    for j in range(len(data["KKTandFN"]["FNName"][0])):
        FNname1[j].value = data["KKTandFN"]["FNName"][0][j]

    FNname2 = (f["стр.3_Разд.1"]["BC23"], f["стр.3_Разд.1"]["BF23"], f["стр.3_Разд.1"]["BI23"],
               f["стр.3_Разд.1"]["BL23"], f["стр.3_Разд.1"]["BO23"], f["стр.3_Разд.1"]["BR23"],
               f["стр.3_Разд.1"]["BU23"], f["стр.3_Разд.1"]["BX23"], f["стр.3_Разд.1"]["CA23"],
               f["стр.3_Разд.1"]["CD23"], f["стр.3_Разд.1"]["CG23"], f["стр.3_Разд.1"]["CJ23"],
               f["стр.3_Разд.1"]["CM23"], f["стр.3_Разд.1"]["CP23"], f["стр.3_Разд.1"]["CS23"],
               f["стр.3_Разд.1"]["CV23"], f["стр.3_Разд.1"]["CY23"], f["стр.3_Разд.1"]["DB23"],
               f["стр.3_Разд.1"]["DE23"], f["стр.3_Разд.1"]["DH23"])

    for j in range(len(data["KKTandFN"]["FNName"][1])):
        FNname2[j].value = data["KKTandFN"]["FNName"][1][j]

    FNname3 = (f["стр.3_Разд.1"]["BC25"], f["стр.3_Разд.1"]["BF25"], f["стр.3_Разд.1"]["BI25"],
               f["стр.3_Разд.1"]["BL25"], f["стр.3_Разд.1"]["BO25"], f["стр.3_Разд.1"]["BR25"],
               f["стр.3_Разд.1"]["BU25"], f["стр.3_Разд.1"]["BX25"], f["стр.3_Разд.1"]["CA25"],
               f["стр.3_Разд.1"]["CD25"], f["стр.3_Разд.1"]["CG25"], f["стр.3_Разд.1"]["CJ25"],
               f["стр.3_Разд.1"]["CM25"], f["стр.3_Разд.1"]["CP25"], f["стр.3_Разд.1"]["CS25"],
               f["стр.3_Разд.1"]["CV25"], f["стр.3_Разд.1"]["CY25"], f["стр.3_Разд.1"]["DB25"],
               f["стр.3_Разд.1"]["DE25"], f["стр.3_Разд.1"]["DH25"])

    for j in range(len(data["KKTandFN"]["FNName"][2])):
        FNname3[j].value = data["KKTandFN"]["FNName"][2][j]

    FNname4 = (f["стр.3_Разд.1"]["BC27"], f["стр.3_Разд.1"]["BF27"], f["стр.3_Разд.1"]["BI27"],
               f["стр.3_Разд.1"]["BL27"], f["стр.3_Разд.1"]["BO27"], f["стр.3_Разд.1"]["BR27"],
               f["стр.3_Разд.1"]["BU27"], f["стр.3_Разд.1"]["BX27"], f["стр.3_Разд.1"]["CA27"],
               f["стр.3_Разд.1"]["CD27"], f["стр.3_Разд.1"]["CG27"], f["стр.3_Разд.1"]["CJ27"],
               f["стр.3_Разд.1"]["CM27"], f["стр.3_Разд.1"]["CP27"], f["стр.3_Разд.1"]["CS27"],
               f["стр.3_Разд.1"]["CV27"], f["стр.3_Разд.1"]["CY27"], f["стр.3_Разд.1"]["DB27"],
               f["стр.3_Разд.1"]["DE27"], f["стр.3_Разд.1"]["DH27"])

    for j in range(len(data["KKTandFN"]["FNName"][3])):
        FNname4[j].value = data["KKTandFN"]["FNName"][3][j]

    FNname5 = (f["стр.3_Разд.1"]["BC29"], f["стр.3_Разд.1"]["BF29"], f["стр.3_Разд.1"]["BI29"],
               f["стр.3_Разд.1"]["BL29"], f["стр.3_Разд.1"]["BO29"], f["стр.3_Разд.1"]["BR29"],
               f["стр.3_Разд.1"]["BU29"], f["стр.3_Разд.1"]["BX29"], f["стр.3_Разд.1"]["CA29"],
               f["стр.3_Разд.1"]["CD29"], f["стр.3_Разд.1"]["CG29"], f["стр.3_Разд.1"]["CJ29"],
               f["стр.3_Разд.1"]["CM29"], f["стр.3_Разд.1"]["CP29"], f["стр.3_Разд.1"]["CS29"],
               f["стр.3_Разд.1"]["CV29"], f["стр.3_Разд.1"]["CY29"], f["стр.3_Разд.1"]["DB29"],
               f["стр.3_Разд.1"]["DE29"], f["стр.3_Разд.1"]["DH29"])

    for j in range(len(data["KKTandFN"]["FNName"][4])):
        FNname5[j].value = data["KKTandFN"]["FNName"][4][j]

    FNname6 = (f["стр.3_Разд.1"]["BC31"], f["стр.3_Разд.1"]["BF31"], f["стр.3_Разд.1"]["BI31"],
               f["стр.3_Разд.1"]["BL31"], f["стр.3_Разд.1"]["BO31"], f["стр.3_Разд.1"]["BR31"],
               f["стр.3_Разд.1"]["BU31"], f["стр.3_Разд.1"]["BX31"], f["стр.3_Разд.1"]["CA31"],
               f["стр.3_Разд.1"]["CD31"], f["стр.3_Разд.1"]["CG31"], f["стр.3_Разд.1"]["CJ31"],
               f["стр.3_Разд.1"]["CM31"], f["стр.3_Разд.1"]["CP31"], f["стр.3_Разд.1"]["CS31"],
               f["стр.3_Разд.1"]["CV31"], f["стр.3_Разд.1"]["CY31"], f["стр.3_Разд.1"]["DB31"],
               f["стр.3_Разд.1"]["DE31"], f["стр.3_Разд.1"]["DH31"])

    for j in range(len(data["KKTandFN"]["FNName"][5])):
        FNname6[j].value = data["KKTandFN"]["FNName"][5][j]

    FNs = (f["стр.3_Разд.1"]["BC33"], f["стр.3_Разд.1"]["BF33"], f["стр.3_Разд.1"]["BI33"],
           f["стр.3_Разд.1"]["BL33"], f["стр.3_Разд.1"]["BO33"], f["стр.3_Разд.1"]["BR33"],
           f["стр.3_Разд.1"]["BU33"], f["стр.3_Разд.1"]["BX33"], f["стр.3_Разд.1"]["CA33"],
           f["стр.3_Разд.1"]["CD33"], f["стр.3_Разд.1"]["CG33"], f["стр.3_Разд.1"]["CJ33"],
           f["стр.3_Разд.1"]["CM33"], f["стр.3_Разд.1"]["CP33"], f["стр.3_Разд.1"]["CS33"],
           f["стр.3_Разд.1"]["CV33"], f["стр.3_Разд.1"]["CY33"], f["стр.3_Разд.1"]["DB33"],
           f["стр.3_Разд.1"]["DE33"], f["стр.3_Разд.1"]["DH33"])

    for j in range(len(data["KKTandFN"]["SerialFN"])):
        FNs[j].value = data["KKTandFN"]["SerialFN"][j]

    index = (f["стр.3_Разд.1"]["AE38"], f["стр.3_Разд.1"]["AH38"], f["стр.3_Разд.1"]["AK38"],
             f["стр.3_Разд.1"]["AN38"], f["стр.3_Разд.1"]["AQ38"], f["стр.3_Разд.1"]["AT38"])

    for j in range(len(data["Address"]["index"])):
        index[j].value = data["Address"]["index"][j]

    f["стр.3_Разд.1"]["DK38"].value = data["Address"]["RegionCode"][0]
    f["стр.3_Разд.1"]["DN38"].value = data["Address"]["RegionCode"][1]

    distr = (f["стр.3_Разд.1"]["AE40"], f["стр.3_Разд.1"]["AH40"], f["стр.3_Разд.1"]["AK40"],
             f["стр.3_Разд.1"]["AN40"], f["стр.3_Разд.1"]["AQ40"], f["стр.3_Разд.1"]["AT40"],
             f["стр.3_Разд.1"]["AW40"], f["стр.3_Разд.1"]["AZ40"], f["стр.3_Разд.1"]["BC40"],
             f["стр.3_Разд.1"]["BF40"], f["стр.3_Разд.1"]["BI40"], f["стр.3_Разд.1"]["BL40"],
             f["стр.3_Разд.1"]["BO40"], f["стр.3_Разд.1"]["BR40"], f["стр.3_Разд.1"]["BU40"],
             f["стр.3_Разд.1"]["BX40"], f["стр.3_Разд.1"]["CA40"], f["стр.3_Разд.1"]["CD40"],
             f["стр.3_Разд.1"]["CG40"], f["стр.3_Разд.1"]["CJ40"], f["стр.3_Разд.1"]["CM40"],
             f["стр.3_Разд.1"]["CP40"], f["стр.3_Разд.1"]["CS40"], f["стр.3_Разд.1"]["CV40"],
             f["стр.3_Разд.1"]["CY40"], f["стр.3_Разд.1"]["DB40"], f["стр.3_Разд.1"]["DE40"],
             f["стр.3_Разд.1"]["DH40"], f["стр.3_Разд.1"]["DK40"], f["стр.3_Разд.1"]["DN40"])

    for j in range(len(data["Address"]["District"])):
        distr[j].value = data["Address"]["District"][j]

    city = (f["стр.3_Разд.1"]["AE42"], f["стр.3_Разд.1"]["AH42"], f["стр.3_Разд.1"]["AK42"],
            f["стр.3_Разд.1"]["AN42"], f["стр.3_Разд.1"]["AQ42"], f["стр.3_Разд.1"]["AT42"],
            f["стр.3_Разд.1"]["AW42"], f["стр.3_Разд.1"]["AZ42"], f["стр.3_Разд.1"]["BC42"],
            f["стр.3_Разд.1"]["BF42"], f["стр.3_Разд.1"]["BI42"], f["стр.3_Разд.1"]["BL42"],
            f["стр.3_Разд.1"]["BO42"], f["стр.3_Разд.1"]["BR42"], f["стр.3_Разд.1"]["BU42"],
            f["стр.3_Разд.1"]["BX42"], f["стр.3_Разд.1"]["CA42"], f["стр.3_Разд.1"]["CD42"],
            f["стр.3_Разд.1"]["CG42"], f["стр.3_Разд.1"]["CJ42"], f["стр.3_Разд.1"]["CM42"],
            f["стр.3_Разд.1"]["CP42"], f["стр.3_Разд.1"]["CS42"], f["стр.3_Разд.1"]["CV42"],
            f["стр.3_Разд.1"]["CY42"], f["стр.3_Разд.1"]["DB42"], f["стр.3_Разд.1"]["DE42"],
            f["стр.3_Разд.1"]["DH42"], f["стр.3_Разд.1"]["DK42"], f["стр.3_Разд.1"]["DN42"])

    for j in range(len(data["Address"]["City"])):
        city[j].value = data["Address"]["City"][j]

    vill = (f["стр.3_Разд.1"]["AE44"], f["стр.3_Разд.1"]["AH44"], f["стр.3_Разд.1"]["AK44"],
            f["стр.3_Разд.1"]["AN44"], f["стр.3_Разд.1"]["AQ44"], f["стр.3_Разд.1"]["AT44"],
            f["стр.3_Разд.1"]["AW44"], f["стр.3_Разд.1"]["AZ44"], f["стр.3_Разд.1"]["BC44"],
            f["стр.3_Разд.1"]["BF44"], f["стр.3_Разд.1"]["BI44"], f["стр.3_Разд.1"]["BL44"],
            f["стр.3_Разд.1"]["BO44"], f["стр.3_Разд.1"]["BR44"], f["стр.3_Разд.1"]["BU44"],
            f["стр.3_Разд.1"]["BX44"], f["стр.3_Разд.1"]["CA44"], f["стр.3_Разд.1"]["CD44"],
            f["стр.3_Разд.1"]["CG44"], f["стр.3_Разд.1"]["CJ44"], f["стр.3_Разд.1"]["CM44"],
            f["стр.3_Разд.1"]["CP44"], f["стр.3_Разд.1"]["CS44"], f["стр.3_Разд.1"]["CV44"],
            f["стр.3_Разд.1"]["CY44"], f["стр.3_Разд.1"]["DB44"], f["стр.3_Разд.1"]["DE44"],
            f["стр.3_Разд.1"]["DH44"], f["стр.3_Разд.1"]["DK44"], f["стр.3_Разд.1"]["DN44"])

    for j in range(len(data["Address"]["Village"])):
        vill[j].value = data["Address"]["Village"][j]

    street = (f["стр.4_Разд.1"]["AE9"], f["стр.4_Разд.1"]["AH9"], f["стр.4_Разд.1"]["AK9"],
              f["стр.4_Разд.1"]["AN9"], f["стр.4_Разд.1"]["AQ9"], f["стр.4_Разд.1"]["AT9"],
              f["стр.4_Разд.1"]["AW9"], f["стр.4_Разд.1"]["AZ9"], f["стр.4_Разд.1"]["BC9"],
              f["стр.4_Разд.1"]["BF9"], f["стр.4_Разд.1"]["BI9"], f["стр.4_Разд.1"]["BL9"],
              f["стр.4_Разд.1"]["BO9"], f["стр.4_Разд.1"]["BR9"], f["стр.4_Разд.1"]["BU9"],
              f["стр.4_Разд.1"]["BX9"], f["стр.4_Разд.1"]["CA9"], f["стр.4_Разд.1"]["CD9"],
              f["стр.4_Разд.1"]["CG9"], f["стр.4_Разд.1"]["CJ9"], f["стр.4_Разд.1"]["CM9"],
              f["стр.4_Разд.1"]["CP9"], f["стр.4_Разд.1"]["CS9"], f["стр.4_Разд.1"]["CV9"],
              f["стр.4_Разд.1"]["CY9"], f["стр.4_Разд.1"]["DB9"], f["стр.4_Разд.1"]["DE9"],
              f["стр.4_Разд.1"]["DH9"], f["стр.4_Разд.1"]["DK9"], f["стр.4_Разд.1"]["DN9"])

    for j in range(len(data["Address"]["Street"])):
        street[j].value = data["Address"]["Street"][j]

    house = (f["стр.4_Разд.1"]["AE11"], f["стр.4_Разд.1"]["AH11"], f["стр.4_Разд.1"]["AK11"],
             f["стр.4_Разд.1"]["AN11"], f["стр.4_Разд.1"]["AQ11"], f["стр.4_Разд.1"]["AT11"],
             f["стр.4_Разд.1"]["AW11"], f["стр.4_Разд.1"]["AZ11"])

    for j in range(len(data["Address"]["House"])):
        house[j].value = data["Address"]["House"][j]

    camp = (f["стр.4_Разд.1"]["AE13"], f["стр.4_Разд.1"]["AH13"], f["стр.4_Разд.1"]["AK13"],
            f["стр.4_Разд.1"]["AN13"], f["стр.4_Разд.1"]["AQ13"], f["стр.4_Разд.1"]["AT13"],
            f["стр.4_Разд.1"]["AW13"], f["стр.4_Разд.1"]["AZ13"])

    for j in range(len(data["Address"]["Campus"])):
        camp[j].value = data["Address"]["Campus"][j]

    room = (f["стр.4_Разд.1"]["AE15"], f["стр.4_Разд.1"]["AH15"], f["стр.4_Разд.1"]["AK15"],
            f["стр.4_Разд.1"]["AN15"], f["стр.4_Разд.1"]["AQ15"], f["стр.4_Разд.1"]["AT15"],
            f["стр.4_Разд.1"]["AW15"], f["стр.4_Разд.1"]["AZ15"])

    for j in range(len(data["Address"]["Room"])):
        room[j].value = data["Address"]["Room"][j]

    place1 = (f["стр.4_Разд.1"]["AZ18"], f["стр.4_Разд.1"]["BC18"], f["стр.4_Разд.1"]["BF18"],
              f["стр.4_Разд.1"]["BI18"], f["стр.4_Разд.1"]["BL18"], f["стр.4_Разд.1"]["BO18"],
              f["стр.4_Разд.1"]["BR18"], f["стр.4_Разд.1"]["BU18"], f["стр.4_Разд.1"]["BX18"],
              f["стр.4_Разд.1"]["CA18"], f["стр.4_Разд.1"]["CD18"], f["стр.4_Разд.1"]["CG18"],
              f["стр.4_Разд.1"]["CJ18"], f["стр.4_Разд.1"]["CM18"], f["стр.4_Разд.1"]["CP18"],
              f["стр.4_Разд.1"]["CS18"], f["стр.4_Разд.1"]["CV18"], f["стр.4_Разд.1"]["CY18"],
              f["стр.4_Разд.1"]["DB18"], f["стр.4_Разд.1"]["DE18"])

    for j in range(len(data["Address"]["Place"][0])):
        place1[j].value = data["Address"]["Place"][0][j]

    place2 = (f["стр.4_Разд.1"]["AZ20"], f["стр.4_Разд.1"]["BC20"], f["стр.4_Разд.1"]["BF20"],
              f["стр.4_Разд.1"]["BI20"], f["стр.4_Разд.1"]["BL20"], f["стр.4_Разд.1"]["BO20"],
              f["стр.4_Разд.1"]["BR20"], f["стр.4_Разд.1"]["BU20"], f["стр.4_Разд.1"]["BX20"],
              f["стр.4_Разд.1"]["CA20"], f["стр.4_Разд.1"]["CD20"], f["стр.4_Разд.1"]["CG20"],
              f["стр.4_Разд.1"]["CJ20"], f["стр.4_Разд.1"]["CM20"], f["стр.4_Разд.1"]["CP20"],
              f["стр.4_Разд.1"]["CS20"], f["стр.4_Разд.1"]["CV20"], f["стр.4_Разд.1"]["CY20"],
              f["стр.4_Разд.1"]["DB20"], f["стр.4_Разд.1"]["DE20"])

    for j in range(len(data["Address"]["Place"][1])):
        place2[j].value = data["Address"]["Place"][1][j]

    place3 = (f["стр.4_Разд.1"]["AZ22"], f["стр.4_Разд.1"]["BC22"], f["стр.4_Разд.1"]["BF22"],
              f["стр.4_Разд.1"]["BI22"], f["стр.4_Разд.1"]["BL22"], f["стр.4_Разд.1"]["BO22"],
              f["стр.4_Разд.1"]["BR22"], f["стр.4_Разд.1"]["BU22"], f["стр.4_Разд.1"]["BX22"],
              f["стр.4_Разд.1"]["CA22"], f["стр.4_Разд.1"]["CD22"], f["стр.4_Разд.1"]["CG22"],
              f["стр.4_Разд.1"]["CJ22"], f["стр.4_Разд.1"]["CM22"], f["стр.4_Разд.1"]["CP22"],
              f["стр.4_Разд.1"]["CS22"], f["стр.4_Разд.1"]["CV22"], f["стр.4_Разд.1"]["CY22"],
              f["стр.4_Разд.1"]["DB22"], f["стр.4_Разд.1"]["DE22"])

    for j in range(len(data["Address"]["Place"][2])):
        place3[j].value = data["Address"]["Place"][2][j]

    Using = (f["стр.4_Разд.1"]["AZ27"], f["стр.5_Разд.2"]["BF11"], f["стр.5_Разд.2"]["BF18"],
             f["стр.5_Разд.2"]["BF23"], f["стр.5_Разд.2"]["BF29"], f["стр.5_Разд.2"]["BF33"],
             f["стр.5_Разд.2"]["BF37"], f["стр.5_Разд.2"]["BF42"], f["стр.6_Разд.2"]["BF10"],
             f["стр.6_Разд.2"]["BF15"], f["стр.6_Разд.2"]["BF19"], f["стр.6_Разд.2"]["BF24"])

    for j in range(len(data["OFD"]["Using"])):
        Using[j].value = "1" if data["OFD"]["Using"][j] else "2"

    OFDName1 = (f["стр.9_Разд.3"]["BC12"], f["стр.9_Разд.3"]["BF12"], f["стр.9_Разд.3"]["BI12"],
                f["стр.9_Разд.3"]["BL12"], f["стр.9_Разд.3"]["BO12"], f["стр.9_Разд.3"]["BR12"],
                f["стр.9_Разд.3"]["BU12"], f["стр.9_Разд.3"]["BX12"], f["стр.9_Разд.3"]["CA12"],
                f["стр.9_Разд.3"]["CD12"], f["стр.9_Разд.3"]["CG12"], f["стр.9_Разд.3"]["CJ12"],
                f["стр.9_Разд.3"]["CM12"], f["стр.9_Разд.3"]["CP12"], f["стр.9_Разд.3"]["CS12"],
                f["стр.9_Разд.3"]["CV12"], f["стр.9_Разд.3"]["CY12"], f["стр.9_Разд.3"]["DB12"],
                f["стр.9_Разд.3"]["DE12"], f["стр.9_Разд.3"]["DH12"])

    for j in range(len(data["OFD"]["OFDName"][0])):
        OFDName1[j].value = data["OFD"]["OFDName"][0][j]

    OFDName2 = (f["стр.9_Разд.3"]["BC14"], f["стр.9_Разд.3"]["BF14"], f["стр.9_Разд.3"]["BI14"],
                f["стр.9_Разд.3"]["BL14"], f["стр.9_Разд.3"]["BO14"], f["стр.9_Разд.3"]["BR14"],
                f["стр.9_Разд.3"]["BU14"], f["стр.9_Разд.3"]["BX14"], f["стр.9_Разд.3"]["CA14"],
                f["стр.9_Разд.3"]["CD14"], f["стр.9_Разд.3"]["CG14"], f["стр.9_Разд.3"]["CJ14"],
                f["стр.9_Разд.3"]["CM14"], f["стр.9_Разд.3"]["CP14"], f["стр.9_Разд.3"]["CS14"],
                f["стр.9_Разд.3"]["CV14"], f["стр.9_Разд.3"]["CY14"], f["стр.9_Разд.3"]["DB14"],
                f["стр.9_Разд.3"]["DE14"], f["стр.9_Разд.3"]["DH14"])

    for j in range(len(data["OFD"]["OFDName"][1])):
        OFDName2[j].value = data["OFD"]["OFDName"][1][j]

    OFDName3 = (f["стр.9_Разд.3"]["BC16"], f["стр.9_Разд.3"]["BF16"], f["стр.9_Разд.3"]["BI16"],
                f["стр.9_Разд.3"]["BL16"], f["стр.9_Разд.3"]["BO16"], f["стр.9_Разд.3"]["BR16"],
                f["стр.9_Разд.3"]["BU16"], f["стр.9_Разд.3"]["BX16"], f["стр.9_Разд.3"]["CA16"],
                f["стр.9_Разд.3"]["CD16"], f["стр.9_Разд.3"]["CG16"], f["стр.9_Разд.3"]["CJ16"],
                f["стр.9_Разд.3"]["CM16"], f["стр.9_Разд.3"]["CP16"], f["стр.9_Разд.3"]["CS16"],
                f["стр.9_Разд.3"]["CV16"], f["стр.9_Разд.3"]["CY16"], f["стр.9_Разд.3"]["DB16"],
                f["стр.9_Разд.3"]["DE16"], f["стр.9_Разд.3"]["DH16"])

    for j in range(len(data["OFD"]["OFDName"][2])):
        OFDName3[j].value = data["OFD"]["OFDName"][2][j]

    OFDName4 = (f["стр.9_Разд.3"]["BC18"], f["стр.9_Разд.3"]["BF18"], f["стр.9_Разд.3"]["BI18"],
                f["стр.9_Разд.3"]["BL18"], f["стр.9_Разд.3"]["BO18"], f["стр.9_Разд.3"]["BR18"],
                f["стр.9_Разд.3"]["BU18"], f["стр.9_Разд.3"]["BX18"], f["стр.9_Разд.3"]["CA18"],
                f["стр.9_Разд.3"]["CD18"], f["стр.9_Разд.3"]["CG18"], f["стр.9_Разд.3"]["CJ18"],
                f["стр.9_Разд.3"]["CM18"], f["стр.9_Разд.3"]["CP18"], f["стр.9_Разд.3"]["CS18"],
                f["стр.9_Разд.3"]["CV18"], f["стр.9_Разд.3"]["CY18"], f["стр.9_Разд.3"]["DB18"],
                f["стр.9_Разд.3"]["DE18"], f["стр.9_Разд.3"]["DH18"])

    for j in range(len(data["OFD"]["OFDName"][3])):
        OFDName4[j].value = data["OFD"]["OFDName"][3][j]

    OFDInn = (f["стр.9_Разд.3"]["BC21"], f["стр.9_Разд.3"]["BF21"], f["стр.9_Разд.3"]["BI21"],
              f["стр.9_Разд.3"]["BL21"], f["стр.9_Разд.3"]["BO21"], f["стр.9_Разд.3"]["BR21"],
              f["стр.9_Разд.3"]["BU21"], f["стр.9_Разд.3"]["BX21"], f["стр.9_Разд.3"]["CA21"],
              f["стр.9_Разд.3"]["CD21"], f["стр.9_Разд.3"]["CG21"], f["стр.9_Разд.3"]["CJ21"])

    for j in range(len(data["OFD"]["OFDInn"])):
        OFDInn[j].value = data["OFD"]["OFDInn"][j]

    f.save("3.xlsx")


if __name__ == "__main__":
    print(FormatDate("04 Ноября 2022"))