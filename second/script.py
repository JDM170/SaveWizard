#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from .form import Ui_SecondWindow
from util import *


class SecondWindow(QDialog, Ui_SecondWindow):
    def __init__(self, lines, owns_sc, owns_fr, owns_it, owns_ats, parent=None):
        from PyQt5.QtCore import Qt
        QDialog.__init__(self, parent, flags=Qt.Window)
        Ui_SecondWindow.__init__(self)
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self)

        self.lines = lines
        self.owns_sc = owns_sc
        self.owns_fr = owns_fr
        self.owns_it = owns_it
        self.owns_ats = owns_ats

        # Default dealers
        self.dealers_ets2 = ["aberdeen", "amsterdam", "berlin", "bern", "birmingham", "bratislava", "bremen", "brussel",
                             "budapest", "calais", "cardiff", "dortmund", "dortmund", "dresden", "dusseldorf",
                             "edinburgh", "felixstowe", "frankfurt", "gdansk", "glasgow", "graz", "grimsby", "hamburg",
                             "hannover", "krakow", "leipzig", "lille", "london", "luxembourg", "manchester", "munchen",
                             "newcastle", "nurnberg", "osnabruck", "plymouth", "prague", "rostock", "rotterdam",
                             "salzburg", "strasbourg", "stuttgart", "szczecin", "szeged", "warszawa", "wien", "wroclaw",
                             "zurich"]
        # SC dealers
        self.dealers_ets2_sc = ["bergen", "goteborg", "kalmar", "kobenhavn", "linkoping", "oslo", "stockholm"]
        # FR dealers
        self.dealers_ets2_fr = ["bordeaux", "bourges", "brest", "geneve", "lemans", "limoges", "lyon", "marseille",
                                "nantes", "paris", "toulouse"]
        # IT dealers
        self.dealers_ets2_it = ["bologna", "catania", "firenze", "milano", "napoli", "palermo", "roma", "taranto",
                                "torino", "verona"]
        # Default agnecies
        self.agencies_ets2 = ["aberdeen", "berlin", "bialystok", "birmingham", "bremen", "brno",
                              "brussel", "budapest", "calais", "debrecen", "dortmund", "dover", "dresden", "edinburgh",
                              "frankfurt", "gdansk", "glasgow", "graz", "grohningen", "hamburg", "hannover",
                              "innsbruck", "kassel", "klagenfurt", "koln", "kosice", "krakow", "leipzig", "liege",
                              "linz", "liverpool", "lodz", "london", "luxembourg", "manchester", "mannheim", "munchen",
                              "newcastle", "nurnberg", "ostrava", "pecs", "plymouth", "poznan", "prague", "sheffield",
                              "southampton", "stuttgart", "swansea", "szczecin", "szeged", "warszava", "wien", "zurich"]
        # SC agencies
        self.agencies_ets2_sc = ["aalborg", "bergen", "helsingborg", "kobenhavn", "malmo", "odense", "oslo",
                                 "stavanger", "stockholm"]
        # FR agencies
        self.agencies_ets2_fr = ["bordeaux", "clermont", "geneve", "larochelle", "lyon", "marseille", "metz", "paris",
                                 "reims", "rennes", "toulouse"]
        # IT agencies
        self.agencies_ets2_it = ["bologna", "catania", "milano", "napoli", "pescara", "roma", "taranto", "venezia"]
        # ATS dealers
        self.dealers_ats = ["elko", "reno", "bakersfield", "phoenix", "flagstaff", "los_angeles", "albuquerque",
                            "hobbs"]
        # ATS agencies
        self.agencies_ats = ["redding", "san_rafael", "stockton", "fresno", "santa_cruz", "bakersfield", "oxnard",
                             "los_angeles", "san_diego", "carson_city", "las_vegas", "phoenix", "tucson",
                             "sierra_vista", "farmington", "santa_fe", "roswell", "carlsbad_nm"]

        self.ui.garage_size.addItem("Small")
        self.ui.garage_size.addItem("Medium")
        self.ui.garage_size.addItem("Big")

        self.ui.garages_analyze.clicked.connect(self.check_garages)
        self.ui.garage_add.clicked.connect(self.add_garage)
        self.ui.garage_unlock_all.clicked.connect(self.add_all_garages)
        self.ui.headquarter_change.clicked.connect(self.change_headquarter)
        self.ui.cities_analyze.clicked.connect(self.check_cities)
        self.ui.city_add.clicked.connect(self.add_city)
        self.ui.city_unlock_all.clicked.connect(self.add_all_cities)
        self.ui.dealerships_analyze.clicked.connect(self.check_dealers)
        self.ui.dealership_add.clicked.connect(self.add_dealer)
        self.ui.dealership_unlock_all.clicked.connect(self.add_all_dealers)
        self.ui.agencies_analyze.clicked.connect(self.check_agencies)
        self.ui.agency_add.clicked.connect(self.add_agency)
        self.ui.agency_unlock_all.clicked.connect(self.add_all_agencies)

    def check_garage_size(self):
        text = str(self.ui.garage_size.currentText())
        garage_size = 0
        garage_status = 0
        if text == "Small":
            garage_size = 1
            garage_status = 1
        elif text == "Medium":
            garage_size = 3
            garage_status = 2
        elif text == "Big":
            garage_size = 5
            garage_status = 3
        return garage_size, garage_status

    def purchased_garages(self):
        garages = []
        i = 0
        try:
            while True:
                while "garage : " not in self.lines[i]:
                    i += 1
                city = match(r"garage : garage.(.+) {$", self.lines[i]).group(1)
                while "status:" not in self.lines[i]:
                    i += 1
                if "0" not in self.lines[i]:
                    garages.append(city)
        except:
            pass
        return garages

    def cities(self):
        cities = []
        line = searchline(self.lines, "companies\[")
        while "companies[" in self.lines[line]:
            city = match(r" companies\[[0-9]+\]: company.volatile.[a-z0-9_]+[.]([a-z_]+)", self.lines[line]).group(1)
            if city not in cities:
                cities.append(city)
            line += 1
        return cities

    def check_garages(self):
        self.ui.garages_text.clear()
        for e in self.purchased_garages():
            self.ui.garages_text.append(e)
        hq = getvalue(self.lines, searchline(self.lines, "hq_city:"))
        self.ui.headquarter_edit.setText(hq)

    def check_cities(self):
        self.ui.cities_text.clear()
        for i in getarrayitems(self.lines, searchline(self.lines, "visited_cities:")):
            self.ui.cities_text.append(i)
        if not getarrayitems(self.lines, searchline(self.lines, "visited_cities:")):
            self.ui.cities_text.append("No cities visited yet.")

    def check_dealers(self):
        self.dealers_ets2 = self.dealers_ets2 + self.dealers_ets2_sc if self.owns_sc else self.dealers_ets2
        self.dealers_ets2 = self.dealers_ets2 + self.dealers_ets2_fr if self.owns_fr else self.dealers_ets2
        self.dealers_ets2 = self.dealers_ets2 + self.dealers_ets2_it if self.owns_it else self.dealers_ets2
        self.ui.dealerships_text.clear()
        for i in getarrayitems(self.lines, searchline(self.lines, "unlocked_dealers:")):
            self.ui.dealerships_text.append(i)
        if not getarrayitems(self.lines, searchline(self.lines, "unlocked_dealers:")):
            self.ui.dealerships_text.append("No dealerships unlocked yet.")

    def check_agencies(self):
        self.agencies_ets2 = self.agencies_ets2 + self.agencies_ets2_sc if self.owns_sc else self.agencies_ets2
        self.agencies_ets2 = self.agencies_ets2 + self.agencies_ets2_fr if self.owns_fr else self.agencies_ets2
        self.agencies_ets2 = self.agencies_ets2 + self.agencies_ets2_it if self.owns_it else self.agencies_ets2
        self.ui.agencies_text.clear()
        for i in getarrayitems(self.lines, searchline(self.lines, "unlocked_recruitments:")):
            self.ui.agencies_text.append(i)
        if not getarrayitems(self.lines, searchline(self.lines, "unlocked_recruitments:")):
            self.ui.agencies_text.append("No recruitment agencies unlocked yet.")

    def add_garage(self):
        garage = str(self.ui.garage_edit.text()).lower()
        if garage is "":
            show_message("Error", "Enter a name for the city.")
            return
        garage_size, garage_status = self.check_garage_size()
        self.ui.garage_edit.setText("")
        if getvalue(self.lines, searchlineinunit(self.lines, "status:", "garage." + garage)) != "0":
            show_message("Error", "Garage in \"{}\" already unlocked.".format(garage))
        else:
            setvalue(self.lines, searchlineinunit(self.lines, "status:", "garage." + garage), str(garage_status))
            for i in range(garage_size):
                addarrayvalue(self.lines, searchlineinunit(self.lines, "vehicles:", "garage." + garage), "null")
                addarrayvalue(self.lines, searchlineinunit(self.lines, "drivers:", "garage." + garage), "null")
            show_message("Success", "Garage in \"{}\" successfully unlocked.".format(garage))
            self.check_garages()

    def add_all_garages(self):
        garage_size, garage_status = self.check_garage_size()
        line = 0
        try:
            while True:
                line = searchline(self.lines, "garage : garage.", start=line)
                if getvalue(self.lines, searchlineinunit(self.lines, "status:", getunitname(self.lines, line))) == "0":
                    setvalue(self.lines, searchlineinunit(self.lines, "status:", getunitname(self.lines, line)),
                             str(garage_status))
                    for i in range(garage_size):
                        addarrayvalue(self.lines, searchlineinunit(self.lines, "vehicles:",
                                                                   getunitname(self.lines, line)), "null")
                        addarrayvalue(self.lines, searchlineinunit(self.lines, "drivers:",
                                                                   getunitname(self.lines, line)), "null")
                line += 1
        except:
            pass
        show_message("Success", "All garages successfully unlocked.")
        self.check_garages()

    def add_city(self):
        city = str(self.ui.city_edit.text()).lower()
        if city is "":
            show_message("Error", "Enter a name for the city.")
            return
        self.ui.city_edit.setText("")
        if city not in getarrayitems(self.lines, searchline(self.lines, "visited_cities:")):
            addarrayvalue(self.lines, searchline(self.lines, "visited_cities:"), city)
            addarrayvalue(self.lines, searchline(self.lines, "visited_cities_count:"), "1")
            show_message("Success", "City \"{}\" successfully visited.".format(city))
            self.check_cities()
        else:
            show_message("Error", "You already visited \"{}\"".format(city))

    def add_all_cities(self):
        for city in self.cities():
            if city not in getarrayitems(self.lines, searchline(self.lines, "visited_cities:")):
                addarrayvalue(self.lines, searchline(self.lines, "visited_cities:"), city)
                addarrayvalue(self.lines, searchline(self.lines, "visited_cities_count:"), "1")
        show_message("Success", "All cities successfully visited.")
        self.check_cities()

    def add_dealer(self):
        dealer = str(self.ui.dealership_edit.text()).lower()
        if dealer is "":
            show_message("Error", "Enter a name for the city.")
            return
        self.ui.dealership_edit.setText("")
        if (not self.owns_ats and dealer not in self.dealers_ets2) or (
                self.owns_ats and dealer not in self.dealers_ats):
            show_message("Error", "There is no dealership in that city.")
        elif dealer in getarrayitems(self.lines, searchline(self.lines, "unlocked_dealers:")):
            show_message("Error", "Dealership is already unlocked.")
        else:
            addarrayvalue(self.lines, searchline(self.lines, "unlocked_dealers:"), dealer)
            show_message("Success", "Dealership in \"{}\" successfully unlocked.".format(dealer))
            self.check_dealers()

    def add_all_dealers(self):
        for dealer in (self.dealers_ets2 if not self.owns_ats else self.dealers_ats):
            if dealer in self.cities() and dealer not in getarrayitems(self.lines,
                                                                       searchline(self.lines, "unlocked_dealers:")):
                addarrayvalue(self.lines, searchline(self.lines, "unlocked_dealers:"), dealer)
        show_message("Success", "All dealerships unlocked.")
        self.check_dealers()

    def add_agency(self):
        agency = str(self.ui.agency_edit.text()).lower()
        if agency is "":
            show_message("Error", "Enter a name for the city.")
            return
        self.ui.agency_edit.setText("")
        if (not self.owns_ats and agency not in self.agencies_ets2) or (
                self.owns_ats and agency not in self.agencies_ats):
            show_message("Error", "There is no recruitment agency in that city.")
        elif agency in getarrayitems(self.lines, searchline(self.lines, "unlocked_recruitments:")):
            show_message("Error", "Recruitment agency is already unlocked.")
        else:
            addarrayvalue(self.lines, searchline(self.lines, "unlocked_recruitments:"), agency)
            show_message("Success", "Recruitment agency in \"{}\" successfully unlocked.".format(agency))
            self.check_agencies()

    def add_all_agencies(self):
        for agency in (self.agencies_ets2 if not self.owns_ats else self.agencies_ats):
            if agency in self.cities() and agency not in getarrayitems(
                    self.lines, searchline(self.lines, "unlocked_recruitments:")):
                addarrayvalue(self.lines, searchline(self.lines, "unlocked_recruitments:"), agency)
        show_message("Success", "All recruitment agencies unlocked.")
        self.check_agencies()

    def change_headquarter(self):
        hq = str(self.ui.headquarter_edit.text()).lower()
        if hq is "":
            show_message("Error", "Enter a name for the city.")
            return
        if getvalue(self.lines, searchline(self.lines, "hq_city:")) == hq:
            show_message("Error", "Your headquarter is already in this city")
        elif hq not in self.purchased_garages():
            show_message("Error", "You need to own the garage in this city.")
        else:
            setvalue(self.lines, searchline(self.lines, "hq_city:"), hq)
            show_message("Success", "Headquarter successfully set to \"{}\".".format(hq))

    def closeEvent(self, event):
        from main.script import MainWindow
        MainWindow().return_lines(self.lines)
