from smartphone import Smartphone
catalog = [
Smartphone("apple","16","+79078888888"),
Smartphone("realme", "17", "+79032222222"),
Smartphone("samsung", "18", "+79053333333"),
Smartphone("xiaomi", "19", "+79065555555"),
Smartphone("alcatel", "20", "+79264444444")]
for smartphone in catalog:
    print(f"{smartphone.brand} - {smartphone.model} - {smartphone.number}")