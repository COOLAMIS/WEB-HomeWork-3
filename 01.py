import os, sys, shutil
#from threading import Thread
import logging
from concurrent.futures import ThreadPoolExecutor

CYRILLIC_SYMBOLS = "абвгґдеёєжзиіїйклмнопрстуфхцчшщъыьэюя"
TRANSLATION = ("a", "b", "v", "h", "g", "d", "e", "e", "ie" "zh", "z",
               "y", "i", "yi", "y", "j", "k", "l", "m", "n", "o", "p",
               "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch",
               "", "y", "", "e", "yu", "ya")

BAD_SYMBOLS = ("%", "*", " ", "-")

TRANS = {}
for c, t in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

for i in BAD_SYMBOLS:
    TRANS[ord(i)] = "_"


def normalize(name: str) -> str:
    trans_name = name.translate(TRANS)
    return trans_name




dict_file_extension = {'picure': ['JPEG', 'PNG', 'JPG', 'SVG'],
                       'video': ['AVI', 'MP4', 'MOV', 'MKV'],
                       'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                       'music': ['MP3', 'OGG', 'WAV', 'AMR'],
                       'archives': ['ZIP', 'GZ', 'TAR']
                       }

list_type_data = []
list_type_folder = []
threads = []
list_data_extension = set()
list_unknown_extension = set()

def move_data(path_i, root_path, name_category):
    target_dir = os.path.join(root_path, name_category)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    file_name = os.path.basename(path_i)
    file_name = os.path.splitext(file_name)[0]
    extension = path_i.split('.')[-1]
    file_move_name = target_dir +'\\' + normalize(file_name) + '.' + extension
    os.replace(path_i, file_move_name)
    extension = extension.upper()
    if extension in ('ZIP', 'GZ', 'TAR'):
        shutil.unpack_archive(file_move_name, os.path.join(target_dir, file_name))
            
def sort_extension(path_i):
    extension = path_i.split('.')[-1]
    extension = extension.upper()
    for key, list_exts in dict_file_extension.items():
        if extension in list_exts:
            list_data_extension.add(extension)
            return key
    list_unknown_extension.add(extension)
    return 'other'
    
def del_empty_data(path_i):
    os.rmdir(path_i)
    
def worker(folder):
    for i in os.listdir(folder):
        path_i = os.path.join(folder, i)
        if os.path.isfile(path_i):
            file_name = os.path.splitext(i)[0]          # получаем имя файла
            list_type_data.append(normalize(file_name))
            name_category = sort_extension(path_i)
            move_data(path_i, list_type_folder[0], name_category)
    #return list_type_data, list_data_extension, list_unknown_extension
    
def recursion_folder(root_path, sub_path=None):
    for i in os.listdir(sub_path if sub_path else root_path):
        path_i = os.path.join(sub_path if sub_path else root_path, i)
        if os.path.isdir(path_i):
            list_type_folder.append(path_i)
            if not os.listdir(path_i):
                del_empty_data(path_i)
            else:
                recursion_folder(root_path, path_i)
    # реализация пула потоков
    with ThreadPoolExecutor() as executor:
        for folder in list_type_folder:
            th = executor.submit(worker, folder)
            threads.append(th)
            
        [el.join() for el in threads]
        print('Finish programm')
        
def main():
    try:
        path = sys.argv[1]
        list_type_folder.append(path)
        logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    except IndexError:
        return "Take a path to folder as param"
    if not os.path.exists(path):
        return f"Path {path} does not axist"
    return recursion_folder(path)

if __name__ == '__main__':
    print(main())