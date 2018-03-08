# -*- coding:utf-8 -*-
import socket
import subprocess
import time
import logging
from logging.handlers import RotatingFileHandler


def popen_command(command, shell=False):
    """
    执行命令行
    :param command:  如果shell是False，传入命令行list，如果shell是True ，传入命令行字符串
    :param shell: If true, the command will be executed through the shell
    :return:stdout,stderr
    """
    return subprocess.Popen(command, shell=shell, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()


def get_host_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            return ip
        except socket.error:
            pass
    finally:
        if s:
            s.close()
    return None


def init_logging(file_uri, level=logging.INFO):
    """
    初始化logging
    :param file_uri:  文件路径和文件名
    :param level: 日志级别，默认INFO
    """
    logging.basicConfig(format="%(asctime)-12s: %(levelname)-3s %(message)s", level=level)
    file_handler = RotatingFileHandler(file_uri, maxBytes=10 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(file_handler)


if __name__ == '__main__':
    init_logging('/tmp/wifi_auto.log')
    logging.info('start')
    while True:
        try:
            ip = get_host_ip()
            logging.info('ip==%s', ip)
            if not ip:
                logging.info('re connect')
                popen_command(['wifiutil', 'associate', 'HAXII-4G', '-p', '12345678'])
        except Exception as e:
            logging.error(e)
        time.sleep(60)
