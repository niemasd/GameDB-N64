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
                if serial == 'NUS-NZGE / NZLE-USA': # manual fix for Ocarina of Time (only one with different notation)
                    serial = 'NUS-NZGE-USA / NZLE-USA'
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
        # manual fixes for missing serials
        if row_data['Title'] == 'Choro Q 64 2: Hachamecha Grand Prix Race':
            releases = [('NTSC-J', 'NUS-NCGJ-JPN', '24/12/99')]
        elif row_data['Title'] == 'Chōkūkan Night: Pro Yakyū King':
            releases = [('NTSC-J', 'NUS-NPKJ-JPN', '20/12/96')]
        elif row_data['Title'] == 'Chōkūkan Night: Pro Yakyū King 2':
            releases = [('NTSC-J', 'NUS-NP2J-JPN', '19/03/99')]
        elif row_data['Title'] == 'Dance Dance Revolution Disney Dancing Museum':
            releases = [('NTSC-J', 'NUS-NDFJ-JPN', '30/12/00')]
        elif row_data['Title'] == 'Densha de Go! 64':
            releases = [('NTSC-J', 'NUS-ND6J-JPN', '30/07/99')]
        elif row_data['Title'] == 'Derby Stallion 64':
            releases = [('NTSC-J', 'NUS-NDAJ-JPN', '10/08/01')]
        elif row_data['Title'] == 'Dezaemon 3D':
            releases = [('NTSC-J', 'NUS-CDZJ-JPN', '26/06/98')]
        elif row_data['Title'] == 'Sin and Punishment: Hoshi no Keishōsha':
            releases = [('NTSC-J', 'NUS-NGUJ-JPN', '21/11/00')]
        for region, serial, release_date_s in releases:
            assert serial != '?', "MISSING SERIAL: %s\n%s" % (row_data['Title'], releases)
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
