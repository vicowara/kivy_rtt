#!/usr/bin/env python3

import sys
import subprocess
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.config import Config

kivy.require("1.10.0")
Config.set("graphics", "width", "120")
Config.set("graphics", "height", "30")
Config.set("graphics", "borderless", "True")

_interval = 1
_destination = "192.168.1.1"


class RootLayout(BoxLayout):
    text = StringProperty()
    color = ListProperty([0, 0, 0, 0])

    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)

    def update_label(self, text, color):
        self.text = text
        self.color = color


def decide_color_level(rtt):
    max_thresholds = 100
    rtt = rtt if rtt < max_thresholds else max_thresholds
    red = rtt / max_thresholds

    return [red, 0, 0, 0]


class RTTApp(App):
    def callback(self, dt):
        cmd = ("ping {dst} -c 1"
               "|perl -anle 'print $1 if /bytes/ && $F[6] =~ /([0-9.]+)/'"
               .format(dst=_destination))
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            stdout, stderr = p.communicate(timeout=_interval)
        except subprocess.TimeoutExpired:
            print("timeout", file=sys.stderr)
        else:
            output = float(stdout.decode("utf-8"))
            self.layout.update_label("{} ms".format(output),
                                     color=decide_color_level(output))

    def build(self):
        self.layout = RootLayout()
        Clock.schedule_interval(self.callback, _interval)
        return self.layout


if __name__ == "__main__":
    RTTApp().run()
