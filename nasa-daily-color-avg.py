from scipy import misc
from PIL import Image
from PIL import ImageDraw
import homeassistant.remote as remote
import urllib
import feedparser
import os

DOWNLOAD_FOLDER = '/home/homeassistant/.homeassistant/WWW/'
FEED_URL = 'http://www.nasa.gov/rss/lg_image_of_the_day.rss'

def get_latest_entry():
    feed = feedparser.parse(FEED_URL)
    return (feed.entries[0].enclosures[0].href, feed.entries[0].summary)

def download_file(url):
    remote_file = urllib.request.urlopen(url)
    local_name = 'daily-img.jpg'
    local_path = os.path.expanduser(os.path.join(DOWNLOAD_FOLDER, local_name))
    local_file = open(local_path, 'wb')
    local_file.write(remote_file.read())
    remote_file.close()
    local_file.close()
    return local_path

if __name__ == '__main__':
    if not os.path.exists(os.path.expanduser(DOWNLOAD_FOLDER)):
        os.makedirs(os.path.expanduser(DOWNLOAD_FOLDER))
    (url, text) = get_latest_entry()
    img_file = download_file(url)
    average = misc.imread(img_file).mean(axis=(0,1)).tolist()
    api = remote.API('127.0.0.1', 'Waterloo!')
    remote.call_service(api, 'light', 'turn_on', {'entity_id': 'group.all_lights', 'rgb_color': average})
    print(average)
