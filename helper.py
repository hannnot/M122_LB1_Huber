from line4 import Line4


def totalPriceXml(lines) :
    totalPrice = 0.00
    for line in lines :
        if line[0] == 'RechnPos' : 
            price = Line4(line)
            totalPrice = totalPrice + float(price.totalPrice)
    total = '%.2f' %totalPrice
    price = ''.join(total.split('.'))
    return price.zfill(10)

def totalPriceTxt(lines) :
    totalPrice = 0.00
    for line in lines :
        if line[0] == 'RechnPos' :
            price = Line4(line)
            totalPrice = totalPrice + float(price.totalPrice)
    return '%.2f' % totalPrice

def totalPriceTxtWthSpc(lines) :
    totalPrice = 0.00
    for line in lines :
        if line[0] == 'RechnPos' :
            pricing = Line4(line)
            totalPrice = totalPrice + float(pricing.price)
    price =str('%.2f' % totalPrice)
    p = price.split('.')
    return p[0] + ' . ' + p[1]