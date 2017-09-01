# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Copyright (C) 2017 OPENGIS.ch
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------

from qgis.gui import (
    QgsDockWidget,
    QgsAttributeForm,
    QgsMapLayerComboBox,
    QgsMapLayerProxyModel
)
from qgis.core import (
    QgsExpression,
    QgsMapLayer,
    QgsMapLayerRegistry,
    QgsFeature
)
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtGui import QGridLayout
from qgis.PyQt.QtCore import pyqtSignal


class AttributesDock(QgsDockWidget):
    layerChanged = pyqtSignal(QgsMapLayer)

    def __init__(self):
        QgsDockWidget.__init__(self)
        self.widget = QWidget()
        self.widget.setLayout(QGridLayout())
        self.layerComboBox = QgsMapLayerComboBox()
        self.layerComboBox.layerChanged.connect(self.setLayer)
        self.widget.layout().addWidget(self.layerComboBox)
        self.formWidget = QWidget()
        self.formWidget.setLayout(QGridLayout())
        self.widget.layout().addWidget(self.formWidget)
        self.setWidget(self.widget)
        self.attributeForm = None
        self.layer = None

        self.layerComboBox.setFilters(QgsMapLayerProxyModel.WritableLayer | QgsMapLayerProxyModel.VectorLayer)

    def setLayer(self, layer):
        if layer == self.layer:
            return
        self.layer = layer
        self.layerComboBox.setLayer(layer)
        if self.attributeForm:
            self.attributeForm.deleteLater()
        self.attributeForm = QgsAttributeForm(layer)
        try:
            self.layer.updatedFields.disconnect(self.attributeForm.onUpdatedFields)
        except TypeError:
            pass
        fields = self.layer.fields()
        self.feature = QgsFeature(fields)
        for idx in range(self.layer.fields().count()):
            self.feature.setAttribute(idx, layer.defaultValue(idx))
        self.feature.setValid(True)
        self.attributeForm.setFeature(self.feature)
        self.attributeForm.attributeChanged.connect(self.onAttributeChanged)
        self.formWidget.layout().addWidget(self.attributeForm)
        self.layerChanged.emit(self.layer)

    def onAttributeChanged(self, attributeName, value):
        idx = self.layer.fieldNameIndex(attributeName)
        self.layer.blockSignals(True)
        self.layer.setDefaultValueExpression(idx, QgsExpression.quotedValue(value))
        self.layer.blockSignals(False)
