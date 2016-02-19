# /////////////////////////////////////////////////////////////////////
#
#  oom.py : Provides the Northbound API, hides the implementation in
#  oomlib.py decode.py and the module type definitions
#
#  Copyright 2015  Finisar Inc.
#
#  Author: Don Bollinger don@thebollingers.org
#
# ////////////////////////////////////////////////////////////////////

import oomlib
from oomlib import decodelib, print_block_hex
from decode import get_string


#
# helper routine, provides a port without requiring the user to
# define the complicated port_t struct
#
def oom_get_port(n):
    port = oomlib.oom_get_port(n)
    return (port)


#
# similarly, get the full list of ports, allocates the
# memory, defines the data types, simple
#
def oom_get_portlist():
    port_list = oomlib.oom_get_portlist()
    return(port_list)


#
# magic decoder - gets any attribute based on its key attribute
# if there is no decoder for the port type, or the key is not
# listed in the memory map for that port type, then returns ''
# NOTE: the type of the value returned depends on the key.
# Use 'str(oom_get_keyvalue(port, key))' to get a readable string
# for all return types
#
def oom_get_keyvalue(port, key):
    mm = port.mmap
    if key not in mm:
        return ''
    par = (port,) + mm[key][1:]           # get the parameters
    raw_data = oom_get_memory_sff(*par)    # get the data
    decoder = getattr(decodelib, mm[key][0])  # get the decoder
    temp = decoder(raw_data)              # get the value
    return temp                           # and return it


#
# Set a key to chosen value (write key to EEPROM)
# Be careful with this, this is likely to change the function
# of your module
#
def oom_set_keyvalue(port, key, value):
    return oomlib.oom_set_keyvalue(port, key, value)


#
# given a 'function', return a dictionary with the values of all the
# keys in that function, on the specified port
#
def oom_get_memory(port, function):

    funcmap = port.fmap
    retval = {}

    if function not in funcmap:
        return None

    for keys in funcmap[function]:
        retval[keys] = oom_get_keyvalue(port, keys)
    return retval


#
# TODO - throw an exception if len != length
#
def oom_get_memory_sff(port, address, page, offset, length):
    return oomlib.oom_get_memory_sff(port, address, page, offset, length)


def oom_set_memory_sff(port, address, page, offset, length, data):
    return oomlib.oom_set_memory_sff(port, address, page, offset, length, data)
