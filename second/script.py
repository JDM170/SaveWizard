#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from .form import Ui_SecondWindow
from util import *
from dataIO import dataIO


class SecondWindow(QDialog, Ui_SecondWindow):
    def __init__(self, owns_list, parent=None):
        from PyQt5.QtCore import Qt
        QDialog.__init__(self, parent, flags=Qt.Window)
        Ui_SecondWindow.__init__(self)
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self)

        self.owns = owns_list  # From main window

        if dataIO.is_valid_json("dealers.json") is False:
            self.dealers = False
            self.ui.dealer_edit.setEnabled(False)
            self.ui.dealer_add.setEnabled(False)
            self.ui.dealer_add_all.setEnabled(False)
            show_message("Error", "'dealers.json' not found, dealers editing has been disabled")
        else:
            self.dealers = []
            self.dealers_file = dataIO.load_json("dealers.json")

        if dataIO.is_valid_json("agencies.json") is False:
            self.agencies = False
            self.ui.agency_edit.setEnabled(False)
            self.ui.agency_add.setEnabled(False)
            self.ui.agency_add_all.setEnabled(False)
            show_message("Error", "'agencies.json' not found, agencies editing has been disabled")
        else:
            self.agencies = []
            self.agencies_file = dataIO.load_json("agencies.json")

        self.ui.garage_size.addItem("Small")
        self.ui.garage_size.addItem("Medium")
        self.ui.garage_size.addItem("Big")

        self.ui.garages_analyze.clicked.connect(self.check_garages)
        self.ui.garage_add.clicked.connect(self.add_garage)
        self.ui.garage_add_all.clicked.connect(self.add_all_garages)
        self.ui.headquarter_change.clicked.connect(self.change_headquarter)
        self.ui.city_add.clicked.connect(self.add_city)
        self.ui.city_add_all.clicked.connect(self.add_all_cities)
        self.ui.dealer_add.clicked.connect(self.add_dealer)
        self.ui.dealer_add_all.clicked.connect(self.add_all_dealers)
        self.ui.agency_add.clicked.connect(self.add_agency)
        self.ui.agency_add_all.clicked.connect(self.add_all_agencies)

        self.initialize_arrays()
        self.check_cities()
        self.check_dealers()
        self.check_agencies()

    @staticmethod
    def purchased_garages():
        garages = []
        i = 0
        try:
            local_lines = get_lines()
            while True:
                while "garage : " not in local_lines[i]:
                    i += 1
                city = match(r"garage : garage.(.+) {$", local_lines[i]).group(1)
                while "status:" not in local_lines[i]:
                    i += 1
                if "0" not in local_lines[i]:
                    garages.append(city)
        except:
            pass
        return garages

    @staticmethod
    def cities():
        cities = []
        line = search_line(r"companies\[")
        local_lines = get_lines()
        while "companies[" in local_lines[line]:
            city = match(r" companies\[[0-9]+\]: company.volatile.[a-z0-9_]+[.]([a-z_]+)", local_lines[line]).group(1)
            if city not in cities:
                cities.append(city)
            line += 1
        return cities

    def initialize_arrays(self):
        if self.owns is False:
            return
        for key in self.owns.keys():
            if self.dealers is not False and key in self.dealers_file:
                for value in self.dealers_file[key]:
                    self.dealers.append(value)
            if self.agencies is not False and key in self.agencies_file:
                for value in self.agencies_file[key]:
                    self.agencies.append(value)

    def check_garage_size(self):
        text = self.ui.garage_size.currentText()
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
        return garage_size, str(garage_status)

    def check_garages(self):
        self.ui.garages_text.clear()
        for garage in self.purchased_garages():
            self.ui.garages_text.append(garage)
        hq = get_value(search_line("hq_city:"))
        self.ui.headquarter_edit.setText(hq)

    def add_garage(self):
        garage = self.ui.garage_edit.text().lower()
        if garage is "":
            show_message("Error", "Enter a name for the city.")
            return
        garage_size, garage_status = self.check_garage_size()
        self.ui.garage_edit.setText("")
        if get_value(search_line_in_unit("status:", "garage." + garage)) != "0":
            show_message("Error", "Garage in \"{}\" already unlocked.".format(garage))
        else:
            set_value(search_line_in_unit("status:", "garage." + garage), garage_status)
            for i in range(garage_size):
                add_array_value(search_line_in_unit("vehicles:", "garage." + garage), "null")
                add_array_value(search_line_in_unit("drivers:", "garage." + garage), "null")
            show_message("Success", "Garage in \"{}\" successfully unlocked.".format(garage))
            self.check_garages()

    def add_all_garages(self):
        garage_size, garage_status = self.check_garage_size()
        line = 0
        try:
            while True:
                line = search_line("garage : garage.", start=line)
                if get_value(search_line_in_unit("status:", get_unit_name(line))) == "0":
                    set_value(search_line_in_unit("status:", get_unit_name(line)), garage_status)
                    for i in range(garage_size):
                        add_array_value(search_line_in_unit("vehicles:", get_unit_name(line)), "null")
                        add_array_value(search_line_in_unit("drivers:", get_unit_name(line)), "null")
                line += 1
        except:
            pass
        show_message("Success", "All garages successfully unlocked.")
        self.check_garages()

    def change_headquarter(self):
        hq = self.ui.headquarter_edit.text().lower()
        if hq is "":
            show_message("Error", "Enter a name for the city.")
            return
        if get_value(search_line("hq_city:")) == hq:
            show_message("Error", "Your headquarter is already in this city")
        elif hq not in self.purchased_garages():
            show_message("Error", "You need to own the garage in this city.")
        else:
            set_value(search_line("hq_city:"), hq)
            show_message("Success", "Headquarter successfully set to \"{}\".".format(hq))

    def check_cities(self):
        self.ui.cities_text.clear()
        for city in get_array_items(search_line("visited_cities:")):
            self.ui.cities_text.append(city)
        if not get_array_items(search_line("visited_cities:")):
            self.ui.cities_text.append("No cities visited yet.")

    def add_city(self):
        city = self.ui.city_edit.text().lower()
        if city is "":
            show_message("Error", "Enter a name for the city.")
            return
        self.ui.city_edit.setText("")
        if city not in get_array_items(search_line("visited_cities:")):
            add_array_value(search_line("visited_cities:"), city)
            add_array_value(search_line("visited_cities_count:"), "1")
            show_message("Success", "City \"{}\" successfully visited.".format(city))
            self.check_cities()
        else:
            show_message("Error", "You already visited \"{}\".".format(city))

    def add_all_cities(self):
        for city in self.cities():
            if city not in get_array_items(search_line("visited_cities:")):
                add_array_value(search_line("visited_cities:"), city)
                add_array_value(search_line("visited_cities_count:"), "1")
        show_message("Success", "All cities successfully visited.")
        self.check_cities()

    def check_dealers(self):
        self.ui.dealerships_text.clear()
        for dealer in get_array_items(search_line("unlocked_dealers:")):
            self.ui.dealerships_text.append(dealer)
        if not get_array_items(search_line("unlocked_dealers:")):
            self.ui.dealerships_text.append("No dealerships unlocked yet.")

    def add_dealer(self):
        dealer = self.ui.dealer_edit.text().lower()
        if dealer is "":
            show_message("Error", "Enter a name for the city.")
            return
        self.ui.dealer_edit.setText("")
        if dealer not in self.dealers:
            show_message("Error", "There is no dealership in that city.")
        elif dealer in get_array_items(search_line("unlocked_dealers:")):
            show_message("Error", "This dealership already unlocked.")
        else:
            add_array_value(search_line("unlocked_dealers:"), dealer)
            show_message("Success", "Dealership in \"{}\" successfully unlocked.".format(dealer))
            self.check_dealers()

    def add_all_dealers(self):
        for dealer in self.dealers:
            if dealer in self.cities() and dealer not in get_array_items(search_line("unlocked_dealers:")):
                add_array_value(search_line("unlocked_dealers:"), dealer)
        show_message("Success", "All dealerships unlocked.")
        self.check_dealers()

    def check_agencies(self):
        self.ui.agencies_text.clear()
        for agency in get_array_items(search_line("unlocked_recruitments:")):
            self.ui.agencies_text.append(agency)
        if not get_array_items(search_line("unlocked_recruitments:")):
            self.ui.agencies_text.append("No recruitment agencies unlocked yet.")

    def add_agency(self):
        agency = self.ui.agency_edit.text().lower()
        if agency is "":
            show_message("Error", "Enter a name for the city.")
            return
        self.ui.agency_edit.setText("")
        if agency not in self.agencies:
            show_message("Error", "There is no recruitment agency in that city.")
        elif agency in get_array_items(search_line("unlocked_recruitments:")):
            show_message("Error", "Recruitment agency is already unlocked.")
        else:
            add_array_value(search_line("unlocked_recruitments:"), agency)
            show_message("Success", "Recruitment agency in \"{}\" successfully unlocked.".format(agency))
            self.check_agencies()

    def add_all_agencies(self):
        for agency in self.agencies:
            if agency in self.cities() and agency not in get_array_items(search_line("unlocked_recruitments:")):
                add_array_value(search_line("unlocked_recruitments:"), agency)
        show_message("Success", "All recruitment agencies unlocked.")
        self.check_agencies()
