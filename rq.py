import requests as rq
from dadata import Dadata


def EgrulRq(inn):
    """
    Запрос к ЕГРЮЛ для получения данных контрагента
    """
    info = []
    if len(inn) == 0:
        return
    url = 'https://egrul.nalog.ru'
    url1 = 'https://egrul.nalog.ru/search-result/'

    r = rq.post(url, data={"query": inn})
    if r:
        r1 = rq.get(url1 + r.json()["t"])
        if r1 and len(r1.json()["rows"]) > 0:
            res = r1.json()["rows"][0]
            # вид лица
            if res["k"] == "sprav-fl":
                return False
            info.append(res["k"])
            # полное наименование/ФИО
            info.append(res["n"])
            # ОГРН
            info.append(res["o"])
            if res["k"] == "ul":
                # КПП
                info.append(res["p"])

    return info if len(info) > 0 else False


def GetIndex(text):
    dadata = Dadata("211c3a81d71b207a60d6b8c287b59b9617b010bd", "8f549bc58baf074ebbfa28a0deac1b90158d8cb4")

    res = dadata.suggest("postal_unit", f"{text}")

    return res[0]["value"] if len(res) > 0 else False


if __name__ == "__main__":
    print(GetIndex("Г.ИРБИТ"))
