#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import hashlib
import os
import sys

def hash_bytestr_iter(bytesiter, hasher):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest()

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

if len (sys.argv) == 1:
    exit()

out_name = str(os.getenv('SLIC3R_PP_OUTPUT_NAME'))

hashstr = hash_bytestr_iter(file_as_blockiter(open(sys.argv[1], 'rb')), hashlib.md5())
path = os.path.splitext(out_name)
fname = path[0] + "_" + str(hashstr) + path[1]

with open(sys.argv[1] + '.output_name', mode='w', encoding='UTF-8') as fopen:
    fopen.write(fname)
