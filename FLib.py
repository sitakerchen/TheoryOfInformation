import numpy as np
import math as mth
import fractions as fc

probability = {}  # 概率库!!!!


def print_b(result):  # output format
    """
    format:print('%.5f bit' % result)
    """
    print('ans = %.5f bit' % result)


def cn_(variable, subscript):
    """
    [trans]: 修饰
    [formula]: x or y -> xi or xj or yi or yj
    :param variable: x or y or z ... (str)
    :param subscript: 1 or 2 or i or j... (integer)
    :return: xi or yj or ...(str)
    """
    return variable + str(subscript)
# def cn_x(i):
#     """
#     function:修饰,i -> xi
#     :return: (str)
#     """
#     return 'x' + str(i)


# def cn_y(j):
#     """
#     function:修饰,j -> yj
#     :return: (str)
#     """
#     return 'y' + str(j)


def add_pro(num):
    """
    [warning]:if you input such as x1y1, y1x1 will automatically added
    [name]:直接输入变量,不需要引号" "or' '
    [value]:integer / integer (eg:3/4)
    :return: (None)
    """
    for i in range(num):
        name = input('please input name:')
        value = input('please input value(fraction):')
        probability[name] = fc.Fraction(value)
        if 'x' and 'y' in name and '|' not in name:
            probability[name[2:] + name[:2]] = fc.Fraction(value)
        print('%s:%s successful added!' % (name, value))


def add_pro_auto(List):
    """
    [warning]:if you input such as x1y1, y1x1 will automatically added
    [input_type]:str
    [format]: name1,value1;name2,value2 ...
    [value]: integer / integer (eg:3/4)
    :return: (None)
    """
    a = str(List)
    b = a.split(';')
    c, d = [], []
    for term in b:
        t1, t2 = term.split(',')
        probability[t1] = fc.Fraction(t2)
        if 'x' and 'y' in t1 and '|' not in t1:
            probability[t1[2:] + t1[:2]] = fc.Fraction(t2)
        print('%s:%s successful added!' % (t1, t2))
    # for name,value in nameList,valueList:
    #     probability[name] = fc.Fraction(value)


def show_allMyPro():
    for item, value in probability.items():
        print(item + ':' + str(value))


def clear_allMyPro():
    """
    [warning]: 此操作无法还原,请谨慎操作
    :return: None
    """
    probability.clear()


def p(xOry, compute_enable=1):
    """
    [warning]:小写p,如果目标不存在,将尝试通过公式计算,若再次失败,将raise KeyError
    [format]: xiyj or xi|yj or yj|xi or xi or yj
    :return: a probability value (fc.Fraction)
    """
    if not compute_enable:
        try:
            return probability[xOry]
        except KeyError:
            raise KeyError
    else:
        try:
            return probability[xOry]
        except KeyError:
            try:
                print('aim p(%s) not exist!' % (xOry))
                t = fc.Fraction
                if 'x' and 'y' in xOry:
                    if '|' in xOry:  # xi|yj 01 2 34
                        try:
                            t = _P_condition(xOry[0:2], xOry[3:])
                        except KeyError:
                            pass
                        else:
                            add_pro_auto(xOry + ',' + str(t))
                            print('Automatically add %s:%s to database' % (xOry, t))
                    else:
                        try:
                            t = _P_joint(xOry[0:2], xOry[2:])
                        except KeyError:
                            pass
                        else:
                            add_pro_auto(xOry + ',' + str(t))
                            print('Automatically add %s:%s to database' % (xOry, t))
                else:
                    raise KeyError
            except KeyError:
                print("no such variable in database, please add in!")
                # print('%s do not exist!' % (xOry))
                # raise KeyError
            else:
                return t


# 大写P
def _P_joint(x, y):
    """
    [trans]: 联合概率
    [warning]: please use "p()" function instead of this
    [input_type]: str
    [formula]: P(xy) = P(x)P(y|x) = P(y)P(x|y)
    :return: a probability value compute by formula above(fc.Fraction)
    """
    # try:
    #     return p(x+y)
    # except KeyError:
    try:
        return p(x, compute_enable=0) * p(y + '|' + x, compute_enable=0)
    except KeyError:
        try:
            return p(y, compute_enable=0) * p(x + '|' + y, compute_enable=0)
        except KeyError:
            print("no such variable in database, please add in!")
            raise KeyError


def _P_condition(x, y):
    """
    [trans]:条件概率
    [warning]: please use "p()" function instead of this
    [input_type]:str (x,y are exchangeable)
    [formula]:p(x|y) = p(xy)/p(y), p(y|x) = p(xy)/p(x)
    :return: a probability value compute by formula above(fc.Fraction)
    """
    try:
        return p(x + y, compute_enable=0) / p(y, compute_enable=0)
    except KeyError:
        print('no such variable in database, please add in!')
        raise KeyError


def I_sef(x):
    """
    [trans]:自信息
    [formula]:I(xi)=-log2(p(xi))
    :param x:xi or yi (str)
    :return: a value compute by formula above (float)
    """
    return -np.log2(float(p(x)))


