from line4 import Line4
from helper import totalPriceXml, totalPriceTxt, totalPriceTxtWthSpc
from line1 import Line1
from line2 import Line2
from line3 import Line3

class FileGenerator() :
    def __init__(self, lines) -> None :
        self.__lines = lines
        self.__xmlFile = self.__openXmlFile()
        self.xml = self.__genXmlFile()
        self.txt = self.__genTxtFile()

    def __openXmlFile(self) :
        with open('invoice.xml', encoding='uft-8') as file :
            string = file.read()
            file.close()
        return string

    def __genXmlFile(self) :
        l1 = Line1(self.__lines[0])
        l2 = Line2(self.__lines[1])
        l3 = Line3(self.__lines[2])
        fileName = l2.customerID + '_' + l1.invoiceNr + '_invoice.xml'
        xmlFile = self.__xmlFile % ( 
            l2.partyID, 
            l3.customerID,
            l1.dateTimeStamp,
            l1.dateStamp,
            l1.dateStamp,
            l1.invoiceNr,
            l1.dateStamp,
            l1.orderNr,
            l1.dateStamp,
            l1.dateStamp,
            l2.customerID,
            l2.partyID,
            l2.name,
            l2.address,
            l2.zip,
            l3.customerID,
            l3.name,
            l3.address,
            l3.zip,
            totalPriceXml(self.__lines),
            l1.daysTillPay,
            l1.dueDateStamp
        )
        try:
            with open(fileName, 'w', encoding='utf-8') as file:
                file.write(xmlFile)
                file.close()
            print('XML file has been created!')
        except:
            print('XML file has failed.')

    def __genTxtFile(self) :
        l1 = Line1(self.__lines[0])
        l2 = Line2(self.__lines[1])
        l3 = Line3(self.__lines[2])
        fileName = l2.customerID + '_' + l1.invoiceNr + '_invoice.txt'
        listOfItems = []
        for line in self.__lines :
            if line[0] == 'RechnPos' :
                listOfItems.append(line)

        source = l1.city + ', den ' + l1.date
        txt = [''] * 65
        txt[4] = l2.name
        txt[5] = l2.address
        txt[6] = l2.zip
        txt[8] = l2.customerID
        txt[13] = '{:<48s}{:<}'.format(source, l3.name)
        txt[14] = '{:<48s}{:<}'.format('', l3.address)
        txt[15] = '{:<48s}{:<}'.format('', l3.zip)
        txt[17] = '{:<16s}{:>8}'.format('Kundennummer:', l2.customerID)
        txt[18] = '{:<16s}{:>8}'.format('Auftragsnummer:', l1.orderNr)
        txt[20] = '{:<16s}{:>8}'.format('Rechnung Nr:', l1.invoiceNr)
        txt[21] = '------------------------'
        for item in listOfItems:
            i = Line4(item)
            txt[21 + int(i.positionNr)] = '{:4s}{:<4s}{:<44s}{:<4s}{:>11s}{:<5s}{:>11s}{:>7}'.format(
                '', i.positionNr, i.itemDescription, i.quantity, i.pricePerItem, '  CHF', i.price, i.mwst)
        txt[22 + len(listOfItems)] = '{:>83}'.format('-----------')
        txt[23 + len(listOfItems)] = '{:>68}{:>15}'.format(
            'Total CHF', totalPriceTxt(self.__lines))
        txt[25 + len(listOfItems)] = '{:>68}{:>15}'.format('Mwst  CHF', '0.00')
        txt[44] = 'Zahlungsziel ohne Abzug {} Tage ({})'.format(
            l1.payWaitTime, l1.payDueDate)
        txt[46] = 'Einzahlungsschein'
        txt[58] = '{:>13s}{:>29s}{:<5s}{:<}'.format(totalPriceTxtWthSpc(
            self.__lines), totalPriceTxtWthSpc(self.__lines), '', l3.name)
        txt[59] = '{:<47}{}'.format('', l3.address)
        txt[60] = '{:<47}{}'.format('0 00000 00000 00000', l3.zip)
        txt[62] = l3.name
        txt[63] = l3.address
        txt[64] = l3.zip
        try:
            with open(fileName, 'w', encoding='utf-8') as file:
                file.write(txt)
                file.close()
            print('TXT file has been created!')
        except:
            print('TXT file has failed.')

