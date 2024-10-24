#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
        QDialog.__init__(self, parent, flags=(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint))
        Ui_SecondWindow.__init__(self)
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self)

        self.owns = owns_list  # From main window

        # Checking config files
        cfg_path = "configs/{}".format(selected_game)
        dealers_path = "{}/dealers.json".format(cfg_path)
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

        agencies_path = "{}/agencies.json".format(cfg_path)
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

        self.da_statics = {
            "dealer": [
                self.dealers, # city_list
                "unlocked_dealers:", # line_to_search
                self.check_dealers, # check_func
            ],
            "agency": [
                self.agencies, # city_list
                "unlocked_recruitments:", # line_to_search
                self.check_agencies, # check_func
            ],
        }

        self.add_da_handlers = {
            self.ui.dealer_add: [
                "dealer",
                self.ui.dealer_edit, # city_to_add
                "Dealership", # message_variable
            ],
            self.ui.dealer_add_all: [
                "dealer",
                "All dealerships unlocked.", # success_message
                "Visiting dealers", # progress_message
            ],
            self.ui.agency_add: [
                "agency",
                self.ui.agency_edit, # city_to_add
                "Recruitment agency", # message_variable
            ],
            self.ui.agency_add_all: [
                "agency",
                "All recruitment agencies unlocked.", # success_message
                "Visiting agencies", # progress_message
            ],
        }

        # Connecting buttons
        self.ui.garages_analyze.clicked.connect(self.check_garages)
        self.ui.garage_add.clicked.connect(self.add_garage)
        self.ui.garage_add_all.clicked.connect(self.add_all_garages)
        self.ui.headquarter_change.clicked.connect(self.change_headquarter)
        self.ui.city_add.clicked.connect(self.add_city)
        self.ui.city_add_all.clicked.connect(self.add_all_cities)
        self.ui.dealer_add.clicked.connect(self.add_da_clicked)
        self.ui.agency_add.clicked.connect(self.add_da_clicked)
        self.ui.dealer_add_all.clicked.connect(self.add_all_da_clicked)
        self.ui.agency_add_all.clicked.connect(self.add_all_da_clicked)

        if self.owns:
            self.fill_list(self.owns, self.dealers, self.dealers_file)
            self.fill_list(self.owns, self.agencies, self.agencies_file)

        # Checking save-file
        self.check_cities()
        self.check_dealers()
        self.check_agencies()

    @staticmethod
    def all_cities():
        cities = []
        for line in util.get_array_items(util.search_line("companies:")):
            city = match(r"company.volatile.[a-z0-9_]+[.]([a-z_]+)", line).group(1)
            if city not in cities:
                cities.append(city)
        return cities

    @staticmethod
    def add_vehicles_and_drivers(start_line, garage_size):
        vehicles_array = util.search_line("vehicles:", start=start_line)
        drivers_array = util.search_line("drivers:", start=start_line)
        for i in range(1, garage_size + 1):
            util.add_array_value(vehicles_array, "null")
            util.add_array_value(drivers_array + i, "null")

    @staticmethod
    def purchased_garages():
        garages = []
        for index in util.search_all_lines("garage : garage."):
            city = match(r"garage : garage.(.+) {$", util.get_lines(index)).group(1)
            if util.get_value(util.search_line("status:", start=index)) != "0":
                garages.append(city)
        return garages

    @staticmethod
    def fill_list(owns, array, file):
        if array is False:
            return
        for key in owns.keys():
            if key not in file:
                continue
            for value in file[key]:
                array.append(value)

    def check_garage_size(self):
        status_id, size = garages_stat[self.ui.garage_size.currentText()]
        return str(status_id), size

    def check_garages(self):
        self.ui.garages_text.clear()
        garages = self.purchased_garages()
        for garage in garages:
            self.ui.garages_text.append(garage)
        self.ui.garages_text.scrollToAnchor(garages[0])

    def add_garage(self):
        garage = self.ui.garage_edit.text().lower()
        if garage == "":
            QMessageBox.critical(self, "Error", "Enter city name!")
            return
        self.ui.garage_edit.setText("")
        current_garage = util.search_line("garage : garage." + garage + " {")
        if current_garage is None:
            QMessageBox.critical(self, "Error", "Garage in \"{}\" not found.".format(garage))
            return
        current_status = util.search_line_in_unit("status:", "garage." + garage)
        if util.get_value(current_status) == "0":
            new_status, size = self.check_garage_size()
            util.set_value(current_status, new_status)
            self.add_vehicles_and_drivers(current_garage, size)
            QMessageBox.information(self, "Success", "Garage in \"{}\" successfully unlocked.".format(garage))
        else:
            QMessageBox.critical(self, "Error", "Garage in \"{}\" already unlocked.".format(garage))

    def add_all_garages(self):
        new_status, size = self.check_garage_size()
        for item in util.get_array_items(util.search_line("garages:")):
            item = match(r"garage.(.+)$", item).group(1)
            current_garage = util.search_line("garage : garage." + item + " {")
            current_status = util.search_line("status:", start=current_garage)
            if util.get_value(current_status) == "0":
                util.set_value(current_status, new_status)
                self.add_vehicles_and_drivers(current_garage, size)
        QMessageBox.information(self, "Success", "All garages successfully unlocked.")

    def change_headquarter(self):
        hq = self.ui.headquarter_edit.text().lower()
        if hq == "":
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
        if city == "":
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
        all_cities = self.all_cities()
        visited_cities = util.get_array_items(util.search_line("visited_cities:"))
        progress = util.show_progress_bar("Visiting cities", "Visiting cities...", len(all_cities)-len(visited_cities))
        for city in all_cities:
            if city not in visited_cities:
                util.add_array_value(util.search_line("visited_cities:"), city)
                util.add_array_value(util.search_line("visited_cities_count:"), "1")
                util.update_progress_bar(progress)
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

    def check_agencies(self):
        self.ui.agencies_text.clear()
        visited_agencies = util.get_array_items(util.search_line("unlocked_recruitments:"))
        if not visited_agencies:
            self.ui.agencies_text.append("No recruitment agencies unlocked yet.")
            return
        for agency in visited_agencies:
            self.ui.agencies_text.append(agency)
        self.ui.agencies_text.scrollToAnchor(visited_agencies[0])

    def add_da_clicked(self):
        da_arr = self.add_da_handlers.get(self.sender())
        if da_arr is None:
            return
        static_key, city_to_add, message_variable = da_arr
        city_list, line_to_search, check_func = self.da_statics.get(static_key)
        city_element = city_to_add.text().lower()
        if not city_element:
            QMessageBox.critical(self, "Error", "Enter city name!")
            return
        city_to_add.setText("")
        if city_element not in city_list:
            QMessageBox.critical(self, "Error", "There is no {} in that city.".format(message_variable.lower()))
        elif city_element in util.get_array_items(util.search_line(line_to_search)):
            QMessageBox.information(self, "Info", "{} in \"{}\" is already unlocked.".format(message_variable,
                                                                                             city_element))
        else:
            util.add_array_value(util.search_line(line_to_search), city_element)
            QMessageBox.information(self, "Success", "{} in \"{}\" successfully unlocked."
                                                     "".format(message_variable, city_element))
            check_func()

    def add_all_da_clicked(self):
        da_arr = self.add_da_handlers.get(self.sender())
        if da_arr is None:
            return
        static_key, success_message, progress_message = da_arr
        city_list, line_to_search, check_func = self.da_statics.get(static_key)
        all_cities = self.all_cities()
        array_line = util.search_line(line_to_search)
        visited_cities = util.get_array_items(array_line)
        progress = util.show_progress_bar(progress_message, progress_message+"...", len(all_cities)-len(visited_cities))
        for element in city_list:
            if (element in all_cities) and (element not in visited_cities):
                util.add_array_value(array_line, element)
                util.update_progress_bar(progress)
        QMessageBox.information(self, "Success", success_message)
        check_func()
