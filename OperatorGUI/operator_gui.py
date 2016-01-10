from PyQt4 import QtCore, QtGui
import sys
from PyTango import AttributeProxy
from taurus.qt.qtgui.container import TaurusMainWindow
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.input import TaurusValueLineEdit

from editable_mano_meter import EditableManoMeter


class UiMainWindow(TaurusMainWindow):
    def __init__(self, motors_list):
        super(UiMainWindow, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                           QtGui.QSizePolicy.MinimumExpanding)
        self.central_widget = QtGui.QWidget(self)
        self.gridLayout = QtGui.QGridLayout(self.central_widget)
        self.gridLayout.setMargin(0)

        self.motor_widgets_list = []
        self.motor_widgets_layout = QtGui.QGridLayout(self.central_widget)
        self.motors_widget = QtGui.QWidget(self.central_widget)
        self.motors_widget.setLayout(self.motor_widgets_layout)
        self.gridLayout.addWidget(self.motors_widget, 0, 0)
        for i, motor in enumerate(motors_list):
            widget = self.get_one_motor_widget(motor)
            self.motor_widgets_layout.addWidget(widget, i / 2, i % 2)
            self.motor_widgets_list.append(widget)

        self.setCentralWidget(self.central_widget)
        self.menu_bar = QtGui.QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.status_bar = QtGui.QStatusBar(self)
        self.setStatusBar(self.status_bar)

    def get_one_motor_widget(self, name):
        widget = QtGui.QWidget(self.central_widget)
        layout = QtGui.QGridLayout(widget)

        motor_name = QtGui.QLabel(widget)
        motor_name.setText(name)
        layout.addWidget(motor_name, 0, 0)

        taurus_led = TaurusLed(widget)
        taurus_led.setMaximumSize(QtCore.QSize(50, 50))
        taurus_led.setMinimumSize(QtCore.QSize(30, 30))
        taurus_led.setModel(name + '/State')
        layout.addWidget(taurus_led, 0, 1)

        taurus_label = TaurusLabel(widget)
        taurus_label.setModel(name + '/Status')
        taurus_label.setMinimumSize(QtCore.QSize(260, 140))
        layout.addWidget(taurus_label, 1, 0, 2, 2)

        taurus_mano = EditableManoMeter(widget)
        taurus_mano.setMaximumSize(QtCore.QSize(500, 500))
        l_lim, u_lim = self.get_limits(name + '/Position')
        taurus_mano.setProperScales(l_lim, u_lim)
        taurus_mano.setModel(name + '/Position')
        layout.addWidget(taurus_mano, 0, 2, 2, 1)

        taurus_line_edit = TaurusValueLineEdit(widget)
        taurus_line_edit.setModel(name + "/Position")
        layout.addWidget(taurus_line_edit, 2, 2)

        limit_switches_label = QtGui.QLabel(widget)
        limit_switches_label.setText('Limit switches:')
        layout.addWidget(limit_switches_label, 0, 3, 1, 2)

        lower_limit_switch = TaurusLed(widget)
        lower_limit_switch.setModel(name + 'Limit_switches')
        lower_limit_switch.setModelIndex('1')
        lower_limit_switch.setMinimumSize(QtCore.QSize(30, 30))
        lower_limit_switch.setMaximumSize(QtCore.QSize(50, 50))
        layout.addWidget(lower_limit_switch, 1, 3)

        widget.setLayout(layout)

        return widget

    @staticmethod
    def get_limits(attrib_name):
        attr_proxy = AttributeProxy(attrib_name)
        attr_config = attr_proxy.get_config()
        lower_limit = attr_config.min_value
        upper_limit = attr_config.max_value
        lower_warning = attr_config.alarms.min_warning
        upper_warning = attr_config.alarms.max_warning
        lower_alarm = attr_config.alarms.min_alarm
        upper_alarm = attr_config.alarms.max_alarm
        return [lower_limit, lower_alarm, lower_warning], [upper_limit,
                                                           upper_alarm,
                                                           upper_warning]


def main():
    app = TaurusApplication()
    motors_list = ['motor/motctrl01/1',
                   'motor/motctrl01/2',
                   'motor/motctrl01/3',
                   'motor/motctrl01/4']
    main_window = UiMainWindow(motors_list)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
