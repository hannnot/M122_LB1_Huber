from line4 import Line4


def __totalPriceXml(lines) :
    totalPrice = 0.00
    for line in lines :
        if line[0] == 'RechnPos' : 
            price = Line4(line)
            totalPrice = totalPrice + float(price.totalPrice)
    total = '%.2f' %totalPrice
    price = ''.join(total.split('.'))
    return price.zfill(10)