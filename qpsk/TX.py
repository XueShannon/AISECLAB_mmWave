#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: User
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import itertools
import math
import numpy
import numpy as np
import pmt
import random



from gnuradio import qtgui

class TX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "TX")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.data = data = [1,0,1,0]
        self.transition_bw = transition_bw = 200
        self.samp_rate = samp_rate = 22e5
        self.preamble = preamble = [1,1,0,0,1,1]
        self.decimation = decimation = 1
        self.MC_data = MC_data = list(np.repeat(data,2))
        self.threshold = threshold = 0.5
        self.tag_message = tag_message = gr.tag_utils.python_to_tag((0, pmt.intern("t0"), pmt.intern("0"), pmt.intern("vecsrc")))
        self.tag_clock = tag_clock = gr.tag_utils.python_to_tag((0, pmt.intern("clock"), pmt.intern("0"), pmt.intern("vecsrc")))
        self.symbol_rate = symbol_rate = 4000
        self.sps = sps = 100
        self.samp_rate_clock = samp_rate_clock = samp_rate*2
        self.periodicity = periodicity = len(MC_data)+len(preamble)
        self.payload_size = payload_size = 160
        self.packets = packets = [1,0,1,0,1,1]
        self.interval = interval = list(itertools.repeat(0, 20))
        self.filter_taps = filter_taps = firdes.low_pass(1,samp_rate,samp_rate/(2*decimation), transition_bw)
        self.clock = clock = "010101"
        self.centerfreq = centerfreq = 2400000000
        self.bits_per_pack = bits_per_pack = 1
        self.bits_per_clock = bits_per_clock = 1
        self.bandwidth = bandwidth = 22000000

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("addr = 192.168.10.7", '', "master_clock_rate=120e6")),
            uhd.stream_args(
                cpu_format="fc32",
                args='peak=0.003906',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_time_source('external', 0)
        self.uhd_usrp_sink_0.set_subdev_spec('A:0', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(centerfreq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(bandwidth, 0)
        self.uhd_usrp_sink_0.set_gain(60, 0)
        self._threshold_range = Range(0.001, 1, 0.001, 0.5, 200)
        self._threshold_win = RangeWidget(self._threshold_range, self.set_threshold, "threshold", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._threshold_win)
        self._sps_range = Range(1, 500, 1, 100, 200)
        self._sps_win = RangeWidget(self._sps_range, self.set_sps, "sample/symbol", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sps_win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=(int(samp_rate/symbol_rate)),
                decimation=1,
                taps=[1],
                fractional_bw=0)
        self.qtgui_time_sink_x_3 = qtgui.time_sink_c(
            4096, #size
            samp_rate, #samp_rate
            "data+preamble+ASK", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_3.set_update_time(0.10)
        self.qtgui_time_sink_x_3.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_3.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_3.enable_tags(True)
        self.qtgui_time_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "t0")
        self.qtgui_time_sink_x_3.enable_autoscale(True)
        self.qtgui_time_sink_x_3.enable_grid(True)
        self.qtgui_time_sink_x_3.enable_axis_labels(True)
        self.qtgui_time_sink_x_3.enable_control_panel(True)
        self.qtgui_time_sink_x_3.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_3.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_3.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_3.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_3.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_3.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_3_win = sip.wrapinstance(self.qtgui_time_sink_x_3.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_3_win)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
            4096, #size
            samp_rate, #samp_rate
            "data+preamble", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "t0")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_0_win)
        self.qtgui_sink_x_1_0_0 = qtgui.sink_c(
            4096, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            centerfreq, #fc
            bandwidth, #bw
            "data+preamble+ASK", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1_0_0.set_update_time(1.0/50)
        self._qtgui_sink_x_1_0_0_win = sip.wrapinstance(self.qtgui_sink_x_1_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1_0_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_1_0_0_win)
        self.blocks_xor_xx_0 = blocks.xor_bb()
        self.blocks_vector_source_x_0_0_0 = blocks.vector_source_b([int(x) for x in clock], True, 1, [tag_clock])
        self.blocks_vector_source_x_0 = blocks.vector_source_b(MC_data, True, 1, [tag_message])
        self.blocks_vector_insert_x_0_0 = blocks.vector_insert_b(interval, (periodicity+len(interval)), 0)
        self.blocks_vector_insert_x_0 = blocks.vector_insert_b(preamble, periodicity, 0)
        self.blocks_unpack_k_bits_bb_0_0 = blocks.unpack_k_bits_bb(bits_per_clock)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(bits_per_pack)
        self.blocks_uchar_to_float_0_0_1_0 = blocks.uchar_to_float()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 22e6,True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff((int(samp_rate/symbol_rate)), 1, 4000, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (samp_rate/500), 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_sink_x_1_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_time_sink_x_3, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_uchar_to_float_0_0_1_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0_1_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_xor_xx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_0, 0), (self.blocks_xor_xx_0, 1))
        self.connect((self.blocks_vector_insert_x_0, 0), (self.blocks_vector_insert_x_0_0, 0))
        self.connect((self.blocks_vector_insert_x_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_unpack_k_bits_bb_0_0, 0))
        self.connect((self.blocks_xor_xx_0, 0), (self.blocks_vector_insert_x_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_moving_average_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "TX")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        self.set_MC_data(list(np.repeat(self.data,2)))

    def get_transition_bw(self):
        return self.transition_bw

    def set_transition_bw(self, transition_bw):
        self.transition_bw = transition_bw
        self.set_filter_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decimation), self.transition_bw))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filter_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decimation), self.transition_bw))
        self.set_samp_rate_clock(self.samp_rate*2)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_frequency((self.samp_rate/500))
        self.blocks_moving_average_xx_0.set_length_and_scale((int(self.samp_rate/self.symbol_rate)), 1)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_3.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.set_periodicity(len(self.MC_data)+len(self.preamble))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_filter_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decimation), self.transition_bw))

    def get_MC_data(self):
        return self.MC_data

    def set_MC_data(self, MC_data):
        self.MC_data = MC_data
        self.set_periodicity(len(self.MC_data)+len(self.preamble))
        self.blocks_vector_source_x_0.set_data(self.MC_data, [self.tag_message])

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_tag_message(self):
        return self.tag_message

    def set_tag_message(self, tag_message):
        self.tag_message = tag_message
        self.blocks_vector_source_x_0.set_data(self.MC_data, [self.tag_message])

    def get_tag_clock(self):
        return self.tag_clock

    def set_tag_clock(self, tag_clock):
        self.tag_clock = tag_clock
        self.blocks_vector_source_x_0_0_0.set_data([int(x) for x in self.clock], [self.tag_clock])

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.blocks_moving_average_xx_0.set_length_and_scale((int(self.samp_rate/self.symbol_rate)), 1)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate_clock(self):
        return self.samp_rate_clock

    def set_samp_rate_clock(self, samp_rate_clock):
        self.samp_rate_clock = samp_rate_clock

    def get_periodicity(self):
        return self.periodicity

    def set_periodicity(self, periodicity):
        self.periodicity = periodicity

    def get_payload_size(self):
        return self.payload_size

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size

    def get_packets(self):
        return self.packets

    def set_packets(self, packets):
        self.packets = packets

    def get_interval(self):
        return self.interval

    def set_interval(self, interval):
        self.interval = interval

    def get_filter_taps(self):
        return self.filter_taps

    def set_filter_taps(self, filter_taps):
        self.filter_taps = filter_taps

    def get_clock(self):
        return self.clock

    def set_clock(self, clock):
        self.clock = clock
        self.blocks_vector_source_x_0_0_0.set_data([int(x) for x in self.clock], [self.tag_clock])

    def get_centerfreq(self):
        return self.centerfreq

    def set_centerfreq(self, centerfreq):
        self.centerfreq = centerfreq
        self.qtgui_sink_x_1_0_0.set_frequency_range(self.centerfreq, self.bandwidth)
        self.uhd_usrp_sink_0.set_center_freq(self.centerfreq, 0)

    def get_bits_per_pack(self):
        return self.bits_per_pack

    def set_bits_per_pack(self, bits_per_pack):
        self.bits_per_pack = bits_per_pack

    def get_bits_per_clock(self):
        return self.bits_per_clock

    def set_bits_per_clock(self, bits_per_clock):
        self.bits_per_clock = bits_per_clock

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.qtgui_sink_x_1_0_0.set_frequency_range(self.centerfreq, self.bandwidth)
        self.uhd_usrp_sink_0.set_bandwidth(self.bandwidth, 0)




def main(top_block_cls=TX, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
