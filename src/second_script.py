#!/usr/bin/python3
# -*- coding: utf-8 -*-

from funcs import *
from second_form import *
from PyQt5.QtWidgets import QDialog


class SecondWindow(QDialog, Ui_SecondWindow):
    # TODO: Constructor
    def __init__(self, ownsSC, ownsFR, ownsIT, ownsATS, lines, parent=None):
        QDialog.__init__(self, parent)
        Ui_SecondWindow.__init__(self)
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self)
        #
        self.funcs = Functions()
        self.lines = lines
        self.ownsSC = ownsSC
        self.ownsFR = ownsFR
        self.ownsIT = ownsIT
        self.ownsATS = ownsATS
        #
        self.dealersets2 = ["aberdeen", "amsterdam", "berlin", "bern", "birmingham", "bratislava", "bremen", "brussel",
                            "budapest", "calais", "cardiff", "dortmund", "dortmund", "dresden", "dusseldorf", "edinburgh",
                            "felixstowe", "frankfurt", "gdansk", "glasgow", "graz", "grimsby", "hamburg", "hannover", "krakow",
                            "leipzig", "lille", "london", "luxembourg", "manchester", "munchen", "newcastle", "nurnberg",
                            "osnabruck", "plymouth", "prague", "rostock", "rotterdam", "salzburg", "strasbourg", "stuttgart",
                            "szczecin", "szeged", "warszawa", "wien", "wroclaw", "zurich"]  # Default dealers
        self.dealersets2_sc = ["bergen", "goteborg", "kalmar", "kobenhavn", "linkoping", "oslo", "stockholm"]  # SC dealers
        self.dealersets2_fr = ["bordeaux", "bourges", "brest", "geneve", "lemans", "limoges", "lyon", "marseille", "nantes",
                               "paris", "toulouse"]  # FR dealers
        self.dealersets2_it = ["bologna", "catania", "firenze", "milano", "napoli", "palermo", "roma", "taranto", "torino",
                               "verona"]  # IT dealers
        #
        self.agenciesets2 = ["aberdeen", "berlin", "bialystok", "birmingham", "bremen", "brno",
                             "brussel", "budapest", "calais", "debrecen", "dortmund", "dover", "dresden", "edinburgh",
                             "frankfurt", "gdansk", "glasgow", "graz", "grohningen", "hamburg", "hannover", "innsbruck", "kassel",
                             "klagenfurt", "koln", "kosice", "krakow", "leipzig", "liege", "linz", "liverpool", "lodz", "london",
                             "luxembourg", "manchester", "mannheim", "munchen", "newcastle", "nurnberg", "ostrava", "pecs",
                             "plymouth", "poznan", "prague", "sheffield", "southampton", "stuttgart", "swansea", "szczecin",
                             "szeged", "warszava", "wien", "zurich"]  # Default agnecies
        self.agenciesets2_sc = ["aalborg", "bergen", "helsingborg", "kobenhavn", "malmo", "odense", "oslo", "stavanger",
                                "stockholm"]  # SC agencies
        self.agenciesets2_fr = ["bordeaux", "clermont", "geneve", "larochelle", "lyon", "marseille", "metz", "paris", "reims",
                                "rennes", "toulouse"]  # FR agencies
        self.agenciesets2_it = ["bologna", "catania", "milano", "napoli", "pescara", "roma", "taranto", "venezia"]  # IT agencies
        #
        self.dealersats = ["elko", "reno", "bakersfield", "phoenix", "flagstaff", "los_angeles", "albuquerque", "hobbs"]
        self.agenciesats = ["redding", "san_rafael", "stockton", "fresno", "santa_cruz", "bakersfield", "oxnard",
                            "los_angeles", "san_diego", "carson_city", "las_vegas", "phoenix", "tucson", "sierra_vista",
                            "farmington", "santa_fe", "roswell", "carlsbad_nm"]
        #
        self.ui.garages_analyze.clicked.connect(self.checkGarages)
        self.ui.garage_add.clicked.connect(self.addGarage)
        self.ui.garage_unlock_all.clicked.connect(self.addAllGarages)
        self.ui.headquarter_change.clicked.connect(self.changeHQ)
        self.ui.cities_analyze.clicked.connect(self.checkCities)
        self.ui.city_add.clicked.connect(self.addCity)
        self.ui.city_unlock_all.clicked.connect(self.addAllCities)
        self.ui.dealerships_analyze.clicked.connect(self.checkDealers)
        self.ui.dealership_add.clicked.connect(self.addDealership)
        self.ui.dealership_unlock_all.clicked.connect(self.addAllDealership)
        self.ui.agencies_analyze.clicked.connect(self.checkAgencies)
        self.ui.agency_add.clicked.connect(self.addAgency)
        self.ui.agency_unlock_all.clicked.connect(self.addAllAgency)

    # TODO: Default functions
    def purchasedgarages(self):
        purchased_garages = []
        i = 0
        try:
            while True:
                while "garage : " not in self.lines[i]:
                    i += 1
                city = match(r"garage : garage.(.+) {$", self.lines[i]).group(1)
                while "status:" not in self.lines[i]:
                    i += 1
                if "0" not in self.lines[i]:
                    purchased_garages.append(city)
        except:
            pass
        return purchased_garages

    def cities(self):
        cities = []
        line = self.funcs.searchline(self.lines, "companies\[")
        while "companies[" in self.lines[line]:
            city = match(r" companies\[[0-9]+\]: company.volatile.[a-z0-9_]+[.]([a-z_]+)", self.lines[line]).group(1)
            if city not in cities:
                cities.append(city)
            line += 1
        return cities

    # TODO: Program functions
    def checkGarages(self):
        self.ui.garages_text.clear()
        for e in self.purchasedgarages():
            self.ui.garages_text.append(e)
        hq = self.funcs.getvalue(self.lines, self.funcs.searchline(self.lines, "hq_city:"))
        self.ui.headquarter_lineedit.setText(hq)

    def checkCities(self):
        self.ui.cities_text.clear()
        for i in self.funcs.getarrayitems(self.lines,
                                          self.funcs.searchline(self.lines, "visited_cities:")):
            self.ui.cities_text.append(i)
        if not self.funcs.getarrayitems(self.lines,
                                        self.funcs.searchline(self.lines, "visited_cities:")):
            self.ui.cities_text.append("No cities visited yet.")

    def checkDealers(self):
        if self.ownsSC:
            self.dealersets2 += self.dealersets2_sc
        if self.ownsFR:
            self.dealersets2 += self.dealersets2_fr
        if self.ownsIT:
            self.dealersets2 += self.dealersets2_it
        self.ui.dealerships_text.clear()
        for i in self.funcs.getarrayitems(self.lines,
                                          self.funcs.searchline(self.lines, "unlocked_dealers:")):
            self.ui.dealerships_text.append(i)
        if not self.funcs.getarrayitems(self.lines,
                                        self.funcs.searchline(self.lines, "unlocked_dealers:")):
            self.ui.dealerships_text.append("No dealerships unlocked yet.")

    def checkAgencies(self):
        if self.ownsSC:
            self.agenciesets2 += self.agenciesets2_sc
        if self.ownsFR:
            self.agenciesets2 += self.agenciesets2_fr
        if self.ownsIT:
            self.agenciesets2 += self.agenciesets2_it
        self.ui.agencies_text.clear()
        for i in self.funcs.getarrayitems(self.lines,
                                          self.funcs.searchline(self.lines, "unlocked_recruitments:")):
            self.ui.agencies_text.append(i)
        if not self.funcs.getarrayitems(self.lines,
                                        self.funcs.searchline(self.lines, "unlocked_recruitments:")):
            self.ui.agencies_text.append("No recruitment agencies unlocked yet.")

    def addGarage(self):
        garage = str(self.ui.garage_lineedit.text()).lower()
        self.ui.garage_lineedit.setText("")
        if self.funcs.getvalue(self.lines,
                               self.funcs.searchlineinunit(self.lines, "status:", "garage." + garage)) != "0":
            self.funcs.showMsgBox("Error", "Garage in \"{}\" already unlocked.".format(garage))
        else:
            self.funcs.setvalue(self.lines,
                                self.funcs.searchlineinunit(self.lines, "status:", "garage." + garage),
                                "6")
            self.funcs.addarrayvalue(self.lines,
                                     self.funcs.searchlineinunit(self.lines, "vehicles:", "garage." + garage),
                                     "null")
            self.funcs.addarrayvalue(self.lines,
                                     self.funcs.searchlineinunit(self.lines, "drivers:", "garage." + garage),
                                     "null")
            self.funcs.showMsgBox("Success", "Garage in \"{}\" successfully unlocked.".format(garage))
            self.checkGarages()

    def addAllGarages(self):
        line = 0
        try:
            while True:
                line = self.funcs.searchline(self.lines, "garage : garage.", start=line)
                if self.funcs.getvalue(self.lines,
                                       self.funcs.searchlineinunit(self.lines, "status:",
                                                                   self.funcs.getunitname(self.lines, line))) == "0":
                    self.funcs.setvalue(self.lines,
                                        self.funcs.searchlineinunit(self.lines,
                                                                    "status:", self.funcs.getunitname(self.lines, line)),
                                        "6")
                    self.funcs.addarrayvalue(self.lines,
                                             self.funcs.searchlineinunit(self.lines,
                                                                         "vehicles:", self.funcs.getunitname(self.lines, line)),
                                             "null")
                    self.funcs.addarrayvalue(self.lines,
                                             self.funcs.searchlineinunit(self.lines,
                                                                         "drivers:", self.funcs.getunitname(self.lines, line)),
                                             "null")
                line += 1
        except:
            pass
        self.funcs.showMsgBox("Success", "All garages successfully unlocked.")
        self.checkGarages()

    def addCity(self):
        city = str(self.ui.city_lineedit.text()).lower()
        self.ui.city_lineedit.setText("")
        if city in self.funcs.getarrayitems(self.lines,
                                            self.funcs.searchline(self.lines, "visited_cities:")):
            self.funcs.showMsgBox("Error", "You already visited \"{}\"".format(city))
        else:
            self.funcs.addarrayvalue(self.lines,
                                     self.funcs.searchline(self.lines, "visited_cities:"),
                                     city)
            self.funcs.addarrayvalue(self.lines,
                                     self.funcs.searchline(self.lines, "visited_cities_count:"),
                                     "1")
            self.funcs.showMsgBox("Success", "City \"{}\" successfully visited.".format(city))
            self.checkCities()

    def addAllCities(self):
        for city in self.cities():
            if city not in self.funcs.getarrayitems(self.lines,
                                                    self.funcs.searchline(self.lines, "visited_cities:")):
                self.funcs.addarrayvalue(self.lines,
                                         self.funcs.searchline(self.lines, "visited_cities:"),
                                         city)
                self.funcs.addarrayvalue(self.lines,
                                         self.funcs.searchline(self.lines, "visited_cities_count:"),
                                         "1")
        self.funcs.showMsgBox("Success", "All cities successfully visited.")
        self.checkCities()

    def addDealership(self):
        dealer = str(self.ui.dealership_lineedit.text()).lower()
        self.ui.dealership_lineedit.setText("")
        if (not self.ownsATS and dealer not in self.dealersets2) or (self.ownsATS and dealer not in self.dealersats):
            self.funcs.showMsgBox("Error", "There is no dealership in that city.")
        elif dealer in self.funcs.getarrayitems(self.lines, self.funcs.searchline(self.lines, "unlocked_dealers:")):
            self.funcs.showMsgBox("Error", "Dealership is already unlocked.")
        else:
            self.funcs.addarrayvalue(self.lines,
                                     self.funcs.searchline(self.lines, "unlocked_dealers:"),
                                     dealer)
            self.funcs.showMsgBox("Success", "Dealership in \"{}\" successfully unlocked.".format(dealer))
            self.checkDealers()

    def addAllDealership(self):
        if not self.ownsATS:
            for dealer in self.dealersets2:
                if dealer in self.cities() and dealer not in self.funcs.getarrayitems(
                        self.lines, self.funcs.searchline(self.lines, "unlocked_dealers:")):
                    self.funcs.addarrayvalue(self.lines,
                                             self.funcs.searchline(self.lines, "unlocked_dealers:"),
                                             dealer)
        else:
            for dealer in self.dealersats:
                if dealer in self.cities() and dealer not in self.funcs.getarrayitems(
                        self.lines, self.funcs.searchline(self.lines, "unlocked_dealers:")):
                    self.funcs.addarrayvalue(self.lines,
                                             self.funcs.searchline(self.lines, "unlocked_dealers:"),
                                             dealer)
        self.funcs.showMsgBox("Success", "All dealerships unlocked.")
        self.checkDealers()

    def addAgency(self):
        agency = str(self.ui.agency_lineedit.text()).lower()
        self.ui.agency_lineedit.setText("")
        if (not self.ownsATS and agency not in self.agenciesets2) or (self.ownsATS and agency not in self.agenciesats):
            self.funcs.showMsgBox("Error", "There is no recruitment agency in that city.")
        elif agency in self.funcs.getarrayitems(self.lines,
                                                self.funcs.searchline(self.lines, "unlocked_recruitments:")):
            self.funcs.showMsgBox("Error", "Recruitment agency is already unlocked.")
        else:
            self.funcs.addarrayvalue(self.lines,
                                     self.funcs.searchline(self.lines, "unlocked_recruitments:"),
                                     agency)
            self.funcs.showMsgBox("Success", "Recruitment agency in \"{}\" successfully unlocked.".format(agency))
            self.checkAgencies()

    def addAllAgency(self):
        if not self.ownsATS:
            for agency in self.agenciesets2:
                if agency in self.cities() and agency not in self.funcs.getarrayitems(
                        self.lines, self.funcs.searchline(self.lines, "unlocked_recruitments:")):
                    self.funcs.addarrayvalue(self.lines,
                                             self.funcs.searchline(self.lines, "unlocked_recruitments:"),
                                             agency)
        else:
            for agency in self.agenciesats:
                if agency in self.cities() and agency not in self.funcs.getarrayitems(
                        self.lines, self.funcs.searchline(self.lines, "unlocked_recruitments:")):
                    self.funcs.addarrayvalue(self.lines,
                                             self.funcs.searchline(self.lines, "unlocked_recruitments:"),
                                             agency)
        self.funcs.showMsgBox("Success", "All recruitment agencies unlocked.")
        self.checkAgencies()

    def changeHQ(self):
        hq = str(self.ui.headquarter_lineedit.text()).lower()
        if self.funcs.getvalue(self.lines, self.funcs.searchline(self.lines, "hq_city:")) == hq:
            self.funcs.showMsgBox("Error", "Your headquarter is already in this city")
        elif hq not in self.purchasedgarages():
            self.funcs.showMsgBox("Error", "You need to own the garage in this city.")
        else:
            self.funcs.setvalue(self.lines, self.funcs.searchline(self.lines, "hq_city:"), hq)
            self.funcs.showMsgBox("Success", "Headquarter successfully set to \"{}\".".format(hq))

    # TODO: send self.lines to MainWindow()
    def closeEvent(self, event):
        from main_script import MainWindow
        mainw = MainWindow()
        mainw.returnLines(self.lines)
