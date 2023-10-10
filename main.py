import dearpygui.dearpygui as dpg
from nodes.video_node import VideoNode, update_video

dpg.create_context()


def callback(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)


def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)


with dpg.file_dialog(
        directory_selector=False, show=False, callback=callback, tag='file_dialog_id',
        cancel_callback=cancel_callback, width=700, height=400):
    dpg.add_file_extension('.mp4', color=(100, 150, 200))
    dpg.add_file_extension('.mov', color=(200, 100, 150))


def link_callback(sender, app_data):
    dpg.add_node_link(app_data[0], app_data[1], parent=sender)


def delink_callback(sender, app_data):
    dpg.delete_item(app_data)


def create_node(sender):
    VideoNode()


def video_editor_window_resize(sender, app_data, user_data):
    width = dpg.get_item_width(app_data)
    height = dpg.get_item_height(app_data)
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    dpg.set_item_width(user_data, viewport_width - width)
    dpg.set_item_height(user_data, viewport_height)
    dpg.set_item_pos(user_data, [width, 0])


def video_preview_window_resize(sender, app_data, user_data):
    width = dpg.get_item_width(app_data)
    height = dpg.get_item_height(app_data)
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    dpg.set_item_width(user_data, viewport_width - width)
    dpg.set_item_height(user_data, viewport_height)
    dpg.set_item_pos(user_data, [0, 0])


texture_data = []
for i in range(0, 100 * 100):
    texture_data.append(255 / 255)
    texture_data.append(0)
    texture_data.append(255 / 255)

with dpg.texture_registry(show=True):
    dpg.add_raw_texture(width=100, height=100, default_value=texture_data, tag="video preview image",
                        format=dpg.mvFormat_Float_rgb)

with dpg.window(label='Video Editor', width=550, height=600, pos=(0, 0), no_move=True, tag='video editor',
                no_close=True, no_collapse=True) as video_editor:
    with dpg.menu_bar():
        with dpg.menu(label="Node"):
            dpg.add_menu_item(label="Create new node", callback=create_node)

    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, tag='node editor'):
        pass

    with dpg.item_handler_registry(label='Editor Handler', tag='editor handler'):
        dpg.add_item_resize_handler(label='resize handler', user_data='video preview',
                                    callback=video_editor_window_resize)

    dpg.bind_item_handler_registry(video_editor, handler_registry='editor handler')

with dpg.window(label='Video Preview', width=250, height=600, pos=(550, 0), no_move=True, tag='video preview',
                no_close=True, no_collapse=True) as video_preview:
    with dpg.item_handler_registry(label='Preview Handler', tag='preview handler'):
        dpg.add_item_resize_handler(label='resize handler', user_data='video editor',
                                    callback=video_preview_window_resize)

    dpg.bind_item_handler_registry(video_preview, handler_registry='preview handler')


def resize_callback(sender, app_data):
    width, height = app_data[0], app_data[1]
    dpg.set_item_width(video_editor, width * 0.7)
    dpg.set_item_height(video_editor, height)
    dpg.set_item_pos(video_preview, [0, 0])

    dpg.set_item_width(video_preview, width * 0.3)
    dpg.set_item_height(video_preview, height)
    dpg.set_item_pos(video_preview, [width * 0.7, 0])
    print(width, height)


dpg.set_viewport_resize_callback(resize_callback)
dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    update_video()
    dpg.render_dearpygui_frame()
dpg.start_dearpygui()
dpg.destroy_context()
