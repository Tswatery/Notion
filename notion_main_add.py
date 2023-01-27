from discrete_add import Discrete_Add


def Main_Add():
    _ = int(input('选择1是制定连续完整，2是制定自定义课表：'))
    if _ == 2:
        Discrete_Add()