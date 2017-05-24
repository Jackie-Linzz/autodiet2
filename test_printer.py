__author__ = 'jerry'

'''
import escpos


HOST = '192.168.123.200'
PORT = 9100
addr = (HOST, PORT)

'''
font_b = b'\x1b\x21\x8'
clear_font = b"\x1c\x21\x00"
fd_font = b'\x1c\x21\x4'
print_code = b'\x1d\x68\x78\x1d\x48\x10\x1d\x6b\x2'

'''
p = escpos.printer.Network(HOST, PORT)
p.text('the art of time\r\n')
p.cut()
'''

