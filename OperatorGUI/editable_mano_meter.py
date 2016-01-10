from taurus.qt.qtgui.gauge import QManoMeter


class EditableManoMeter(QManoMeter):
    def __init__(self, parent):
        super(EditableManoMeter, self).__init__(parent)
        self.model = None

    def setModel(self, model):
        self.model = model

    def setProperScales(self, lower_limits, upper_limits):
        #:TODO: get to know how to do this!
        self._min = int(lower_limits[0])
        self._minimum = int(lower_limits[0])
        self._minimumAlarm = int(lower_limits[1])
        self._minimumWarning = int(lower_limits[2])

        self._max = int(upper_limits[0])
        self._maximum = int(upper_limits[0])
        self._maximumAlarm = int(upper_limits[1])
        self._maximumWarning = int(upper_limits[2])

