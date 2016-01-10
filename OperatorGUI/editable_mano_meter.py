from taurus.qt.qtgui.gauge import QManoMeter


class EditableManoMeter(QManoMeter):
    def __init__(self, parent):
        super(EditableManoMeter, self).__init__(parent)

    def setProperScales(self, lower_limits, upper_limits):
        pass
        #:TODO: get to know how to do this!
