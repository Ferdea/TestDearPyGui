import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
import dearpygui.dearpygui as dpg

from nodes.node_base import NodeBase


class FilterNode(NodeBase):
    def __init__(self, video_path: str):
        super().__init__('Video Clip')
        self.video_clip = VideoFileClip(video_path)
        self.current_frame = 1

        frame = self.video_clip.get_frame(0)
        data = np.asfarray(frame.ravel(), dtype='f')
        texture_data = np.true_divide(data, 255.0)
        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(frame.shape[1], frame.shape[0], texture_data, tag=f'{self.id}:image',
                                format=dpg.mvFormat_Float_rgb)

        with dpg.node_attribute(label='Video', parent=self.id, attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_image(f'{self.id}:image', width=min(frame.shape[1], 512), height=min(frame.shape[0], 288))

        with dpg.node_attribute(label='Video Duration', parent=self.id, attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_slider_float(label='Video Duration', width=256, max_value=self.video_clip.duration, min_value=0,
                                 callback=self.set_frame, tag=f'{self.id}:slider', )

        self.update_frame()

    def set_frame(self, sender, duration):
        self.current_frame = int(duration * self.video_clip.fps)

    def update_frame(self):
        frame = self.video_clip.get_frame(self.current_frame / self.video_clip.fps)
        data = np.asfarray(frame.ravel(), dtype='f')
        texture_data = np.true_divide(data, 255.0)
        dpg.set_value(f'{self.id}:image', texture_data)
        self.current_frame = (self.current_frame + 1) % self.video_clip.reader.nframes
        dpg.set_value(f'{self.id}:slider', self.current_frame / self.video_clip.fps)
