#coding=utf-8
__author__ = 'jerry'

from escpos import *

HOST = '192.168.123.200'
p = printer.Network(HOST)
p.text(u'妈妈，北京下的好大的雪啊。 好大的雪啊。好大的雪啊。好大的雪啊。好大的雪啊。好大的雪啊。好大的雪啊。好大的雪啊。好大的雪啊。\r\n'.encode('gb2312'))
p.cut()