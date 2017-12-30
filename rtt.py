#!/usr/bin/env python3

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.config import Config
import subprocess
import sys

kivy.require("1.10.0")
Config.set("graphics", "width", "120")
Config.set("graphics", "height", "90")


class RootLayout(BoxLayout):
    text = StringProperty()
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)

    def update_label(self, text, color):
        self.text = text
        self.color = color


def decide_color_level(rtt):
    max_thresholds = 100
    rtt = rtt if max_thresholds > rtt else max_thresholds
    red = rtt / max_thresholds

    return [red, 0, 0, 0]


class RTTApp(App):
    def callback(self, dt):
        cmd = ("ping 192.168.1.1 -c 1|"
               "perl -anle 'print $1 if /bytes/ && $F[6] =~ /([0-9.]+)/'")

        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = p.communicate(timeout=0.5)
        except subprocess.TimeoutExpired:
            print("timeout", file=sys.stderr)
        else:
            output = float(stdout.decode("utf-8"))
            self.layout.update_label("{} ms".format(output),
                                     color=decide_color_level(output))

    def build(self):
        self.layout = RootLayout()
        Clock.schedule_interval(
            self.callback, 0.5
        )
        return self.layout


if __name__ == "__main__":
    RTTApp().run()
