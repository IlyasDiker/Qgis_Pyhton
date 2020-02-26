from PyQt4.QtCore import Qt
from qgis.gui import QgsMapTool
from qgis.utils import iface

class SendPointToolCoordinates(QgsMapTool):

    def __init__(self, canvas, layer):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.layer = layer
        self.setCursor(Qt.CrossCursor)

    def canvasReleaseEvent(self, event):
        point = self.toLayerCoordinates(self.layer, event.pos())

        print(point.x(), point.y())

layer, canvas = iface.activeLayer(), iface.mapCanvas()

send_point_tool_coordinates = SendPointToolCoordinates(
    canvas,
    layer
)
canvas.setMapTool(send_point_tool_coordinates)