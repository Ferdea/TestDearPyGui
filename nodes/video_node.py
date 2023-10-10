import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip

from nodes.node_base import NodeBase
import dearpygui.dearpygui as dpg

current_texture_count = 0
video_clip = None
current_frame = 0


def is_active_video_node(sender, app_data, user_data):
    global video_clip, current_frame, current_texture_count
    print(user_data)
    current_texture_count += 1

    frame = user_data.get_frame(0)
    data = np.asfarray(frame.ravel(), dtype='f')
    texture_data = np.true_divide(data, 255.0)

    dpg.delete_item('video preview image')

    with dpg.texture_registry(show=True):
        dpg.add_raw_texture(width=frame.shape[1], height=frame.shape[0], default_value=texture_data,
                            tag=f'video preview image {current_texture_count}', format=dpg.mvFormat_Float_rgb)

    dpg.add_image(f'video preview image {current_texture_count}', parent='video preview', tag='video preview image')

    video_clip = user_data
    current_frame = 0    
    print(current_texture_count)


def update_video():
    global video_clip, current_frame, current_texture_count

    if video_clip is None:
        return

    frame = video_clip.get_frame(current_frame / video_clip.fps)
    data = np.asfarray(frame.ravel(), dtype='f')
    texture_data = np.true_divide(data, 255.0)
    print(texture_data)
    dpg.set_value(f'video preview image {current_texture_count}', texture_data)
    current_frame = (current_frame + 1) % video_clip.reader.nframes


class VideoNode(NodeBase):
    def __init__(self):
        super().__init__('Video Clip')
        self.path = None

        with dpg.file_dialog(
                directory_selector=False, show=False, callback=self.set_video_path, tag=f'file_dialog_id:{self.id}',
                cancel_callback=self.set_video_path, width=700, height=400):
            dpg.add_file_extension('.mp4', color=(100, 150, 200))
            dpg.add_file_extension('.mov', color=(200, 100, 150))

        with dpg.node_attribute(label='Video File', parent=self.id, attribute_type=dpg.mvNode_Attr_Output):
            dpg.add_button(label='File Select', callback=lambda: dpg.show_item(f"file_dialog_id:{self.id}"))

        with dpg.node_attribute(label='Video Preview', parent=self.id, attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_button(label='Preview', callback=self.get_video_clip)

    def get_video_clip(self, sender, app_data, user_data):
        if self.path is None:
            return 
        print(self.path)
        is_active_video_node(sender, app_data, VideoFileClip(self.path))

    def set_video_path(self, sender, app_data, user_data):
        self.path = app_data['file_path_name']
        print(self.path)
