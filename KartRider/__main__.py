import sys
from zipfile import ZipFile
from io import BytesIO
import argparse
import requests
from tqdm import tqdm

if __name__ == '__main__':

    def download_meta(file_dir):
        print('다운로드 준비 중...')
        url = 'https://static.api.nexon.co.kr/kart/latest/metadata.zip'
        res = requests.get(url, stream=True)

        tsize = int(res.headers.get('content-length', 0))
        bsize = 1024

        t = tqdm(total=tsize, unit='iB', unit_scale=True)

        zipdata = BytesIO()
        for data in res.iter_content(bsize):
            t.update(len(data))
            zipdata.write(data)

        t.close()
        res.close()

        if tsize != 0 and t.n != tsize:
            print('다운로드 실패')
            sys.exit(1)
        else:
            print(f'압축 해제 중.. {file_dir}')
            zipfile = ZipFile(zipdata)

            zipfile.extractall(file_dir)
            zipfile.close()
            zipdata.close()

            print(f'다운로드 성공')
            sys.exit(0)

    parser = argparse.ArgumentParser()

    key = ''
    parser.add_argument('-d', '--download',
                        metavar='DOWNLOAD_DIR', help='메타데이터 다운로드')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()

    if args.download is not None:
        download_meta(args.download)
