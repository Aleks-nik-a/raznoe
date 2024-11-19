#!/usr/bin/env python3


from wb_modbus import bindings, parse_uart_settings_str
from collections import OrderedDict
import logging
import sys



MODBUS_ADDRESS = 69
UART_PARAM = [9600, 'N', 2]
DEVICE = 'map12e'
PORT = '/dev/ttyRS485-2'


tables = {
    'mr3lvi':{
        'holdings':[
                    {'start': 128, 'end': 130},
                    {'start': 384, 'end': 447},

            ],


        'inputs':[
                    {'start': 40, 'end': 55},

            ]
            },
    'map3e':{
        'holdings':[
            {'start': 0x1490, 'end': 0x1490 + 5  },
            {'start': 0x1001, 'end': 0x1001 + 13 },
            {'start': 0x1031, 'end': 0x1031 + 9 },
            {'start': 0x1041, 'end': 0x1041 + 11 },
            {'start': 0x1051, 'end': 0x1051 + 5  },
            {'start': 0x1061, 'end': 0x1061 + 11 },
            {'start': 0x1460, 'end': 0x1460 + 5  },
            {'start': 0x1000, 'end': 0x1000 + 0  },
            {'start': 0x14a0, 'end': 0x14a0 + 2  },
        ]
    },
    'map12e':{
        'holdings':[
            {'start': 0x1490, 'end': 0x1490 + 5  },
            {'start': 0x1001, 'end': 0x1001 + 13 },
            {'start': 0x1031, 'end': 0x1031 + 9  },
            {'start': 0x1041, 'end': 0x1041 + 11 },
            {'start': 0x1051, 'end': 0x1051 + 5  },
            {'start': 0x1061, 'end': 0x1061 + 11 },
            {'start': 0x1460, 'end': 0x1460 + 5  },
            {'start': 0x1000, 'end': 0x1000 + 0  },
            {'start': 0x14a0, 'end': 0x14a0 + 2  },
            {'start': 0x2490, 'end': 0x2490 + 5  },
            {'start': 0x2001, 'end': 0x2001 + 13 },
            {'start': 0x2031, 'end': 0x2031 + 9  },
            {'start': 0x2041, 'end': 0x2041 + 11 },
            {'start': 0x2051, 'end': 0x2051 + 5  },
            {'start': 0x2061, 'end': 0x2061 + 11 },
            {'start': 0x2460, 'end': 0x2460 + 5  },
            {'start': 0x2000, 'end': 0x2000 + 0  },
            {'start': 0x24a0, 'end': 0x24a0 + 2  },
            {'start': 0x3490, 'end': 0x3490 + 5  },
            {'start': 0x3001, 'end': 0x3001 + 13 },
            {'start': 0x3031, 'end': 0x3031 + 9  },
            {'start': 0x3041, 'end': 0x3041 + 11 },
            {'start': 0x3051, 'end': 0x3051 + 5  },
            {'start': 0x3061, 'end': 0x3061 + 11 },
            {'start': 0x3460, 'end': 0x3460 + 5  },
            {'start': 0x3000, 'end': 0x3000 + 0  },
            {'start': 0x34a0, 'end': 0x34a0 + 2  },
            {'start': 0x4490, 'end': 0x4490 + 5  },
            {'start': 0x4001, 'end': 0x4001 + 13 },
            {'start': 0x4031, 'end': 0x4031 + 9  },
            {'start': 0x4041, 'end': 0x4041 + 11 },
            {'start': 0x4051, 'end': 0x4051 + 5  },
            {'start': 0x4061, 'end': 0x4061 + 11 },
            {'start': 0x4460, 'end': 0x4460 + 5  },
            {'start': 0x4000, 'end': 0x4000 + 0  },
            {'start': 0x44a0, 'end': 0x44a0 + 2  },
        ]
    },



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
        try:
            regs = client.read_u16_holdings(base_address, length)
            result.update({base_address : regs})
        except:
            pass
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
        try:
            regs = client.read_u16_inputs(base_address, length)
            result.update({base_address : regs})
        except:
            pass
    return result



def do_read_tables(client, types, dumpfile=sys.stdout): #Gets a FILE type object as arg
    """
    Reading holdings into an opened fp
    """
    if 'holdings' in tables[types]:
        result = do_read_holdings(client, types)
        dumpfile.write('holdings\n')
        for base_address, regs in result.items():
            regs_str = ', '.join(map(str, regs))
            dumpfile.write(f'0x{base_address}: [{regs_str}]\n')

    if 'inputs' in tables[types]:
        result = do_read_inputs(client, types)
        dumpfile.write('inputs\n')
        for base_address, regs in result.items():
            regs_str = ', '.join(map(str, regs))
            dumpfile.write(f'0x{base_address}: [{regs_str}]\n')

    dumpfile.close()


def main():
    uart_params = UART_PARAM
    client = bindings.WBModbusDeviceBase(MODBUS_ADDRESS, PORT, *uart_params)
    if not client.device:
        logging.error("Failed to connect to RS-485 bus")
        return

    types = DEVICE
    dumpfile = 'txt.txt'


    do_read_tables(client, types)


if __name__ == '__main__':
    main()
