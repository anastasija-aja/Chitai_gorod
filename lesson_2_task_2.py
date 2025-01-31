is_year_leap=input("Введите год:")
is_year_leap=int(is_year_leap)
if (is_year_leap % 4==0):
    print("год",is_year_leap,":",True)
if (is_year_leap % 4==1):
    print("год", is_year_leap, ":", False)
if (is_year_leap % 4 == 2):
    print("год", is_year_leap, ":", False)
if (is_year_leap % 4 == 3):
    print("год", is_year_leap, ":", False)