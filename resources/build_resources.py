import subprocess
import sys
import os
import traceback

UI_PYTHON_PATH = '../python/app/ui'

uic_path = ''
rcc_path = ''


def build_qt(exec_path, file_name, ext, output_file_name):
    cmd = '%s -o "%s/%s.py" "%s.%s"' % (exec_path, UI_PYTHON_PATH, output_file_name, file_name, ext)
    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    p.wait()

    output_path = os.path.realpath(os.path.join(UI_PYTHON_PATH, output_file_name+'.py'))

    fp = open(output_path, 'r')
    try:
        s = fp.read()
    except:
        print traceback.format_exc()
        return
    finally:
        fp.close()

    s = s.replace('from PySide import', 'from tank.platform.qt import')
    fp = open(output_path, 'w')
    try:
        fp.write(s)
    except:
        print traceback.format_exc()
    finally:
        fp.close()


def build_ui(file_name):
    build_qt(r'C:\Python27\python.exe C:\Python27\Lib\site-packages\PySide\scripts\uic.py', file_name, 'ui', file_name)


def build_res(file_name):
    build_qt(r'C:\Python27\Lib\site-packages\PySide\pyside-rcc.exe', file_name, 'qrc', file_name+'_rc')


def build():
    print 'building user interfaces...'
    build_ui('dialog')

    print 'building resources...'
    build_res('resources')


build()
