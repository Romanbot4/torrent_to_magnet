import sys
import bencodepy
import hashlib
import base64
from os.path import exists
import urllib.request

def download_file(url, file):
    urllib.request.urlretrieve(url, file)
    return file

def is_local(link):
    if link.startswith('http'):
        return False
    else:
        return True

def _get_length(subj):
    if b'length' in subj:
        return subj[b'length']
    elif b'files' in subj:
        return sum([_get_length(f[b'path']) for f in subj[b'files']])
    else:
        return 0

def _get_name(subj):
    if b'name' in subj:
        return subj[b'name']
    else:
        return ''

def make_magnet_from_file(file) :
    metadata = bencodepy.decode_from_file(file)
    subj = metadata[b'info']
    hashcontents = bencodepy.encode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    name = _get_name(subj)
    announce = metadata[b'announce']
    length = _get_length(subj)
    return 'magnet:?'\
             + 'xt=urn:btih:' + b32hash.decode()\
             + '&dn=' + name.decode()\
             + '&tr=' + announce.decode()\
             + '&xl=' + str(length)

# convert a torrent file to magnet link
def make_magnet_from_torrent(torrent):
    if(is_local(torrent)):
        return make_magnet_from_file(torrent)
    else:
        return make_magnet_from_file(download_file(torrent, 'temp.torrent'))

link  = 'https://releases.ubuntu.com/21.10/ubuntu-21.10-desktop-amd64.iso.torrent?_ga=2.201817617.1652849701.1639329806-1115114217.1639329806'
string = make_magnet_from_torrent(link)
print(string)