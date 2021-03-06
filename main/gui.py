import tkinter as tk

import os
import sys

import asyncio

from lyrik import Lyrik
from local import Local


class Window(object):
    def __init__(self):
        self.lyrik = Lyrik()
        self.local = Local()

        self.root = tk.Tk()
        self.root.title('黙れ—左')
        self.root.bind("<Escape>", self.quit)

        self.topLabel = tk.Label(self.root, text="黙れ—左", font=("Helvetica", 26)).grid(row=0, column=0, columnspan=3)

        # topic for the train section
        self.train_topic = tk.Label(self.root, text="仕込む", font=("Helvetica 12 bold")).grid(row=1, column=0)

        # line to select the host
        self.host_label_train = tk.Label(self.root, text="サーバ").grid(row=2, column=0, sticky=tk.W, padx=10)
        self.host_entry_train = tk.Entry(self.root)
        self.host_entry_train.grid(row=2, column=1)
        self.host_entry_train.delete(0, tk.END)
        self.host_entry_train.insert(0, self.lyrik.host)

        # line to select the style file itself
        self.style_label = tk.Label(self.root, text="型").grid(row=3, column=0, sticky=tk.W, padx=10)
        self.selected_style = tk.StringVar(self.root)
        self.selected_style.set('choose')
        self.styles_chooser = tk.OptionMenu(self.root, self.selected_style, *self.lyrik.style_images()).grid(row=3, column=1)

        # line to select the image size for the training
        self.image_size_label = tk.Label(self.root, text="画像サイズ").grid(row=4, column=0, sticky=tk.W, padx=10)
        self.image_size_entry = tk.Entry(self.root)
        self.image_size_entry.grid(row=4, column=1)
        self.image_size_entry.delete(0, tk.END)
        self.image_size_entry.insert(0, 1080)

        # line to select the content weight for the training
        self.content_weight_label = tk.Label(self.root, text="コンテンツの重み").grid(row=5, column=0, sticky=tk.W, padx=10)
        self.content_weight_entry = tk.Entry(self.root)
        self.content_weight_entry.grid(row=5, column=1)
        self.content_weight_entry.delete(0, tk.END)
        self.content_weight_entry.insert(0, 1.0)

        # line to select the style weight for the training
        self.style_weight_label = tk.Label(self.root, text="スタイルウェイト").grid(row=6, column=0, sticky=tk.W, padx=10)
        self.style_weight_entry = tk.Entry(self.root)
        self.style_weight_entry.grid(row=6, column=1)
        self.style_weight_entry.delete(0, tk.END)
        self.style_weight_entry.insert(0, 5.0)

        def train():
            style_image = self.selected_style.get()
            style_size = self.image_size_entry.get()
            content_weight = self.content_weight_entry.get()
            style_weight = self.style_weight_entry.get()
            self.logger('training: ' + style_image + ' ' + style_size + ' ' + content_weight + ' ' + style_weight)
            self.lyrik.train(style_image, style_size, content_weight, style_weight)

        # train button
        self.train_button = tk.Button(self.root, text='仕込む!', command=train).grid(row=7, column=2)

        # topic for the render section
        self.render_topic = tk.Label(self.root, text="描く", font=("Helvetica 12 bold")).grid(row=9, column=0)

        # line to select the host
        self.host_label_render = tk.Label(self.root, text="サーバ").grid(row=10, column=0, sticky=tk.W, padx=10)
        self.host_entry_render = tk.Entry(self.root)
        self.host_entry_render.grid(row=10, column=1)
        self.host_entry_render.delete(0, tk.END)
        self.host_entry_render.insert(0, self.lyrik.host)

        # line to select the model file itself
        self.model_label = tk.Label(self.root, text="型").grid(row=11, column=0, sticky=tk.W, padx=10)
        self.selected_model = tk.StringVar(self.root)
        self.selected_model.set('choose')
        self.model_chooser = tk.OptionMenu(self.root, self.selected_model, *self.lyrik.models()).grid(row=11, column=1)

        # line to select the content video
        self.content_label = tk.Label(self.root, text="ビデオ").grid(row=12, column=0, sticky=tk.W, padx=10)
        self.selected_video = tk.StringVar(self.root)
        self.selected_video.set('choose')
        self.video_chooser = tk.OptionMenu(self.root, self.selected_video, *self.lyrik.content_videos()).grid(row=12, column=1)

        # line to select the resolution
        self.resolution_label = tk.Label(self.root, text="解像度").grid(row=13, column=0, sticky=tk.W, padx=10)
        self.resolution_entry = tk.Entry(self.root)
        self.resolution_entry.grid(row=13, column=1)
        self.resolution_entry.delete(0, tk.END)
        self.resolution_entry.insert(0, "960:540")

        # line to configure waifu2x
        self.waifu_label = tk.Label(self.root, text="高級").grid(row=14, column=0, sticky=tk.W, padx=10)
        self.do_waifu = tk.BooleanVar(self.root)
        self.waifu_checkbox = tk.Checkbutton(self.root, variable=self.do_waifu)
        self.waifu_checkbox.grid(row=14, column=1)

        # line to configure the output video fps
        self.outputfps_label = tk.Label(self.root, text="間隔").grid(row=15, column=0, sticky=tk.W, padx=10)
        self.output_fps_entry = tk.Entry(self.root)
        self.output_fps_entry.grid(row=15, column=1)
        self.output_fps_entry.delete(0, tk.END)
        self.output_fps_entry.insert(0, '60')

        def render():
            content = self.selected_video.get()
            style = self.selected_model.get()
            resolution = self.resolution_entry.get()
            waifu = self.do_waifu.get()
            fps = self.output_fps_entry.get()
            self.logger('rendering: ' + content + ' ' + style + ' ' + resolution + ' ' + str(waifu) + ' ' + fps)
            self.lyrik.render(content, style, resolution, waifu, fps)

        # render button
        self.render_button = tk.Button(self.root, text='描く!', command=render).grid(row=16, column=2)

        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.grid(row=17, column=4, rowspan=2, sticky='NSW')

        self.log = tk.Text(self.root, height=10, width=80, yscrollcommand=self.scrollbar.set)
        self.log.grid(row=17, column=0, columnspan=3)
        self.scrollbar.config(command=self.log.yview)

        self.sync_videos_to_lyrik()
        self.sync_images_to_lyrik()

        self.root.mainloop()

    def quit(self, ev):
        self.lyrik.disconnect()
        sys.exit(0)

    def logger(self, msg):
        self.log.insert(tk.END, str(msg)+'\n')
        self.scrollbar.config(command=self.log.yview)
        tk.Tk.update(self.root)

    def sync_images_to_lyrik(self):
        self.logger('start syncing images')
        lyrik_images = self.lyrik.style_images()
        self.logger('done syncing images')
        if self.lyrik.fabric.ERROR in lyrik_images:
            self.logger('Not syncing, no connection to Lyrik.')
            return

        local_images = self.local.style_images()
        self.logger('got local list')
        lyrik_missing = list(set(local_images) - set(lyrik_images))
        self.logger('some '+str(lyrik_missing)+' processing')
        lyrik_missing = [os.path.join(self.local.images_folder, fn) for fn in lyrik_missing]
        self.logger('start uploading images')
        self.lyrik.upload(self.lyrik.style_images_folder, lyrik_missing)
        self.logger('finished upload images')

    def sync_videos_to_lyrik(self):
        self.logger('started syncing videos')
        lyrik_videos = self.lyrik.content_videos()
        self.logger('got list')

        if self.lyrik.fabric.ERROR in lyrik_videos:
            self.logger('Not syncing, no connection to Lyrik.')
            return

        local_videos = self.local.content_videos()
        self.logger('got local list')
        lyrik_missing = list(set(local_videos) - set(lyrik_videos))
        self.logger('syncing '+str(lyrik_missing)+' some processing..')
        lyrik_missing = [os.path.join(self.local.video_folder, fn) for fn in lyrik_missing]
        self.logger('started uploading videos')
        self.lyrik.upload(self.lyrik.content_videos_folder, lyrik_missing)
        self.logger('finished uploading vidos')