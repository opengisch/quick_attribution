# -*- coding: utf-8 -*-
#-----------------------------------------------------------
# Copyright (C) 2017 OPENGIS.ch
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from qgis.PyQt.QtCore import Qt
from AttributesDock import AttributesDock
# from MapLayerProperties import QuickAttributionLayerProperties

def classFactory(iface):
    return QuickAttribution(iface)

class QuickAttribution:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.dockWidget = AttributesDock()
        self.iface.addDockWidget(Qt.RightDockWidgetArea ,self.dockWidget)
        self.iface.currentLayerChanged.connect(self.dockWidget.setLayer)
        self.dockWidget.layerChanged.connect(self.iface.setActiveLayer)

#        self.layerPropertiesFactory = QuickAttributionLayerProperties()
#        self.iface.registerMapLayerConfigWidgetFactory(self.layerPropertiesFactory)

    def unload(self):
        self.iface.removeDockWidget(self.dockWidget)
        del self.dockWidget
#        self.iface.unregisterMapLayerConfigWidgetFactory(self.layerPropertiesFactory)
#        del self.layerPropertiesFactory
