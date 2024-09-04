#!/usr/bin/env python3


from wb_modbus import bindings, parse_uart_settings_str
from collections import OrderedDict
import logging
import sys



MODBUS_ADDRESS = 110
UART_PARAM = [9600, 'N', 2]
DEVICE = 'mr3lvi'


tables = {
    "mr3lvi":{
        'holdings':[
                    {'start': 128, 'end': 130},
                    {'start': 384, 'end': 447},

            ],


        'inputs':[
                    {'start': 40, 'end': 55},

            ]
            }
        }





def do_read_holdings(client, types):
    """
    Reading fram into a dict
    """
    result = OrderedDict()

    t = tables[types]['holdings']
    for table in t:
        base_address = table['start']
        length = table['end'] - table['start'] + 1
        regs = client.read_u16_holdings(base_address, length)
        result.update({base_address : regs})
    return result



def do_read_inputs(client, types):
    """
    Reading fram into a dict
    """
    result = OrderedDict()

    t = tables[types]['inputs']
    for table in t:
        base_address = table['start']
        length = table['end'] - table['start'] + 1
        regs = client.read_u16_inputs(base_address, length)
        result.update({base_address : regs})
    return result



def do_read_tables(client, types, dumpfile=sys.stdout): #Gets a FILE type object as arg
    """
    Reading holdings into an opened fp
    """
    result = do_read_holdings(client, types)
    dumpfile.write('holdings\n')
    for base_address, regs in result.items():
        regs_str = ', '.join(map(str, regs))
        dumpfile.write(f'0x{base_address}: [{regs_str}]\n')

    result = do_read_inputs(client, types)
    dumpfile.write('inputs\n')
    for base_address, regs in result.items():
        regs_str = ', '.join(map(str, regs))
        dumpfile.write(f'0x{base_address}: [{regs_str}]\n')

    dumpfile.close()


def main():
    uart_params = UART_PARAM
    client = bindings.WBModbusDeviceBase(MODBUS_ADDRESS, '/dev/ttyRS485-2', *uart_params)
    if not client.device:
        logging.error("Failed to connect to RS-485 bus")
        return

    types = DEVICE
    dumpfile = 'txt.txt'


    do_read_tables(client, types)


if __name__ == '__main__':
    main()
