#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Attacker
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
import random



from gnuradio import qtgui

class Attacker(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Attacker", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Attacker")
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

        self.settings = Qt.QSettings("GNU Radio", "Attacker")

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
        self.transition_bw = transition_bw = 200
        self.samp_rate = samp_rate = 22e5
        self.decimation = decimation = 1
        self.threshold = threshold = 0.9
        self.symbol_rate = symbol_rate = 4000
        self.sps = sps = 100
        self.samp_rate_clock = samp_rate_clock = samp_rate*2
        self.preamble = preamble = [1,1,0,0,1,1]
        self.filter_taps = filter_taps = firdes.low_pass(1,samp_rate,samp_rate/(2*decimation), transition_bw)
        self.delay = delay = 0
        self.centerfreq = centerfreq = 2400000000
        self.bits_per_pack = bits_per_pack = 1
        self.bits_per_clock = bits_per_clock = 1
        self.bandwidth = bandwidth = 22000000

        ##################################################
        # Blocks
        ##################################################

        self._threshold_range = Range(0.01, 1, 0.1, 0.9, 200)
        self._threshold_win = RangeWidget(self._threshold_range, self.set_threshold, "threshold", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._threshold_win)
        self._sps_range = Range(1, 500, 1, 100, 200)
        self._sps_win = RangeWidget(self._sps_range, self.set_sps, "sample/symbol", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sps_win)
        self._delay_range = Range(0, 100, 1, 0, 200)
        self._delay_win = RangeWidget(self._delay_range, self.set_delay, "'delay'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._delay_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("addr = 192.168.10.8", '', "master_clock_rate=120e6")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_subdev_spec('A:0', 0)
        self.uhd_usrp_source_0.set_samp_rate(2200000)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(centerfreq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(bandwidth, 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(20, 0)
        self.uhd_usrp_source_0.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source_0.set_auto_iq_balance(True, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("addr=192.168.10.6", '', "master_clock_rate=120e6")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_time_source('external', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(2400000000, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(22000000, 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "output_directly", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "t0")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "output_after_estimator", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "t0")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_1_0_0_0 = qtgui.sink_f(
            4096, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            centerfreq, #fc
            bandwidth, #bw
            "output_1", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1_0_0_0.set_update_time(1.0/50)
        self._qtgui_sink_x_1_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_1_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1_0_0_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_1_0_0_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, filter_taps, centerfreq, samp_rate)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(preamble, sps, 0, threshold, digital.THRESHOLD_ABSOLUTE)
        self.digital_clock_recovery_mm_xx_0_0 = digital.clock_recovery_mm_ff(1, (0.25*0.175*0.175), 0.5, 0.175, 0.005)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(1, (0.25*0.175*0.175), 0.5, 0.175, 0.005)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'C:\\Users\\AISECLAB\\Desktop\\AISECLAB_mmWave\\qpsk\\attacker.data', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.analog_pll_carriertracking_cc_0 = analog.pll_carriertracking_cc(0.05, (2*math.pi*centerfreq/samp_rate), (-2*math.pi*centerfreq/samp_rate))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.digital_clock_recovery_mm_xx_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.qtgui_sink_x_1_0_0_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.analog_pll_carriertracking_cc_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_file_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Attacker")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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
        self.analog_pll_carriertracking_cc_0.set_max_freq((2*math.pi*self.centerfreq/self.samp_rate))
        self.analog_pll_carriertracking_cc_0.set_min_freq((-2*math.pi*self.centerfreq/self.samp_rate))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_filter_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decimation), self.transition_bw))

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.digital_corr_est_cc_0.set_threshold(self.threshold)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate_clock(self):
        return self.samp_rate_clock

    def set_samp_rate_clock(self, samp_rate_clock):
        self.samp_rate_clock = samp_rate_clock

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_filter_taps(self):
        return self.filter_taps

    def set_filter_taps(self, filter_taps):
        self.filter_taps = filter_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.filter_taps)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(int(self.delay))

    def get_centerfreq(self):
        return self.centerfreq

    def set_centerfreq(self, centerfreq):
        self.centerfreq = centerfreq
        self.analog_pll_carriertracking_cc_0.set_max_freq((2*math.pi*self.centerfreq/self.samp_rate))
        self.analog_pll_carriertracking_cc_0.set_min_freq((-2*math.pi*self.centerfreq/self.samp_rate))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.centerfreq)
        self.qtgui_sink_x_1_0_0_0.set_frequency_range(self.centerfreq, self.bandwidth)
        self.uhd_usrp_source_0.set_center_freq(self.centerfreq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.centerfreq, 1)

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
        self.qtgui_sink_x_1_0_0_0.set_frequency_range(self.centerfreq, self.bandwidth)
        self.uhd_usrp_source_0.set_bandwidth(self.bandwidth, 0)
        self.uhd_usrp_source_0.set_bandwidth(self.bandwidth, 1)




def main(top_block_cls=Attacker, options=None):

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
