#! -*- coding: utf-8 -*-

import sys

from ConfigSwitcher import ConfigSwitcher

if __name__ == "__main__":
    try:
        s = ConfigSwitcher(sys.argv[1])

        s.switch()
    except IndexError:
        print("Не указан путь к файлу.")
        exit()

