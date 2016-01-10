from PyQt4 import Qt
from taurus.qt.qtgui.base import TaurusBaseWidget, TaurusBaseController, \
    TaurusScalarAttributeControllerHelper
from taurus.qt.qtgui.gauge import QManoMeter


class TaurusManoMeterController(TaurusBaseController):
    def __init__(self, manometer):
        self._value = 0
        TaurusBaseController.__init__(self, manometer)
    
    def manometer(self):
        return self.widget()

    def _needsStateConnection(self):
        manometer = self.manometer()
        ret = 'state' in (manometer.fgRole, manometer.bgRole)
        return ret
    
    def _updateForeground(self, manometer):
        fgRole, value = manometer.fgRole, ""
        if fgRole == 'value':
            value += self.getDisplayValue()
        elif fgRole == 'w_value':
            value += self.getDisplayValue(True)
        elif fgRole == 'state':
            stateObj = self.stateObj()
            value += stateObj and stateObj.getDisplayValue() or manometer.getNoneValue()
        elif fgRole == 'quality':
            quality = self.quality()
            if quality is None:
                value += manometer.getNoneValue()
            else:
                value += str(quality)
        elif fgRole in ('', 'none'):
            pass
        else:
            manometer.setValue(0)
            return
        
        self._value = value

        manometer.setValue(value)

    def _updateToolTip(self, manometer):
        if not manometer.getAutoTooltip():
            return
        toolTip = manometer.getFormatedToolTip()
        manometer.setToolTip(toolTip)
        
        
class TaurusManometerControllerAttribute(TaurusScalarAttributeControllerHelper, TaurusManoMeterController):
    def __init__(self, manometer):
        TaurusScalarAttributeControllerHelper.__init__(self)
        TaurusManoMeterController.__init__(self, manometer)
        # manometer = self.manometer()
        # manometer.setDynamicTextInteractionFlags(Qt.Qt.TextSelectableByMouse | Qt.Qt.LinksAccessibleByMouse)


