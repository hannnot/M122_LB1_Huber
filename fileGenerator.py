from line1 import Line1
from line2 import Line2
from line3 import Line3

class FileGenerator() :
    def __init__(self, lines) -> None :
        self.__lines = lines
        self.__xmlFile = self.__openXmlFile()

    def __openXmlFile(self) :
        with open('invoice.xml', encoding='uft-8') as file :
            string = file.read()
            file.close()
        return string

    def __genInvoiceXml(self) :
        l1 = Line1(self.__lines[0])
        l2 = Line2(self.__lines[1])
        l3 = Line3(self.__lines[2])
        fileName = l2.customerID + '_' + l1.invoiceNr + '_invoice.xml'
        xmlFile = self.__xmlFile % ( l1. )
