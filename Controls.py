# pylint has troubles importing from gi.repository because
# it uses introspection
# pylint: disable=E0611
#from gi.repository import GLib
from gi.repository import Gtk
# pylint: disable=F0401
from gi.repository.Gtk import SizeGroupMode
from gi.repository import Gdk

from reportclient import _
from froslogging import info, warn
import os


class Controls(Gtk.Window):
    #  selected plugin
    controller = None

    def __init__(self, controller):
        Gtk.Window.__init__(self)
        self.controller = controller
        buttons_size_group = Gtk.SizeGroup(SizeGroupMode.BOTH)
        main_vbox = Gtk.VBox()
        main_hbox = Gtk.HBox()
        # pylint: disable=E1101
        self.add(main_vbox)
        # pylint: disable=E1101
        self.set_decorated(False)

        # move away from the UI!
        self.wroot = Gdk.get_default_root_window()
        self.wwidth = self.wroot.get_width()
        self.wheight = self.wroot.get_height()

        #progress bar
        self.progress = Gtk.ProgressBar()
        self.progress.set_no_show_all(True)

        #stop button
        self.stop_button = Gtk.Button(stock=Gtk.STOCK_MEDIA_STOP)
        self.stop_button.connect("clicked", self.__stop_recording__)
        self.stop_button.set_sensitive(False)
        buttons_size_group.add_widget(self.stop_button)
        main_hbox.pack_start(self.stop_button, False, False, 0)

        #start button
        rec_button = Gtk.Button(stock=Gtk.STOCK_MEDIA_RECORD)
        rec_button.connect("clicked", self.__start_recording__, self.stop_button)
        # have to select window first
        rec_button.set_sensitive(False)
        buttons_size_group.add_widget(rec_button)
        main_hbox.pack_start(rec_button, False, False, 0)

        # select button
        select_button = Gtk.Button(_("Select window"))
        select_button.connect("clicked", self.controller.SelectArea, None)
        buttons_size_group.add_widget(select_button)
        main_hbox.pack_start(select_button, False, False, 0)

        # close button
        close_button = Gtk.Button(stock=Gtk.STOCK_CLOSE)
        close_button.connect("clicked", Gtk.main_quit)
        buttons_size_group.add_widget(close_button)
        main_hbox.pack_start(close_button, False, False, 0)

        main_vbox.pack_start(main_hbox, True, True, 0)
        main_vbox.pack_start(self.progress, True, True, 0)

        self.connect("destroy", Gtk.main_quit)

    def __stop_recording__(self):
        print "Stop recording:"

    def __start_recording__(self, button):
        print "start recording"
        button.set_sensitive(False)
        self.stop_button.set_sensitive(True)
