#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from .form import Ui_SecondWindow
from util import *
from dataIO import dataIO

garages_stat = {
    "Small": [1, 1],
    "Medium": [2, 3],
    "Big": [3, 5]
}


class SecondWindow(QDialog, Ui_SecondWindow):
    def __init__(self, selected_game, owns_list, parent=None):
        # Setup UI
        QDialog.__init__(self, parent, flags=Qt.Window)
        Ui_SecondWindow.__init__(self)
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self)

        self.owns = owns_list  # From main window

        # Checking files
        cfg_path = "configs/{}".format(selected_game)
        dealers_path = "{}/dealers.json".format(cfg_path)
        agencies_path = "{}/agencies.json".format(cfg_path)
        if dataIO.is_valid_json(dealers_path) is False:
            self.dealers = False
            self.ui.dealer_edit.setEnabled(False)
            self.ui.dealer_add.setEnabled(False)
            self.ui.dealer_add_all.setEnabled(False)
            QMessageBox.warning(self, "Warning", "'dealers.json' from '{}' have errors or not found.\n"
                                                 "Dealers editing has been disabled".format(selected_game))
        else:
            self.dealers = []
            self.dealers_file = dataIO.load_json(dealers_path)

        if dataIO.is_valid_json(agencies_path) is False:
            self.agencies = False
            self.ui.agency_edit.setEnabled(False)
            self.ui.agency_add.setEnabled(False)
            self.ui.agency_add_all.setEnabled(False)
            QMessageBox.warning(self, "Warning", "'agencies.json' from '{}' have errors or not found.\n"
                                                 "Agencies editing has been disabled".format(selected_game))
        else:
            self.agencies = []
            self.agencies_file = dataIO.load_json(agencies_path)

        self.ui.garage_size.addItem("Small")
        self.ui.garage_size.addItem("Medium")
        self.ui.garage_size.addItem("Big")

        # Dealers and agencies properties
        self.da_array = {
            self.ui.dealer_add: [self.ui.dealer_edit, "unlocked_dealers:", "Dealership", self.dealers,
                                 self.check_dealers],
            self.ui.agency_add: [self.ui.agency_edit, "unlocked_recruitments:", "Recruitment agency",
                                 self.agencies, self.check_agencies],
        }

        # Connecting buttons
        self.ui.garages_analyze.clicked.connect(self.check_garages)
        self.ui.garage_add.clicked.connect(self.add_garage)
        self.ui.garage_add_all.clicked.connect(self.add_all_garages)
        self.ui.headquarter_change.clicked.connect(self.change_headquarter)
        self.ui.city_add.clicked.connect(self.add_city)
        self.ui.city_add_all.clicked.connect(self.add_all_cities)
        self.ui.dealer_add.clicked.connect(self.da_clicked)
        self.ui.dealer_add_all.clicked.connect(self.add_all_dealers)
        self.ui.agency_add.clicked.connect(self.da_clicked)
        self.ui.agency_add_all.clicked.connect(self.add_all_agencies)

        if self.owns:
            self.fill_list(self.dealers, self.dealers_file)
            self.fill_list(self.agencies, self.agencies_file)
        # Checking save-file
        self.check_cities()
        self.check_dealers()
        self.check_agencies()

    @staticmethod
    def purchased_garages():
        garages = []
        for index in util.search_all_lines("garage : garage."):
            city = match(r"garage : garage.(.+) {$", util.get_lines(index)).group(1)
            if util.get_value(util.search_line("status:", start=index)) != "0":
                garages.append(city)
        return garages

    @staticmethod
    def all_cities():
        cities = []
        for line in util.get_array_items(util.search_line("companies:")):
            city = match(r"company.volatile.[a-z0-9_]+[.]([a-z_]+)", line).group(1)
            if city not in cities:
                cities.append(city)
        return cities

    def fill_list(self, array, file):
        if array is False:
            return
        for key in self.owns.keys():
            if key not in file:
                continue
            for value in file[key]:
                array.append(value)

    def check_garage_size(self):
        stat = garages_stat[self.ui.garage_size.currentText()]
        return str(stat[0]), stat[1]

    def check_garages(self):
        self.ui.garages_text.clear()
        garages = self.purchased_garages()
        for garage in garages:
            self.ui.garages_text.append(garage)
        self.ui.garages_text.scrollToAnchor(garages[0])

    def add_garage(self):
        garage = self.ui.garage_edit.text().lower()
        if garage is "":
            QMessageBox.critical(self, "Error", "Enter city name!")
            return
        self.ui.garage_edit.setText("")
        reg_garage = "garage." + garage
        current_status = util.search_line_in_unit("status:", reg_garage)
        if util.get_value(current_status) == "0":
            new_status, size = self.check_garage_size()
            util.set_value(current_status, new_status)
            vehicles_array = util.search_line_in_unit("vehicles:", reg_garage)
            drivers_array = util.search_line_in_unit("drivers:", reg_garage)
            for i in range(1, size+1):
                util.add_array_value(vehicles_array, "null")
                util.add_array_value(drivers_array+i, "null")
            QMessageBox.information(self, "Success", "Garage in \"{}\" successfully unlocked.".format(garage))
        else:
            QMessageBox.critical(self, "Error", "Garage in \"{}\" already unlocked.".format(garage))

    def add_all_garages(self):
        new_status, size = self.check_garage_size()
        for item in util.get_array_items(util.search_line("garages:")):
            item = match(r"garage.(.+)$", item).group(1)
            current_garage = util.search_line("garage : garage."+item+" {")
            current_status = util.search_line("status:", start=current_garage)
            if util.get_value(current_status) == "0":
                util.set_value(current_status, new_status)
                vehicles_array = util.search_line("vehicles:", start=current_garage)
                drivers_array = util.search_line("drivers:", start=current_garage)
                for i in range(1, size+1):
                    util.add_array_value(vehicles_array, "null")
                    util.add_array_value(drivers_array+i, "null")
        QMessageBox.information(self, "Success", "All garages successfully unlocked.")

    def change_headquarter(self):
        hq = self.ui.headquarter_edit.text().lower()
        if hq is "":
            QMessageBox.critical(self, "Error", "Enter city name!")
            return
        if util.get_value(util.search_line("hq_city:")) == hq:
            QMessageBox.information(self, "Info", "Your headquarter is already in this city.")
        elif hq not in self.purchased_garages():
            QMessageBox.critical(self, "Error", "You need a garage in \"{}\" to set headquarter.".format(hq))
        else:
            util.set_value(util.search_line("hq_city:"), hq)
            QMessageBox.information(self, "Success", "Headquarter successfully set to \"{}\".".format(hq))

    def check_cities(self):
        self.ui.headquarter_edit.setText(util.get_value(util.search_line("hq_city:")))
        self.ui.cities_text.clear()
        visited_cities = util.get_array_items(util.search_line("visited_cities:"))
        if not visited_cities:
            self.ui.cities_text.append("No cities visited yet.")
            return
        for city in visited_cities:
            self.ui.cities_text.append(city)
        self.ui.cities_text.scrollToAnchor(visited_cities[0])

    def add_city(self):
        city = self.ui.city_edit.text().lower()
        if city is "":
            QMessageBox.critical(self, "Error", "Enter city name!")
            return
        self.ui.city_edit.setText("")
        if city not in util.get_array_items(util.search_line("visited_cities:")):
            util.add_array_value(util.search_line("visited_cities:"), city)
            util.add_array_value(util.search_line("visited_cities_count:"), "1")
            QMessageBox.information(self, "Success", "City \"{}\" successfully visited.".format(city))
            self.check_cities()
        else:
            QMessageBox.critical(self, "Error", "You've already visited \"{}\".".format(city))

    def add_all_cities(self):
        visited_cities = util.get_array_items(util.search_line("visited_cities:"))
        for city in self.all_cities():
            if city not in visited_cities:
                util.add_array_value(util.search_line("visited_cities:"), city)
                util.add_array_value(util.search_line("visited_cities_count:"), "1")
        QMessageBox.information(self, "Success", "All cities successfully visited.")
        self.check_cities()

    def check_dealers(self):
        self.ui.dealerships_text.clear()
        visited_dealers = util.get_array_items(util.search_line("unlocked_dealers:"))
        if not visited_dealers:
            self.ui.dealerships_text.append("No dealerships unlocked yet.")
            return
        for dealer in visited_dealers:
            self.ui.dealerships_text.append(dealer)
        self.ui.dealerships_text.scrollToAnchor(visited_dealers[0])

    def add_all_dealers(self):
        all_cities = self.all_cities()
        visited_dealers = util.get_array_items(util.search_line("unlocked_dealers:"))
        for dealer in self.dealers:
            if dealer in all_cities and dealer not in visited_dealers:
                util.add_array_value(util.search_line("unlocked_dealers:"), dealer)
        QMessageBox.information(self, "Success", "All dealerships unlocked.")
        self.check_dealers()

    def check_agencies(self):
        self.ui.agencies_text.clear()
        visited_agencies = util.get_array_items(util.search_line("unlocked_recruitments:"))
        if not visited_agencies:
            self.ui.agencies_text.append("No recruitment agencies unlocked yet.")
            return
        for agency in visited_agencies:
            self.ui.agencies_text.append(agency)
        self.ui.agencies_text.scrollToAnchor(visited_agencies[0])

    def add_all_agencies(self):
        all_cities = self.all_cities()
        visited_agencies = util.get_array_items(util.search_line("unlocked_recruitments:"))
        for agency in self.agencies:
            if agency in all_cities and agency not in visited_agencies:
                util.add_array_value(util.search_line("unlocked_recruitments:"), agency)
        QMessageBox.information(self, "Success", "All recruitment agencies unlocked.")
        self.check_agencies()

    def da_clicked(self):
        da_arr = self.da_array.get(self.sender())
        if da_arr is None:
            return
        edit, file_var, message_var = da_arr[0], da_arr[1], da_arr[2]
        city_element = edit.text().lower()
        if not city_element:
            QMessageBox.critical(self, "Error", "Enter city name!")
            return
        edit.setText("")
        if city_element not in da_arr[3]:
            QMessageBox.critical(self, "Error", "There is no {} in that city.".format(message_var.lower()))
        elif city_element in util.get_array_items(util.search_line(file_var)):
            QMessageBox.information(self, "Info", "{} in \"{}\" is already unlocked.".format(message_var, city_element))
        else:
            util.add_array_value(util.search_line(file_var), city_element)
            QMessageBox.information(self, "Success", "{} in \"{}\" successfully unlocked."
                                                     "".format(message_var, city_element))
            da_arr[4]()
