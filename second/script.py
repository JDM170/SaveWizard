#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from .form import Ui_SecondWindow
from util import *
from dataIO import dataIO


class SecondWindow(QDialog, Ui_SecondWindow):
    def __init__(self, owns_list, parent=None):
        # Setup UI
        QDialog.__init__(self, parent, flags=Qt.Window)
        Ui_SecondWindow.__init__(self)
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self)

        self.owns = owns_list  # From main window

        # Checking files
        if dataIO.is_valid_json("dealers.json") is False:
            self.dealers = False
            self.ui.dealer_edit.setEnabled(False)
            self.ui.dealer_add.setEnabled(False)
            self.ui.dealer_add_all.setEnabled(False)
            show_message(QMessageBox.Warning, "Warning", "'dealers.json' not found, dealers editing has been disabled")
        else:
            self.dealers = []
            self.dealers_file = dataIO.load_json("dealers.json")

        if dataIO.is_valid_json("agencies.json") is False:
            self.agencies = False
            self.ui.agency_edit.setEnabled(False)
            self.ui.agency_add.setEnabled(False)
            self.ui.agency_add_all.setEnabled(False)
            show_message(QMessageBox.Warning, "Warning", "'agencies.json' not found, agencies editing has been"
                                                         "disabled")
        else:
            self.agencies = []
            self.agencies_file = dataIO.load_json("agencies.json")

        self.ui.garage_size.addItem("Small")
        self.ui.garage_size.addItem("Medium")
        self.ui.garage_size.addItem("Big")

        # Connecting buttons
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

        # Checking save-file
        self.initialize_arrays()
        self.check_cities()
        self.check_dealers()
        self.check_agencies()

    @staticmethod
    def purchased_garages():
        garages = []
        for index in search_all_lines("garage : garage."):
            city = match(r"garage : garage.(.+) {$", get_lines(index)).group(1)
            if get_value(search_line("status:", start=index)) != "0":
                garages.append(city)
        return garages

    @staticmethod
    def all_cities():
        cities = []
        for line in get_array_items(search_line("companies:")):
            city = match(r"company.volatile.[a-z0-9_]+[.]([a-z_]+)", line).group(1)
            if city not in cities:
                cities.append(city)
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
        status = 0
        size = 0
        if text == "Small":
            status = 1
            size = 1
        elif text == "Medium":
            status = 2
            size = 3
        elif text == "Big":
            status = 3
            size = 5
        return str(status), size

    def check_garages(self):
        self.ui.garages_text.clear()
        for garage in self.purchased_garages():
            self.ui.garages_text.append(garage)

    def add_garage(self):
        garage = self.ui.garage_edit.text().lower()
        if garage is "":
            show_message(QMessageBox.Critical, "Error", "Enter a name for the city.")
            return
        self.ui.garage_edit.setText("")
        reg_garage = "garage." + garage
        current_status = search_line_in_unit("status:", reg_garage)
        if get_value(current_status) == "0":
            new_status, size = self.check_garage_size()
            set_value(current_status, new_status)
            vehicles_array = search_line_in_unit("vehicles:", reg_garage)
            drivers_array = search_line_in_unit("drivers:", reg_garage)
            for i in range(1, size+1):
                add_array_value(vehicles_array, "null")
                add_array_value(drivers_array+i, "null")
            show_message(QMessageBox.Information, "Success", "Garage in \"{}\" successfully unlocked.".format(garage))
        else:
            show_message(QMessageBox.Warning, "Warning", "Garage in \"{}\" already unlocked.".format(garage))

    def add_all_garages(self):
        new_status, size = self.check_garage_size()
        for item in get_array_items(search_line("garages:")):
            item = match(r"garage.(.+)$", item).group(1)
            current_garage = search_line("garage : garage."+item+" {")
            current_status = search_line("status:", start=current_garage)
            if get_value(current_status) == "0":
                set_value(current_status, new_status)
                vehicles_array = search_line("vehicles:", start=current_garage)
                drivers_array = search_line("drivers:", start=current_garage)
                for i in range(1, size+1):
                    add_array_value(vehicles_array, "null")
                    add_array_value(drivers_array+i, "null")
        show_message(QMessageBox.Information, "Success", "All garages successfully unlocked.")

    def change_headquarter(self):
        hq = self.ui.headquarter_edit.text().lower()
        if hq is "":
            show_message(QMessageBox.Critical, "Error", "Enter a name for the city.")
            return
        if get_value(search_line("hq_city:")) == hq:
            show_message(QMessageBox.Critical, "Error", "Your headquarter is already in this city")
        elif hq not in self.purchased_garages():
            show_message(QMessageBox.Critical, "Error", "You need to own the garage in this city.")
        else:
            set_value(search_line("hq_city:"), hq)
            show_message(QMessageBox.Information, "Success", "Headquarter successfully set to \"{}\".".format(hq))

    def check_cities(self):
        self.ui.headquarter_edit.setText(get_value(search_line("hq_city:")))
        self.ui.cities_text.clear()
        visited_cities = get_array_items(search_line("visited_cities:"))
        if not visited_cities:
            self.ui.cities_text.append("No cities visited yet.")
            return
        for city in visited_cities:
            self.ui.cities_text.append(city)

    def add_city(self):
        city = self.ui.city_edit.text().lower()
        if city is "":
            show_message(QMessageBox.Critical, "Error", "Enter a name for the city.")
            return
        self.ui.city_edit.setText("")
        if city not in get_array_items(search_line("visited_cities:")):
            add_array_value(search_line("visited_cities:"), city)
            add_array_value(search_line("visited_cities_count:"), "1")
            show_message(QMessageBox.Warning, "Success", "City \"{}\" successfully visited.".format(city))
            self.check_cities()
        else:
            show_message(QMessageBox.Critical, "Error", "You already visited \"{}\".".format(city))

    def add_all_cities(self):
        visited_cities = get_array_items(search_line("visited_cities:"))
        for city in self.all_cities():
            if city not in visited_cities:
                add_array_value(search_line("visited_cities:"), city)
                add_array_value(search_line("visited_cities_count:"), "1")
        show_message(QMessageBox.Information, "Success", "All cities successfully visited.")
        self.check_cities()

    def check_dealers(self):
        self.ui.dealerships_text.clear()
        visited_dealers = get_array_items(search_line("unlocked_dealers:"))
        if not visited_dealers:
            self.ui.dealerships_text.append("No dealerships unlocked yet.")
            return
        for dealer in visited_dealers:
            self.ui.dealerships_text.append(dealer)

    def add_dealer(self):
        dealer = self.ui.dealer_edit.text().lower()
        if dealer is "":
            show_message(QMessageBox.Critical, "Error", "Enter a name for the city.")
            return
        self.ui.dealer_edit.setText("")
        if dealer not in self.dealers:
            show_message(QMessageBox.Critical, "Error", "There is no dealership in that city.")
        elif dealer in get_array_items(search_line("unlocked_dealers:")):
            show_message(QMessageBox.Critical, "Error", "This dealership already unlocked.")
        else:
            add_array_value(search_line("unlocked_dealers:"), dealer)
            show_message(QMessageBox.Information, "Success", "Dealership in \"{}\" successfully unlocked."
                                                             "".format(dealer))
            self.check_dealers()

    def add_all_dealers(self):
        all_cities = self.all_cities()
        visited_dealers = get_array_items(search_line("unlocked_dealers:"))
        for dealer in self.dealers:
            if dealer in all_cities and dealer not in visited_dealers:
                add_array_value(search_line("unlocked_dealers:"), dealer)
        show_message(QMessageBox.Information, "Success", "All dealerships unlocked.")
        self.check_dealers()

    def check_agencies(self):
        self.ui.agencies_text.clear()
        visited_agencies = get_array_items(search_line("unlocked_recruitments:"))
        if not visited_agencies:
            self.ui.agencies_text.append("No recruitment agencies unlocked yet.")
            return
        for agency in visited_agencies:
            self.ui.agencies_text.append(agency)

    def add_agency(self):
        agency = self.ui.agency_edit.text().lower()
        if agency is "":
            show_message(QMessageBox.Critical, "Error", "Enter a name for the city.")
            return
        self.ui.agency_edit.setText("")
        if agency not in self.agencies:
            show_message(QMessageBox.Critical, "Error", "There is no recruitment agency in that city.")
        elif agency in get_array_items(search_line("unlocked_recruitments:")):
            show_message(QMessageBox.Critical, "Error", "Recruitment agency is already unlocked.")
        else:
            add_array_value(search_line("unlocked_recruitments:"), agency)
            show_message(QMessageBox.Information, "Success", "Recruitment agency in \"{}\" successfully unlocked."
                                                             "".format(agency))
            self.check_agencies()

    def add_all_agencies(self):
        all_cities = self.all_cities()
        visited_agencies = get_array_items(search_line("unlocked_recruitments:"))
        for agency in self.agencies:
            if agency in all_cities and agency not in visited_agencies:
                add_array_value(search_line("unlocked_recruitments:"), agency)
        show_message(QMessageBox.Information, "Success", "All recruitment agencies unlocked.")
        self.check_agencies()
