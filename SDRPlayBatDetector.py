#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SDRPlayBatDetector-grc
# Author: JoeTester1965
# Copyright: MIT License
# GNU Radio version: 3.10.5.1

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import sdrplay3
from gnuradio import zeromq
from gnuradio.fft import logpwrfft
import configparser




class SDRPlayBatDetector(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "SDRPlayBatDetector-grc", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self._samp_rate_config = configparser.ConfigParser()
        self._samp_rate_config.read('./SDRPlayBatDetector.ini')
        try: samp_rate = self._samp_rate_config.getint('graph', 'samp_rate')
        except: samp_rate = 250000
        self.samp_rate = samp_rate
        self._fft_resolution_config = configparser.ConfigParser()
        self._fft_resolution_config.read('./SDRPlayBatDetector.ini')
        try: fft_resolution = self._fft_resolution_config.getint('graph', 'fft_resolution')
        except: fft_resolution = 1024
        self.fft_resolution = fft_resolution
        self._fft_frame_rate_config = configparser.ConfigParser()
        self._fft_frame_rate_config.read('./SDRPlayBatDetector.ini')
        try: fft_frame_rate = self._fft_frame_rate_config.getint('graph', 'fft_frame_rate')
        except: fft_frame_rate = 10
        self.fft_frame_rate = fft_frame_rate
        self._decimation_config = configparser.ConfigParser()
        self._decimation_config.read('./SDRPlayBatDetector.ini')
        try: decimation = self._decimation_config.getint('graph', 'decimation')
        except: decimation = 10
        self.decimation = decimation
        self._audio_conversion_gain_config = configparser.ConfigParser()
        self._audio_conversion_gain_config.read('./SDRPlayBatDetector.ini')
        try: audio_conversion_gain = self._audio_conversion_gain_config.getint('graph', 'audio_conversion_gain')
        except: audio_conversion_gain = 256
        self.audio_conversion_gain = audio_conversion_gain

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://127.0.0.1:50241', 100, False)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_float, fft_resolution, 'tcp://127.0.0.1:50242', 100, False, (-1), '', True)
        self.sdrplay3_rspdxr2_0 = sdrplay3.rspdxr2(
            '',
            stream_args=sdrplay3.stream_args(
                output_type='fc32',
                channels_size=1
            ),
        )
        self.sdrplay3_rspdxr2_0.set_sample_rate(samp_rate)
        self.sdrplay3_rspdxr2_0.set_center_freq(0)
        self.sdrplay3_rspdxr2_0.set_bandwidth(0)
        self.sdrplay3_rspdxr2_0.set_antenna('Antenna B')
        self.sdrplay3_rspdxr2_0.set_gain_mode(False)
        self.sdrplay3_rspdxr2_0.set_gain(-(59), 'IF')
        self.sdrplay3_rspdxr2_0.set_gain(-(0), 'RF')
        self.sdrplay3_rspdxr2_0.set_freq_corr(0)
        self.sdrplay3_rspdxr2_0.set_dc_offset_mode(True)
        self.sdrplay3_rspdxr2_0.set_iq_balance_mode(True)
        self.sdrplay3_rspdxr2_0.set_agc_setpoint((-30))
        self.sdrplay3_rspdxr2_0.set_hdr_mode(False)
        self.sdrplay3_rspdxr2_0.set_rf_notch_filter(False)
        self.sdrplay3_rspdxr2_0.set_dab_notch_filter(False)
        self.sdrplay3_rspdxr2_0.set_biasT(False)
        self.sdrplay3_rspdxr2_0.set_debug_mode(False)
        self.sdrplay3_rspdxr2_0.set_sample_sequence_gaps_check(False)
        self.sdrplay3_rspdxr2_0.set_show_gain_changes(False)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_float, 1, '192.168.1.77', 50243, 0, 1472, False)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=fft_resolution,
            ref_scale=1,
            frame_rate=fft_frame_rate,
            avg_alpha=1.0,
            average=True,
            shift=True)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimation,  firdes.low_pass(1,samp_rate,samp_rate/decimation/3,100), (samp_rate/4), samp_rate)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(audio_conversion_gain)
        self.blocks_correctiq_0 = blocks.correctiq()
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.freq_xlating_fir_filter_xxx_0, 'freq'))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_correctiq_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_correctiq_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.sdrplay3_rspdxr2_0, 0), (self.blocks_correctiq_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1,self.samp_rate,self.samp_rate/self.decimation/3,100))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.samp_rate/4))
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.sdrplay3_rspdxr2_0.set_sample_rate(self.samp_rate)

    def get_fft_resolution(self):
        return self.fft_resolution

    def set_fft_resolution(self, fft_resolution):
        self.fft_resolution = fft_resolution

    def get_fft_frame_rate(self):
        return self.fft_frame_rate

    def set_fft_frame_rate(self, fft_frame_rate):
        self.fft_frame_rate = fft_frame_rate

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1,self.samp_rate,self.samp_rate/self.decimation/3,100))

    def get_audio_conversion_gain(self):
        return self.audio_conversion_gain

    def set_audio_conversion_gain(self, audio_conversion_gain):
        self.audio_conversion_gain = audio_conversion_gain
        self.blocks_multiply_const_vxx_0.set_k(self.audio_conversion_gain)




def main(top_block_cls=SDRPlayBatDetector, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
