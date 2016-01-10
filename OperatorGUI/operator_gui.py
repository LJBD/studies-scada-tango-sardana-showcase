from PyQt4 import QtCore, QtGui

import sys
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.qt.qtgui.gauge import QManoMeter
from taurus.qt.qtgui.application import TaurusApplication


class UiMainWindow(QtGui.QMainWindow):
    def __init__(self, motors_list):
        super(UiMainWindow, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                           QtGui.QSizePolicy.MinimumExpanding)
        self.central_widget = QtGui.QWidget(self)
        self.gridLayout = QtGui.QGridLayout(self.central_widget)
        self.gridLayout.setMargin(0)

        self.motor_widgets_list = []
        self.motor_widgets_layout = QtGui.QVBoxLayout(self.central_widget)
        self.motors_widget = QtGui.QWidget(self.central_widget)
        self.motors_widget.setLayout(self.motor_widgets_layout)
        self.gridLayout.addWidget(self.motors_widget, 0, 0)
        for motor in motors_list:
            widget = self.get_one_motor_widget(motor)
            self.motor_widgets_layout.addWidget(widget)
            self.motor_widgets_list.append(widget)

        # self.taurusLed_mot02 = TaurusLed(self.central_widget)
        # self.taurusLed_mot02.setMaximumSize(QtCore.QSize(30, 30))
        # self.gridLayout.addWidget(self.taurusLed_mot02, 1, 1, 1, 1)
        # self.taurusLed_mot03 = TaurusLed(self.central_widget)
        # self.taurusLed_mot03.setMaximumSize(QtCore.QSize(30, 30))
        # self.gridLayout.addWidget(self.taurusLed_mot03, 2, 1, 1, 1)
        # self.taurusLed_mot04 = TaurusLed(self.central_widget)
        # self.gridLayout.addWidget(self.taurusLed_mot04, 3, 1, 1, 1)
        # self.qManoMeter_mot03 = QManoMeter(self.central_widget)
        # self.qManoMeter_mot03.setMaximumSize(QtCore.QSize(100, 100))
        # self.gridLayout.addWidget(self.qManoMeter_mot03, 2, 0, 1, 1)
        # self.taurusLabel_2 = TaurusLabel(self.central_widget)
        # self.taurusLabel_2.setMaximumSize(QtCore.QSize(300, 20))
        # self.gridLayout.addWidget(self.taurusLabel_2, 1, 2, 1, 1)
        # self.qManoMeter_mot01 = QManoMeter(self.central_widget)
        # self.qManoMeter_mot01.setMaximumSize(QtCore.QSize(100, 100))
        # self.gridLayout.addWidget(self.qManoMeter_mot01, 0, 0, 1, 1)
        # self.taurusLed_mot01 = TaurusLed(self.central_widget)
        # self.gridLayout.addWidget(self.taurusLed_mot01, 0, 1, 1, 1)
        # self.taurusLabel = TaurusLabel(self.central_widget)
        # self.taurusLabel.setMaximumSize(QtCore.QSize(300, 20))
        # self.gridLayout.addWidget(self.taurusLabel, 0, 2, 1, 1)
        # self.qManoMeter_mot02 = QManoMeter(self.central_widget)
        # self.qManoMeter_mot02.setMaximumSize(QtCore.QSize(100, 100))
        # self.gridLayout.addWidget(self.qManoMeter_mot02, 1, 0, 1, 1)
        # self.qManoMeter_mot04 = QManoMeter(self.central_widget)
        # self.qManoMeter_mot04.setMaximumSize(QtCore.QSize(100, 100))
        # self.gridLayout.addWidget(self.qManoMeter_mot04, 3, 0, 1, 1)
        # self.taurusLabel_3 = TaurusLabel(self.central_widget)
        # self.taurusLabel_3.setMaximumSize(QtCore.QSize(300, 20))
        # self.gridLayout.addWidget(self.taurusLabel_3, 2, 2, 1, 1)
        # self.taurusLabel_4 = TaurusLabel(self.central_widget)
        # self.taurusLabel_4.setMaximumSize(QtCore.QSize(300, 20))
        # self.gridLayout.addWidget(self.taurusLabel_4, 3, 2, 1, 1)

        self.setCentralWidget(self.central_widget)
        self.menubar = QtGui.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def get_one_motor_widget(self, name):
        widget = QtGui.QWidget(self.central_widget)
        layout = QtGui.QGridLayout(widget)

        motor_name = QtGui.QLabel(widget)
        motor_name.setText(name)
        layout.addWidget(motor_name, 0, 0)

        taurus_led = TaurusLed(widget)
        taurus_led.setMaximumSize(QtCore.QSize(30, 30))
        taurus_led.setModel(name + '/State')
        print 'LED MODEL:', taurus_led.model
        layout.addWidget(taurus_led, 0, 1)

        taurus_label = TaurusLabel(widget)
        taurus_label.setModel(name + '/Status')
        layout.addWidget(taurus_label, 1, 0, 1, 2)

        taurus_mano = QManoMeter(widget)
        taurus_mano.setMaximumSize(QtCore.QSize(200, 200))
        #:TODO: Get limits for mano.
        layout.addWidget(taurus_mano, 0, 2, 2, 1)

        widget.setLayout(layout)

        return widget

def main():
    app = TaurusApplication()
    motors_list = ['motor/motctl01/1',
                   'motor/motctl01/2',
                   'motor/motctl01/3',
                   'motor/motctl01/4']
    main_window = UiMainWindow(motors_list)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