class EditableManoMeter(QManoMeter, TaurusBaseWidget):
    DefaultBgRole = 'quality'
    DefaultFgRole = 'value'

    def __init__(self, parent):
        super(EditableManoMeter, self).__init__(parent)
        super(TaurusBaseWidget, self).__init__(self.__class__.__name__)
        self._controller = None
        self._disconnect_on_hide = True
        self._bgRole = self.DefaultBgRole
        self._fgRole = self.DefaultFgRole
        self._dynamicTextInteractionFlags = True
        self._autoTooltip = ''

    def setProperScales(self, lower_limits, upper_limits):
        self._min = int(lower_limits[0])
        self._minimum = int(lower_limits[0])
        self._minimumAlarm = int(lower_limits[1])
        self._minimumWarning = int(lower_limits[2])

        self._max = int(upper_limits[0])
        self._maximum = int(upper_limits[0])
        self._maximumAlarm = int(upper_limits[1])
        self._maximumWarning = int(upper_limits[2])

    def _calculate_controller_class(self):
        # ctrl_map = _CONTROLLER_MAP
        # if self._designMode:
        #     ctrl_map = _DESIGNER_CONTROLLER_MAP
        # model_type = self.getModelType()
        # ctrl_klass = ctrl_map.get(model_type, TaurusLabelController)
        ctrl_klass = TaurusManometerControllerAttribute
        return ctrl_klass

    def controller(self):
        ctrl = self._controller
        # if there is a controller object and it is not the base controller...
        if ctrl is not None and not ctrl.__class__ == TaurusManoMeterController:
            return ctrl

        # if there is a controller object and it is still the same class...
        ctrl_klass = self._calculate_controller_class()
        if ctrl_klass is None:
            return None
        elif ctrl.__class__ == ctrl_klass:
            return ctrl

        self._controller = ctrl = ctrl_klass(self)
        return ctrl

    def controllerUpdate(self):
        ctrl = self.controller()
        if ctrl is not None:
            ctrl.update()

    def handleEvent(self, evt_src, evt_type, evt_value):
        ctrl = self.controller()
        if ctrl is not None:
            ctrl.handleEvent(evt_src, evt_type, evt_value)

    def isReadOnly(self):
        return True

    def setModel(self, m):
        #force to build another controller
        self._controller = None
        TaurusBaseWidget.setModel(self, m)

    def getBgRole(self):
        return self._bgRole

    def setBgRole(self, bgRole):
        self._bgRole = str(bgRole).lower()
        self.controllerUpdate()

    def resetBgRole(self):
        self.setBgRole(self.DefaultBgRole)

    def getFgRole(self):
        return self._fgRole

    def setFgRole(self, fgRole):
        self._fgRole = str(fgRole).lower()
        self.controllerUpdate()

    def resetFgRole(self):
        self.setFgRole(self.DefaultFgRole)

    def setDynamicTextInteractionFlags(self, flags):
        if self.hasDynamicTextInteractionFlags():
            Qt.QLabel.setTextInteractionFlags(self, flags)

    def hasDynamicTextInteractionFlags(self):
        return self._dynamicTextInteractionFlags

    def setTextInteractionFlags(self, flags):
        Qt.QLabel.setTextInteractionFlags(self, flags)
        self._dynamicTextInteractionFlags = False

    def resetTextInteractionFlags(self):
        Qt.QLabel.resetTextInteractionFlags(self)
        self.dynamicTextInteractionFlags = True


    #: This property holds the unique URI string representing the model name
    #: with which this widget will get its data from. The convention used for
    #: the string can be found :ref:`here <model-concept>`.
    #:
    #: In case the property :attr:`useParentModel` is set to True, the model
    #: text must start with a '/' followed by the attribute name.
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`TaurusBaseWidget.getModel`
    #:     * :meth:`TaurusLabel.setModel`
    #:     * :meth:`TaurusBaseWidget.resetModel`
    #:
    #: .. seealso:: :ref:`model-concept`

    model = Qt.pyqtProperty("QString", TaurusBaseWidget.getModel, setModel,
                            TaurusBaseWidget.resetModel)

    #: This property holds the foreground role (the text).
    #: Valid values are:
    #:
    #:     #. ''/'None' - no value is displayed
    #:     #. 'value' - the value is displayed
    #:     #. 'w_value' - the write value is displayed
    #:     #. 'quality' - the quality is displayed
    #:     #. 'state' - the device state is displayed
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`TaurusLabel.getFgRole`
    #:     * :meth:`TaurusLabel.setFgRole`
    #:     * :meth:`TaurusLabel.resetFgRole`
    fgRole = Qt.pyqtProperty("QString", getFgRole, setFgRole,
                             resetFgRole, doc="foreground role")

    #: This property holds the background role.
    #: Valid values are ''/'None', 'quality', 'state'
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`TaurusLabel.getBgRole`
    #:     * :meth:`TaurusLabel.setBgRole`
    #:     * :meth:`TaurusLabel.resetBgRole`
    bgRole = Qt.pyqtProperty("QString", getBgRole, setBgRole,
                             resetBgRole, doc="background role")

    #: This property holds the
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`TaurusLabel.isDragEnabled`
    #:     * :meth:`TaurusLabel.setDragEnabled`
    #:     * :meth:`TaurusLabel.resetDragEnabled`
    dragEnabled = Qt.pyqtProperty("bool", TaurusBaseWidget.isDragEnabled,
                                  TaurusBaseWidget.setDragEnabled,
                                  TaurusBaseWidget.resetDragEnabled,
                                  doc="enable dragging")

    #: Specifies how the label should interact with user input if it displays
    #: text.
    #:
    #: **Access functions:**
    #:
    #:     * :meth:`TaurusLabel.textInteractionFlags`
    #:     * :meth:`TaurusLabel.setTextInteractionFlags`
    #:     * :meth:`TaurusLabel.resetTextInteractionFlags
    try:
        textInteractionFlags = Qt.pyqtProperty(Qt.Qt.TextInteractionFlag,
                                   Qt.QLabel.textInteractionFlags,
                                   setTextInteractionFlags,
                                   resetTextInteractionFlags,
                                   doc="Specifies how the label should interact with user input if it displays text.")
    except TypeError: #Old PyQt4 version only accept strings for the type arg
        textInteractionFlags = Qt.pyqtProperty("int",
                                   Qt.QLabel.textInteractionFlags,
                                   setTextInteractionFlags,
                                   resetTextInteractionFlags,
                                   doc="Specifies how the label should interact with user input if it displays text.")

