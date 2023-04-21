"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import hashlib


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, text="Enter the text here"):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Hash encode',   # will show up in GRC
            in_sig=None,
            out_sig=[(np.byte,320)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.text = text

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        result = hashlib.sha1(self.text.encode())

        list_str = list(bin(int(result.hexdigest(), 16))[2:].zfill(160))

        byte_array = np.array(list_str, dtype=int).repeat(2)

        output_items[0][:] = byte_array

        return len(output_items[0])
