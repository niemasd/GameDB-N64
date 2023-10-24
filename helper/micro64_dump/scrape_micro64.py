#! /usr/bin/env python3
'''
Scrape metadata from Micro64
'''
from bs4 import BeautifulSoup
from datetime import datetime
from os import makedirs
from os.path import abspath, expanduser, isdir
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
        elif row_data['Title'] == 'Doom 64':
            releases = [('NTSC-U', 'NUS-NDME-USA', '04/04/97'), ('PAL', 'NUS-NDMP-UKV', '02/12/97'), ('NTSC-J', 'NUS-NDMJ-JPN', '01/08/97')]
        elif row_data['Title'] == 'Doraemon: Nobita to Mittsu no Seirei Ishi':
            releases = [('NTSC-J', 'NUS-NDRJ-JPN', '21/03/97')]
        elif row_data['Title'] == 'Doraemon 2: Nobita to Hikari no Shinden':
            releases = [('NTSC-J', 'NUS-ND2J-JPN', '11/12/98')]
        elif row_data['Title'] == 'Doraemon 3: Nobita no Machi SOS!':
            releases = [('NTSC-J', 'NUS-N3DJ-JPN', '28/07/00')]
        elif row_data['Title'] == 'Eikō no Saint Andrews':
            releases = [('NTSC-J', 'NUS-NSTJ-JPN', '29/11/96')]
        elif row_data['Title'] == 'Famista 64':
            releases = [('NTSC-J', 'NUS-NFSJ-JPN', '28/11/97')]
        elif row_data['Title'] == 'Fushigi no Dungeon: Fūrai no Shiren 2: Oni Shūrai! Siren-jō!':
            releases = [('NTSC-J', 'NUS-NSIJ-JPN', '27/12/00')]
        elif row_data['Title'] == 'Getter Love!!':
            releases = [('NTSC-J', 'NUS-NGLJ-JPN', '04/12/98')]
        elif row_data['Title'] == 'Goemon Mononoke Sugoroku':
            releases = [('NTSC-J', 'NUS-NGPJ-JPN', '25/12/99')]
        elif row_data['Title'] == 'Hamster Monogatari 64':
            releases = [('NTSC-J', 'NUS-NHSJ-JPN', '06/04/01')]
        elif row_data['Title'] == 'Heiwa Pachinko World 64':
            releases = [('NTSC-J', 'NUS-NHPJ-JPN', '28/11/97')]
        elif row_data['Title'] == 'Ide Yōsuke no Mahjong Juku':
            releases = [('NTSC-J', 'NUS-NIMJ-JPN', '21/04/00')]
        elif row_data['Title'] == 'J-League Dynamite Soccer 64':
            releases = [('NTSC-J', 'NUS-NDSJ-JPN', '05/09/97')]
        elif row_data['Title'] == 'J-League Eleven Beat 1997':
            releases = [('NTSC-J', 'NUS-NJEJ-JPN', '24/10/97')]
        elif row_data['Title'] == 'J-League Live 64':
            releases = [('NTSC-J', 'NUS-NJLJ-JPN', '28/03/97')]
        elif row_data['Title'] == 'J-League Tactics Soccer':
            releases = [('NTSC-J', 'NUS-NSJJ-JPN', '15/01/99')]
        elif row_data['Title'] == 'Jangō Simulation Mahjong-dō 64':
            releases = [('NTSC-J', 'NUS-NMAJ-JPN', '25/07/97')]
        elif row_data['Title'] == 'Jikkyō GI Stable':
            releases = [('NTSC-J', 'NUS-NGSJ-JPN', '28/04/99')]
        elif row_data['Title'] == 'Jikkyō J. League: Perfect Striker':
            continue # the serial exists for 'International Superstar Soccer 64': https://gamefaqs.gamespot.com/n64/944295-jikkyou-jleague-perfect-striker/data
        elif row_data['Title'] == 'Jikkyō Powerful Pro Yakyū 4':
            releases = [('NTSC-J', 'NUS-NP4J-JPN', '14/03/97')]
        elif row_data['Title'] == 'Jikkyō Powerful Pro Yakyū 5':
            releases = [('NTSC-J', 'NUS-NJ5J-JPN', '26/03/98')]
        elif row_data['Title'] == 'Jikkyō Powerful Pro Yakyū 6':
            releases = [('NTSC-J', 'NUS-NP6J-JPN', '25/03/99')]
        elif row_data['Title'] == 'Jikkyō Powerful Pro Yakyū 2000':
            releases = [('NTSC-J', 'NUS-NPAJ-JPN', '29/04/00')]
        elif row_data['Title'] == 'Jikkyō Powerful Pro Yakyū Basic-ban 2001':
            releases = [('NTSC-J', 'NUS-NPEJ-JPN', '29/03/01')]
        elif row_data['Title'] == 'Jinsei Game 64':
            releases = [('NTSC-J', 'NUS-NJGJ-JPN', '19/03/99')]
        elif row_data['Title'] == 'Kira tto Kaiketsu! 64 Tanteidan':
            releases = [('NTSC-J', 'NUS-N64J-JPN', '23/10/98')]
        elif row_data['Title'] == 'Last Legion UX':
            releases = [('NTSC-J', 'NUS-NLLJ-JPN', '28/03/99')]
        elif row_data['Title'] == "Masters '98: Haruka Naru Augusta":
            releases = [('NTSC-J', 'NUS-NM9J-JPN', '26/12/97')]
        elif row_data['Title'] == 'New Japan Pro Wrestling: Tōhkon Road Brave Spirits':
            releases = [('NTSC-J', 'NUS-NTOJ-JPN', '04/01/98')]
        elif row_data['Title'] == 'New Japan Pro Wrestling: Tōhkon Road Brave Spirits 2, The Next Generation':
            releases = [('NTSC-J', 'NUS-NT3J-JPN', '26/12/98')]
        elif row_data['Title'] == 'Sin and Punishment: Hoshi no Keishōsha':
            releases = [('NTSC-J', 'NUS-NGUJ-JPN', '21/11/00')]
        for region, serial, release_date_s in releases:
            assert serial != '?', "MISSING SERIAL: %s\n%s" % (row_data['Title'], releases)
            if release_date_s is None or release_date_s == '??/??/??':
                release_date = None
            else:
                try:
                    release_date = datetime.strptime(release_date_s, '%d/%m/%Y').strftime('%Y-%m-%d')
                except:
                    try:
                        release_date = datetime.strptime(release_date_s, '%d/%m/%y').strftime('%Y-%m-%d')
                    except:
                        try:
                            release_date = datetime.strptime(release_date_s[3:], '%m/%y').strftime('%Y-%m')
                        except:
                            tmp = int(release_date_s.split('/')[-1])
                            if tmp < 30:
                                tmp += 2000
                            else:
                                tmp += 1900
                            release_date = str(tmp)
            game_path = '%s/%s' % (games_path, serial)
            assert not isdir(game_path), "PATH EXISTS: %s" % game_path
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
