import sys
import re
from datetime import datetime, timedelta

class Line1:
    def __init__(self, line) -> None:
        if 'Rechnung_' not in line[0]:
            sys.exit()
        else :
            self.__line = line
            self.__getValue()

    def __getValue(self) :
        self.invoiceNr = self.__invoiceNr()
        self.orderNr = self.__orderNr()
        self.city = self.__city()
        self.date = self.__date()
        self.time = self.__time()
        self.daysTillPay = self.__daysTillPay()
        self.calculateDueDate = self.__calculateDueDate()

    def __invoiceNr(self) :
        if not re.match('Rechnung_\d{5}', self.__line[0]) :
            print('error! orderNr has incorrect format')
        return self.__line[0].split('_')[1]

    def __orderNr (self) :
        if not re.match('Auftrag_A\d{3}', self.__line[1]) :
            print('error! orderNr has incorrect format')
        return self.__line[1]

    def __city (self) :
        if len(self.__line[2]) < 1 :
            print('error! No city provided')
        return self.__line[2]

    def __date (self) :
        if not re.match('\d{2}\.\d{2}\.\d{4}', self.__line[3]) :
            print('error! Date has incorrect format')
        return self.__line[3]

    def __time (self) :
        if not re.match('\d{2}\:\d{2}\:\d{2}', self.__line[4]) :
            print('error! wrong time format!')
        return self.__line[4]

    def __daysTillPay (self) :
        if not re.match('ZahlungszielInTagen_\d{2}', self.__line[5]) :
            print('error! Days until Pay is incorrect format!')
        return self.__line[5]

    def __calculateDueDate (self) :
        date = datetime.strptime(self.__date(), '%d.%m.%Y') + timedelta(days=int(self.__daysTillPay()))
        return date.strftime('%d.%m.%Y')