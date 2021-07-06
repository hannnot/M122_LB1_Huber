import sys
import re

class Line2:
    def __init__(self, line) -> None:
        if 'Herkunft' not in line[0]:
            sys.exit() #TODO after errors
        else :
            self.__line = line
            self.__getValue()

    def __getValue(self) :
        self.partyID = self.__partyID()
        self.customerID = self.__customerID()
        self.name = self.__name()
        self.address = self.__address()
        self.zip = self.__zip()
        self.taxID = self.__taxID()
        self.email = self.__email()




    def __partyID (self) :
        if not re.match(r'\d{17}', self.__line[1]) :
            print('error! party ID has incorrect format')
        return self.__line[1]

    def __customerID (self) :
        if not re.match(r'K\d{3}', self.__line[2]) :
            print('error! customer ID incorrect')
        return self.__line[2]

    def __name (self) :
        if len(self.__line[3]) < 1 :
            print('error! No name provided')
        return self.__line[3]

    def __address (self) :
        if len(self.__line[4]) < 1 :
            print('error! No address provided')
        return self.__line[4]

    def __zip (self) :
        if not re.match(r'\d{4}', self.__line[5]) :
            print('error! Zip is not 4 digits!')
        return self.__line[5]

    def __taxID (self) :
        if not re.match(r'CHE-\d{3}\.\d{3}\.\d{3}\ MWST', self.__line[6]) :
            print('error! MWST is incorrect!')
        return self.__line[6]

    def __email (self) :
        if len(self.__line[7]) < 1 :
            print('error! No email provided')
        return self.__line[7]