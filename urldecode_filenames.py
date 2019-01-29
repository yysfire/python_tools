#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: urldecode_filenames.py
Author: yysfire
Email: yysfire[at]gmail
Github: https://github.com/yysfire
Description: 将文件名中的URL转义字符解码，并重命名该文件，使其更具可读性。
"""

import os
import argparse
import sys
if sys.version_info < (3, 0):
    from urllib import unquote_plus as uq
else:
    from urllib.parse import unquote_plus as uq


def urldecode_filename(filepath):
    """将文件名中的URL转义字符解码，并重命名该文件.

    :filepath: string, 文件完整路径
    :returns: 布尔值，表示重命名是否成功

    """
    print('filepath:%s', filepath)
    if sys.version_info < (3, 0):
        newfilepath = uq(filepath)
    else:
        if sys.getfilesystemencoding() == 'mbcs':
            encoding = 'gbk'
        else:
            encoding = 'utf-8'
        newfilepath = uq(filepath, encoding=encoding)
    print('newfilepath:%s', newfilepath)
    try:
        os.rename(filepath, newfilepath)
        return True
    except Exception as e:
        print('{0}: {1}'.format(type(e), e))
        return False


def main():
    """批量重命名文件（将文件名中的URL转义符号解码成可读字符）
    :returns: None

    """
    parser = argparse.ArgumentParser(description='批量URL逆转义文件名并重命名')
    parser.add_argument(
        'filelist', metavar='str', nargs='+', type=str,
        help='文件完整路径'
    )
    args = parser.parse_args()
    print('args.filelist: %s', args.filelist)
    for f in args.filelist:
        urldecode_filename(f)


if __name__ == "__main__":
    main()
