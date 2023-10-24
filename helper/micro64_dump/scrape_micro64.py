#! /usr/bin/env python3
'''
Scrape metadata from Micro64
'''
from bs4 import BeautifulSoup
from datetime import datetime
from os import makedirs
from os.path import abspath, expanduser
from sys import argv, stdout
from urllib.request import urlopen

URL = 'http://micro-64.com/database/masterlist.shtml'

# clean a string
def clean(s):
    return s.replace(chr(65533),'').replace(chr(0),'').replace(u'\xa0 ',u' ').replace(u'\xa0',u' ').strip()

# main program
if __name__ == "__main__":
    games_path = '%s/games' % '/'.join(abspath(expanduser(argv[0])).split('/')[:-3])
    soup = BeautifulSoup(urlopen(URL).read(), 'html.parser')
    header = [clean(v.text) for v in list(soup.find_all('thead'))[0].find_all('th')]
    for row in list(soup.find_all('tbody'))[0].find_all('tr'):
        cols = [clean(v.text) for v in row.find_all('td')]
        row_data = {header[i]:cols[i] for i in range(len(row)) if cols[i] not in {'','~'}}
        releases = list()
        for region, k1, k2 in [('NTSC-U', 'Product Code (NA)','NA Release'), ('PAL', 'Product Code (PAL)','PAL Release'), ('NTSC-J', 'Product Code (JP)','JP Release')]:
            if k1 in row_data:
                serial = row_data[k1]
                if k2 in row_data:
                    release_date_s = row_data[k2]
                else:
                    release_date_s = None
                if '/' in serial:
                    main_serial = serial.split('/')[0].strip()
                    releases.append((region, main_serial, release_date_s))
                    suffixes = [v.strip() for v in serial.split('/')[1:]]
                    for suffix in suffixes:
                        new_serial = main_serial[:-len(suffix)] + suffix
                        releases.append((region, new_serial, release_date_s))
                else:
                    releases.append((region, serial, release_date_s))
        for region, serial, release_date_s in releases:
            if release_date_s is None or release_date_s == '??/??/??':
                release_date = None
            else:
                try:
                    release_date = datetime.strptime(release_date_s, '%d/%B/%y').strftime('%Y-%m-%d')
                except:
                    try:
                        release_date = datetime.strptime(release_date_s[3:], '%B/%y').strftime('%Y-%m')
                    except:
                        release_date = str(int(release_date_s[6:]))
            game_path = '%s/%s' % (games_path, serial)
            makedirs(game_path, exist_ok=True)
            curr_data = {
                'title': row_data['Title'],
                'developer': row_data['Developer'],
                'publisher': row_data['Publisher'],
                'region': region,
            }
            if release_date is not None:
                curr_data['release_date'] = release_date
            if 'Rating' in row_data:
                curr_data['rating'] = row_data['Rating']
            for k, v in curr_data.items():
                f = open('%s/%s.txt' % (game_path, k), 'w'); f.write('%s\n' % v); f.close()
