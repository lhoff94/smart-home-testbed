import mpytool
import os


def init(port, baudrate=115200):
    conn = mpytool.ConnSerial(port=port, baudrate=baudrate)
    return mpytool.Mpy(conn)

def clean(mpy, entry_path=''):
    file_list = get_file_list(mpy, entry_path)
    for file in file_list:
        try:
            mpy.delete(file)
        except mpytool.mpy.PathNotFound:
            pass


def get_file_list(mpy, entry_path=''):
    file_list = []
    for entry in mpy.ls(entry_path):
        if not entry[1] == None:
            file_list.append(entry_path + entry[0])
        else:
            file_list.append('/' + entry[0])
            file_list.extend(get_file_list(mpy, entry[0] + '/'))
    return file_list

def copy_file(mpy, src_path, dest_path):
    with open(src_path, 'rb') as file:
        data = file.read()
        mpy.put(data, dest_path)

#def replace_all(mpy, path):
#    clean(mpy)
#    mpy.put(path, )
#    pass





board = init(port='/dev/ttyUSB0', baudrate=115200)

#clean(board)

#replace_all(board, '/home/lhoff/masterarbeit/smart-home-testbed/docker/micropython/mpy-client/new-mpy-payload/main.py')

copy_file(board,'/home/lhoff/masterarbeit/smart-home-testbed/docker/micropython/mpy-client/new-mpy-payload/main.py','.' )

print(get_file_list(board))


 