import os
import sys
from pathlib import Path
import zipfile
import logging


def unzip(source_file, dest_path):
    with zipfile.ZipFile(source_file, 'r') as zf:
        zipInfo = zf.infolist()
        for member in zipInfo:
            try:
                # 한글 decoding 해보고 아니면 말고
                member.filename = member.filename.encode('cp437').decode('euc-kr', 'ignore')
            except Exception as ex:
                logging.error(ex)
            
            zf.extract(member, dest_path)


def zip_archieve(ret_path, dir_and_files: list):
    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile(ret_path, mode="w")
    try:
        for item in dir_and_files:
            parent_path, _ = os.path.split(item)
            if os.path.isdir(item):
                # dir
                file_list, _ = get_file_list_by_extensions(item, None, ['*.*'])
                for file_path in file_list:
                    zf.write(file_path, file_path.replace(parent_path, ''), compress_type=compression)
            else:
                # file
                zf.write(item, item.replace(parent_path, ''), compress_type=compression)

    except FileNotFoundError as ex:
        logging.error(ex)
        raise ex
    finally:
        # Don't forget to close the file!
        zf.close()


def get_1_depth_sub_path_n_file_list_by_extensions(root_path, extensions):

    sub_path_n_file_list = []
    for dir in get_dir_list_by_depth(root_path, depth=1):
        root_path, sub_path = os.path.split(dir)

        files_list, _ = get_file_list_by_extensions(root_path, sub_path, extensions)

        sub_path_n_file_list.append((sub_path, files_list))

    return sub_path_n_file_list


def get_dir_list_by_depth(root_path, regex_pattern = None, depth = 1):
    '''
    n depth 까지 폴더를 가져온다.
    '''

    if os.path.exists(root_path) == False:
        return

    depth -= 1
    with os.scandir(root_path) as p:
        for entry in p:
            if entry.is_dir() == False:
                continue

            if regex_pattern == None:
                yield entry.path
            elif bool(search(regex_pattern, entry.path)):
                yield entry.path

            if depth > 0:
                yield from get_dir_list_by_depth(entry.path, depth=depth)


'''
@param extensions: a list of file types like [r'*.pdf', r'*.docx', r'*.htm', r'*.html']
'''
def get_file_list_by_extensions(root, child, extensions, exclude=[]):
    files_list = []
    sub_list = []
    if child == None:
        path = root
    else:
        path = os.path.join(root, child)
    
    #print('Searching ' + path)

    for type in extensions:
        for f in Path(path).rglob(type):
            if f.name[0] == '~':
                continue
            
            strf = str(f)

            is_exclude = False
            for exclude_path in exclude:
                if exclude_path in strf:
                    is_exclude = True
                    break
            
            if is_exclude:
                continue
            
            files_list.append(strf)
            
            if not str(f.parent) in sub_list:
                sub_list.append(str(f.parent))

    # files_list = [nfd2nfc(f) for f in files_list]   # 이거 때문에 괄호가 있는 파일을 못 찾아서 comment out 시킴
    # sub_list = [nfd2nfc(f) for f in sub_list]
    return files_list, sub_list


def convert_path_to_long_supported(path):
    '''
    윈도우를 사용할시에 path 길이가 길더라도 open을 이용할때 에러가 나지 않도록 path를 수정해준다.
    return "\\?\" + 절대경로 for windows
    '''

    prefix = os.path.sep + os.path.sep + '?' + os.path.sep

    if sys.platform in ['cygwin', 'win32']:
        # 파일명이 너무 길면 파일 생성이 안된다.
        # 하지만 위도우에서는 방법이 있지
        path = str(path)
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        
        if path.startswith(prefix) == True:
            return path

        return prefix + os.path.normpath(path)
    
    return path

def get_original_file_path_by_txt_file_path(root_path, txt_file_path):
    for p in Path(os.path.splitext(txt_file_path)[0]).parts:
        if r'-txt' in p:
            txt_dir = p
            sub_path = txt_dir.rstrip(r'-txt')
            break
    
    return os.path.join(root_path, sub_path, txt_file_path.split(txt_dir, 1)[-1].lstrip(r'\\')[:-4])

def get_original_file_path_by_xlsx_file_path(xlsx_file_path):
    # remove .xlsx -5
    # remove .txt - 4
    return xlsx_file_path[:-9]
