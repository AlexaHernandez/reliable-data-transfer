from PyQt4 import QtCore
from Core.Device import *

class Switch(Device):
    device_type = "Switch"

    def __init__(self):
        Device.__init__(self)
        self.setProperty("Hub mode", "False")
        self.setProperty("OVS mode", "False")
        self.setProperty("Priority", "100")
        self.setProperty("mac", "")
#       self.setProperty("mask", "")
#       self.setProperty("subnet", "")
#       self.setProperty("link_subnet", "0")
#       self.setProperty("port", "")
#       self.setProperty("monitor", "")
        self.gateway = None

    def addEdge(self, edge):
        Device.addEdge(self, edge)

        node = edge.getOtherDevice(self)
        if node.device_type == "Mach":
            node.addInterface(self)
        elif node.device_type == "Router":
            node.addInterface(self)

    def removeEdge(self, edge):
        Device.removeEdge(self, edge)

        node = edge.getOtherDevice(self)
        if node.device_type == "Mach":
            node.removeInterface(self)
        elif node.device_type == "Router":
            node.removeInterface(self)

    def getGateway(self):
        return self.gateway[QtCore.QString("ipv4")]

    """
    If the switch is connected to a subnet, return the opposite node
    to which that subnet is connected, if any
    """
    def getTarget(self, node):
        for con in self.edges():
            other = con.getOtherDevice(self)
            if other != node and other.device_type == "Subnet":
                return other.getTarget(self)
