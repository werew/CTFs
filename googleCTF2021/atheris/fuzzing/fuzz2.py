#!/usr/bin/python3
import atheris
import cryptography
from cryptography.hazmat.primitives.asymmetric import ed25519
import base64
import subprocess
import tempfile
import os

with atheris.instrument_imports():
    import turbozipfile
    import sys
    import zipfile


"""Finds the first *.<sig>.autorun.py file in a given ZIP file that's signed with the trusted public key."""

# arguments:
#  - argv[1]: path to zip file


with open(os.path.join(os.getcwd(), "public_key"), "rb") as f:
  public_key = ed25519.Ed25519PublicKey.from_public_bytes(f.read())

# This is not a cryptography challenge. The expected solution has
# nothing to do with breaking ed25519.
#@atheris.instrument_func
def check_signature(filename, file_bytes):
  b64 = filename.encode("utf-8")[0:-11]
  b64 = b64[-87:]
  b64 += b"=="
  b64 = b64.replace(b"_", b"/")
  sig = base64.decodebytes(b64)
  public_key.verify(sig, file_bytes)


@atheris.instrument_func
def validate_zipfile(info):
  if not info.filename:
    raise RuntimeError(f"Empty filename not allowed: {info.filename}")
  if info.filename[0] == '/':
    raise RuntimeError(f"Relative-to-root filename not allowed: {info.filename}")
  if ".." in info.filename.split("/"):
    raise RuntimeError(f"Directory backtracking in filename not allowed: {info.filename}")
  if "\0" in info.filename:
    raise RuntimeError(f"Null byte in filename not allowed: {info.filename}")
  if info.external_attr & 0x20000000:
    raise RuntimeError(f"Symlink not allowed: {info.filename}")
  disallowed_extras=[0x554e, 0x7075]
  extra = info.extra
  while extra:
    typ = int.from_bytes(extra[0:2], "little")
    if typ in disallowed_extras:
      raise RuntimeError(f"Extra field header {hex(typ)} not allowed: {info.filename}")
    sz = 4 + int.from_bytes(extra[2:4], "little")
    extra = extra[sz:]

class FileInfoDiffer(Exception):
    pass

class FileDataDiffer(Exception):
    pass

class FoundBugError(Exception):
    pass

@atheris.instrument_func
def find_valid_autorun(zip_filename):
  with open(zip_filename, "rb") as f:
    try:
        z = zipfile.ZipFile(f)
        infos = z.infolist()

        # Validate that this zip file is safe
        for info in infos:
          validate_zipfile(info)

        tz = turbozipfile.ZipFile(f)
        tinfos = tz.infolist()
    except Exception:
        return

    seen_files = []
    for info in infos:
      if info.filename in seen_files:
        raise RuntimeError(f"Multiple files with the same filename not allowed: {info.filename}")
      seen_files.append(info.filename)
    seen_files = sorted(seen_files)

    tseen_files = []
    for info in tinfos:
      tseen_files.append(info.filename)
    tseen_files = sorted(tseen_files)

    if seen_files != tseen_files:
        sys.stderr.write(f"FILE INFO DIFFER\n")
        sys.stderr.write(f"{seen_files}\n")
        sys.stderr.write(f"{tseen_files}\n")
        raise FileInfoDiffer()

    for info in infos:
        with z.open(info, "r") as g:
            try:
                data = g.read()
            except Exception:
                return None

        for tinfo in tinfos:
            if tinfo.filename != info.filename:
                continue

            with tz.open(info, "r") as g:
                try:
                    tdata = g.read()
                except Exception:
                    return None

        if data != tdata:
            sys.stderr.write(f"{data}\n")
            sys.stderr.write(f"{tdata}\n")
            raise FileDataDiffer()
  return None



######################################################################
######################################################################

outdir = tempfile.mkdtemp()


def TestOneInput(data):
    with open("input.zip","wb") as f:
        f.write(data)

    differ=False
    try:
        # First, check whether the zip file contains a valid autorun file.
        autorun = find_valid_autorun("input.zip")
        #if autorun is not None:
        #    raise FoundBugError()

        # Second, unzip the file properly.
        # Use our super-duper ultra-fast zip file implementation!
    except turbozipfile.BadZipFile:
        pass

    except zipfile.BadZipFile:
        pass
    
    except FoundBugError:
        raise FoundBugError

    except FileInfoDiffer:
        differ = True
        pass
        #raise FileInfoDiffer 

    except FileDataDiffer:
        raise FileDataDiffer 

    except Exception:
        pass



    try:
        with turbozipfile.ZipFile("input.zip") as z:
          z.extractall(outdir)
    except Exception:
        return

    if differ:
        raise FoundBugError()

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()

