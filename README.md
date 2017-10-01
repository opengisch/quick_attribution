# QGIS Quick Attribution Plugin

When digitizing a lot of features with identical attributes, this is the way to go.

It will show an attribute form in a dock widget next to the map canvas. These attributes will then be used when you digitize new features even when the feature form is suppressed.

![Sample](https://github.com/opengisch/quick_attribution/raw/master/doc/sample.png)

## Configure project

1. Disable the attribute form on layers on which you want to digitize quickly. Go to layer properties -> Fields and set "Suppress attribute form pop-up after feature creation" to "On".

2. Set all layers to read only which you do not want to appear in the list of editable layers. This can be done in project properties -> Identify Layers.

