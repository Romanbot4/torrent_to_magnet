import sys
import bencodepy
import hashlib
import base64
from os.path import exists

#download a file and return the local path
def download_file(url, file):
    import urllib.request
    urllib.request.urlretrieve(url, file)
    return file

# check whether a given link is local or network
def is_local(link):
    if link.startswith('http'):
        return False
    else:
        return True

def make_magnet_from_file(file) :
    metadata = bencodepy.decode_from_file(file)
    subj = metadata[b'info']
    hashcontents = bencodepy.encode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    name = subj[b'name']
    announce = metadata[b'announce']
    length = subj[b'files'][0][b'length']
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

link  = 'C:/Users/ticel/Downloads/onejav.com_abw178.torrent'
string = make_magnet_from_torrent(link)
print(string)