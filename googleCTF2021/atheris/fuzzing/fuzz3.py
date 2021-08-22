#!/usr/bin/env python3
import warnings
warnings.simplefilter("ignore", UserWarning)

import base64

import atheris

with atheris.instrument_imports():
    import sys
    import turbozipfile
    import zipfile


class FileDataDiffer(Exception):
    pass


@atheris.instrument_func
def a(filename):
    with zipfile.ZipFile('test.zip', 'w') as fh:
        try:
            fh.writestr(filename.decode('utf8'), b'data')
            fh.writestr(filename.decode('cp437'), b'data')
        except:
            #print(filename.decode('cp437'))
            return None

    with open('test.zip', 'rb') as fh:
        z = zipfile.ZipFile(fh)
        zinfo = z.infolist()

        for info in zinfo:
            if '..' in info.filename.split('/') or '\0' in info.filename:
                return

        tz = turbozipfile.ZipFile(fh)
        tinfo = tz.infolist()

    zset = {i.filename for i in zinfo}
    tset = {i.filename for i in tinfo}

    #print(filename, zset, tset)
    if len(zset) != len(tset):
        print(f'{filename=}')
        print(f'Files in ZipFile: {zset};\nFiles in TurboZipFile: {tset}')
        raise FileDataDiffer()

#a(bytes.fromhex('2f 61 05 e5 00'))
#a(base64.b64decode('Li4='))
#a(bytes.fromhex('417f'))

#quit()


def TestOneInput(data):
    try:
        a(data)
    except FileDataDiffer:
        raise
    except:
        # drop all exceptions except for FileDataDiffer
        pass


atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()