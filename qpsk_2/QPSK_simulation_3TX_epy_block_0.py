"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, preamble=1.0, match=[1,1]):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.preamble = preamble
        self.match = match
        self.count = 0
        self.error = 0
        self.len = len(match)
        self.step = 1
        self.time = time.time()

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if time.time() - self.time < 1:
            return (len(input_items[0]))
        for x in input_items[0]:
            match self.step:
                case 1:
                    if x == 0:
                        self.count = self.count + 1
                    if self.count >= self.preamble*8:
                        self.step = 2
                        self.count = 0

                case 2:                     
                    if x != self.match[self.count]:
                        self.error = self.error + 1

                    self.count = self.count + 1
                    
                    if self.count >= self.len:
                        print("symbol error rate:")
                        print(self.error/self.len*100)
                        print("%")
                        self.step = 1
                        self.count = 0
                        self.error = 0
                        self.time = time.time()     

        return (len(input_items[0]))