def I_mutual(pvi, rce):
    """
    [trans] :互信息
    [formula]:I(xi;yj) = I(xi) - I(xi|yj) = I(yi) - I(yi|xi) = p(pvi+rce)/p(pvi)*p(rce)
    :param pvi: x or y (str)
    :param rce: x or y (str)
    :return: a value compute by formula above (float)
    """
    try:
        return I_sef(pvi) - I_sef(pvi + '|' + rce)
    except KeyError:
        try:
            return I_sef(rce) - I_sef(rce + '|' + pvi)
        except KeyError:
            try:
                return np.log2(float(p(pvi + rce) / p(pvi) * p(rce)))
            except KeyError:
                print('no such variable in database, please add in!')
                raise KeyError


def I_sef_combine(xAndy):
    """
    [trans]: 联合自信息
    [formula]: I(xi yj) = -log2(p(xi yj))
    :param xAndy: xiyi (str)
    :return: a value compute by formula above (float)
    """
    return -np.log2(float(p(xAndy)))


def I_sef_condition(xCy):
    """
    [tarns]: 条件自信息
    [formula]: I(xi|yj) = -log2(p(xi|yj))
    :param xCy: xi|yj (str)
    :return: a value compute by formula above (float)
    """
    return -np.log2(float(p(xCy)))


def _I_mutual_condition(x, y ,z):
    """
    [trans]: 条件互信息
    [formula]: I(xi;yj|zk) = log2(p(xi|yjzk)/p(xi|zk))
    [warning]: 不确定能不能正常 work 因为涉及到三个变量
    :param x: xi(str)
    :param y: yj(str)
    :param z: zk(str)
    :return: a value compute by formula above (float)
    """
    return None #不会




def H_sel(x, term):
    """
    [trans]: 平均自信息(信源熵)
    :param x: x (str)
    :param term: 下标的最大值,即项数(integer)
    :return: (float)
    """
    ans = 0.0
    for i in range(1, term+1):
        ans = ans + p(cn_(x, i)) * I_sef(cn_(x, i))
    return ans


def H_mutual(x, y, term):
    """
    [trans]: 平均互信息(互信息熵)
    :param x: x (str)
    :param y: y (str)
    :param term: 下标的最大值,即项数(integer)
    :return: (float)
    """
    total = 0.0
    for i in range(1, term + 1):
        for j in range(1, term + 1):
            total += p(cn_(x, i)+cn_(y, j)) * I_mutual(cn_(x, i), cn_(y, j))
    return total


def _get_xy_From_P_cond(n):
    """
    [trans]: 由条件概率批量得到联合概率.p(x|y),p(y) -> p(xy)
    [warning]: 由于函数库更新,此函数的功能可由 p()函数自动实现,一般不要用
    :param n: max number of subscript
    :return: None (the ans will automatically add in database by the function "add_pro_auto")
    """
    #     n = input('please input max subscript')
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            name = 'x' + str(i) + 'y' + str(j)
            value = p(name)
            add_pro_auto(name+','+value)
            print('P(%s):%s' % (name, str(value)))


def _get_P_condxy_From_xy(n):  # P(xy),P(y) -> P(x|y)
    """
    [trans]: 由联合概率批量得到条件概率.p(xy),p(y) -> p(x|y)
    [warning]: 由于函数库更新,此函数的功能可由 p()函数自动实现,一般不要用
    :param n: max number of subscript
    :return: None (the ans will automatically add in database by the function "add_pro_auto")
    """
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            x, y = 'x' + str(i), 'y' + str(j)
            name = 'x' + str(i) + '|' + 'y' + str(j)
            value = p(x+'|'+y)
            add_pro_auto(name + ',' + str(value))
            print('P(%s):%s' % (name, str(value)))


def H_equivocation(fir, sec, n):
    """
    [trans]: 疑义度
    [formula]: H(Y|X) = p(xi yj)*I(xi|yj) + ...
    :param fir: variable 1 such as 'x' (str)
    :param sec: variable 2 such as 'y' (str)
    :param n: max number of subscript (integer)
    :return: (float)
    """
    ans = 0.0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            x = cn_(fir, i)
            y = cn_(sec, j)
            ans += p(x + y) * I_sef_condition(x + '|' + y)
    return ans


def H_Noise(fir, sec, n):
    """
    [trans]: 噪声熵
    [formula]: H(Y|X) = p(xi yj)*I(yj|xi) + ...
    :param fir: variable 1 such as 'x' (str)
    :param sec: variable 2 such as 'y' (str)
    :param n: number of the max subscript (integer)
    :return: (float)
    """
    ans = 0.0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            x = cn_(fir, i)
            y = cn_(sec, j)
            ans += p(x + y) * I_sef_condition(y+'|'+x)
    return ans


def H_combination(fir, sec, n):  # 联合熵
    """
    [trans]: 联合熵
    [formula]: H(XY) = p(xi yj) * I(xi yj) + ...
    :param fir: variable 1 such as 'x' (str)
    :param sec: variable 2 such as 'y' (str)
    :param n: number of the max subscript (integer)
    :return: (float)
    """
    ans = 0.0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            x = cn_(fir, i)
            y = cn_(sec, j)
            ans += p(x + y) * I_sef_combine(x + y)
    return ans


def Trans_real2binary(num, l):
    """
    :param num: 源小数 (float)
    :param l: 精度 (int)
    :return: 目标二进制小数 (str)
    """
    s = ''
    remain = num
    for i in range(l):
        remain = remain*2
        if remain >= 1:
            s = s + '1'
            remain = remain - 1
        else:
            s = s + '0'
    return s

