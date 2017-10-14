#! -*- coding: utf-8 -*-

from __future__ import print_function
import fileinput, re

"""
Класс, для переключения конфигурации NGINX.
"""
class ConfigSwitcher():
    __FRONTEND = 1
    __BACKEND = 2

    # Признак: открыт frontend или backend
    __TYPE = None

    def __init__(self, path):
        try:
            self.f = fileinput.FileInput(path, inplace=1, backup=".bck")

            regex_front = re.compile(r'^#.*(?=\s#\stype:\sfrontend$)', re.IGNORECASE)
            regex_back = re.compile(r'^#.*(?=\s#\stype:\sbackend$)', re.IGNORECASE)

            # Индексация файла для определения текущей настройки (backend|frontend)
            with open(path) as file:
                for line in file:
                    if regex_front.findall(line):
                        self.__TYPE = self.__BACKEND
                        break
                    elif regex_back.findall(line):
                        self.__TYPE = self.__FRONTEND
                        break
        except IOError:
            print("File is not exists.\n")
            exit()

    """
    Функция переключает в конфигурации frontend и backend.
    """
    def switch(self):
        regex_front = re.compile(r'^.*(?=\s#\stype:\sfrontend$)', re.IGNORECASE)
        regex_back = re.compile(r'^.*(?=\s#\stype:\sbackend$)', re.IGNORECASE)

        for line in self.f:
            if regex_front.findall(line) and self.__TYPE == 1:
                # Если открыт frontend и найдена строка с frontend-конфигурацией,
                # то закрываем frontend.
                print("#%s" % line, end='')
            elif regex_back.findall(line) and self.__TYPE == 1:
                # Если открыт frontend и найдена строка с backend-конфигурацией,
                # то открываем backend.
                print(line.replace("#", "", 1), end='')
            elif regex_front.findall(line) and self.__TYPE == 2:
                # Если открыт backend и найдена строка с frontend-конфигурацией,
                # то открываем frontend.
                print(line.replace("#", "", 1), end='')
            elif regex_back.findall(line) and self.__TYPE == 2:
                # Если открыт backend и найдена строка с backend-конфигурацией,
                # то закрываем backend.
                print("#%s" % line, end='')
            else:
                print(line, end='')

    def get_type(self):
        return self.__TYPE

    def __del__(self):
        self.f.close()