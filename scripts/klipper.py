#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Скрипт проверки совпадения контрольных сумм файла в слайсере
и после загрузки в принтер.
@author: Шовкат Кудратов (shah.typhoon@gmail.com
@license: MIT
@date: 04.06.2024
"""

import hashlib
import os
import sys

def hash_bytestr_iter(bytesiter, hasher, ashexstr=True):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

if len (sys.argv) < 2:
    print("!! Ошибка. Не указан обязательный параметр.")
    exit()

fname = ' '.join(sys.argv[1:])
if not os.path.exists(fname):
    print("!! Ошибка. Указанный файл не найден.")
    exit()

path = os.path.splitext(fname)
parts = path[0].rsplit('_', 1)
if len(parts) < 2 or len(parts[1]) != 32:
    print('!! Имя файла не содержит контрольную сумму из слайсера. Но это не значит, что файл поврежден. Можете продолжить печать на свой страх и риск.')
    exit()

hashstr = hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.md5())

print(f"Контрольная сумма файла из слайсера: {parts[1]}\nКонтрольная сумма загруженного файла: {hashstr}")
if parts[1] == hashstr:
    print("Контрольные суммы СОВПАДАЮТ, файл не битый. Для продолжения возобновите печать.")
else:
    print("!! ВНИМАНИЕ! Контрольные суммы НЕ СОВПАДАЮТ! Файл загружен с ошибкой.")
