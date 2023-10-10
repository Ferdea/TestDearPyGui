import dearpygui.dearpygui as dpg


class NodeBase:
    def __init__(self, label: str):
        self.id = dpg.add_node(label=label, parent='node editor')

    def delete(self):
        dpg.delete_item(self.id)
