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
    QgsAttributeEditorContext
)
from qgis.core import (
    QgsExpression,
    QgsMapLayer,
    QgsFeature,
    QgsMapLayerProxyModel,
    QgsProject
)
from qgis.PyQt.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QSizePolicy
)
from qgis.PyQt.QtCore import pyqtSignal

class AttributesDock(QgsDockWidget):
    layerChanged = pyqtSignal(QgsMapLayer)

    def __init__(self, iface):
        QgsDockWidget.__init__(self)
        self.iface = iface
        self.widget = QWidget()
        self.widget.setLayout(QGridLayout())
        self.layerComboBox = QgsMapLayerComboBox()
        self.layerComboBox.layerChanged.connect(self.setLayer)
        self.layerTitleLabel = QLabel()
        self.widget.layout().addWidget(self.layerTitleLabel, 0, 0, 1, 1)
        self.widget.layout().addWidget(self.layerComboBox, 0, 1, 1, 1)
        self.formWidget = QWidget()
        self.formWidget.setLayout(QGridLayout())
        self.widget.layout().addWidget(self.formWidget, 1, 0, 1, 2)
        self.setWidget(self.widget)
        self.attributeForm = None
        self.layer = None

        self.layerComboBox.setFilters(
            QgsMapLayerProxyModel.WritableLayer | QgsMapLayerProxyModel.VectorLayer)

        QgsProject.instance().readProject.connect(self.onProjectRead)

    def setLayer(self, layer):
        if layer == self.layer:
            return
        if self.layer:
            self.layer.destroyed.disconnect(self.onLayerRemoved)
        self.layer = layer
        if self.layer:
            self.layer.destroyed.connect(self.onLayerRemoved)
        self.layerComboBox.setLayer(layer)
        if self.attributeForm:
            try:
                self.attributeForm.deleteLater()
            except RuntimeError:
                # Sometimes the form has already been deleted, that's ok for us
                pass
        if self.layer:
            context = QgsAttributeEditorContext()
            context.setVectorLayerTools(self.iface.vectorLayerTools())
            context.setFormMode(QgsAttributeEditorContext.StandaloneDialog)
            self.attributeForm = QgsAttributeForm(self.layer, QgsFeature(), context)
            self.attributeForm.hideButtonBox()
            try:
                self.layer.updatedFields.disconnect(
                    self.attributeForm.onUpdatedFields)
            except TypeError:
                pass
            fields = self.layer.fields()
            self.feature = QgsFeature(fields)
            for idx in range(self.layer.fields().count()):
                self.feature.setAttribute(idx, self.layer.defaultValue(idx))
            self.feature.setValid(True)
            self.attributeForm.setFeature(self.feature)
            self.attributeForm.attributeChanged.connect(
                self.onAttributeChanged)
            self.formWidget.layout().addWidget(self.attributeForm)
            self.layerChanged.emit(self.layer)

    def onLayerRemoved(self):
        self.setLayer(None)

    def onAttributeChanged(self, attributeName, value):
        idx = self.layer.fieldNameIndex(attributeName)
        self.layer.blockSignals(True)
        self.layer.setDefaultValueExpression(
            idx, QgsExpression.quotedValue(value))
        self.layer.blockSignals(False)

    def onProjectRead(self, doc):
        title, isDefined = QgsProject.instance().readEntry('quick_attribution', 'layercbxtitle')
        if isDefined:
            self.layerTitleLabel.setText(title)
        else:
            self.layerTitleLabel.setText(self.tr('Layer'))
