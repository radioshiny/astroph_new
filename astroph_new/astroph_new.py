from bs4 import BeautifulSoup as bs
from selenium import webdriver
from whoswho import who
import numpy as np
import time
import os
from datetime import datetime, date, timedelta
import pickle


def get_new(refresh: int = 30):
    # check duplicate
    recent = os.getcwd()+'/.newsub'
    if os.path.exists(recent):
        with open(recent, 'rb') as file:
            savtime, newsub = pickle.load(file)
        now = datetime.now()
        if int((now-savtime).total_seconds()) < refresh*60:
            print('There is a result which has got within refresh time.')
            return newsub

    # get astro-ph new page contents
    file = 'https://arxiv.org/list/astro-ph/new'
    browser = webdriver.Chrome()
    browser.get(file)
    _temp = bs(browser.page_source, 'html.parser')
    while True:
        time.sleep(5)
        soup = bs(browser.page_source, 'html.parser')
        if soup == _temp:
            break
        _temp = soup
    # page_source = browser.page_source
    browser.quit()
    # print('Done!')

    newsub = {}

    # get arXiv id
    id_tags = soup.find_all('span', {'class': 'list-identifier'})
    newsub['class'] = [i.text.replace(']', '').split(',')[0].replace(' from', ') ').replace('[pdf', '(new)').split()[1] for i in id_tags]
    newsub['link'] = ['https://arxiv.org{}'.format(i.find('a')['href']) for i in id_tags]

    # get title
    title_tags = soup.find_all('div', {'class': 'list-title mathjax'})
    newsub['title'] = [i.text[8:-1].replace('  ', ' ') for i in title_tags]

    # get author list
    author_tags = soup.find_all('div', {'class': 'list-authors'})
    author_tags = [i.find_all('a') for i in author_tags]
    newsub['author'] = []
    for iat in author_tags:
        authors = []
        for i in iat:
            authors.append(i.text)
        newsub['author'].append(authors)

    # get subject
    subject_tags = soup.find_all('div', {'class': 'list-subjects'})
    subject_tags = [i.text.split('(astro-ph.')[1:] for i in subject_tags]
    newsub['subject'] = []
    for ist in subject_tags:
        subjects = []
        for i in ist:
            subjects.append(i[:2])
        newsub['subject'].append(subjects)

    # get abstract
    abstract_tags = soup.find_all('p', {'class': 'mathjax'})
    newsub['abstract'] = [i.text.replace('\n', ' ').replace('  ', ' ').replace("`", "'") for i in abstract_tags]

    nrep = len(newsub['class']) - len(newsub['abstract'])
    for i in range(nrep):
        newsub['abstract'].append('')

    # Save temp data to prevent duplicates.
    savtime = datetime.now()
    with open(recent, 'wb') as file:
        pickle.dump((savtime, newsub), file)

    return newsub


def _init_params():
    with open('.params', 'w') as fp:
        fp.write('file: .interests\n')
        fp.write('show: open -a "Google Chrome"\n')
    return


def get_params(key: str = None):
    # init params
    if not os.path.exists('.params'):
        _init_params()

    # read params
    with open('.params', 'r') as fp:
        params = {}
        for line in fp.readlines():
            pkey, pval = [i.replace('\n', '').strip() for i in line.split(':', 1)]
            params[pkey] = pval

    if key is None:
        return params

    if not key in params.keys():
        raise KeyError(f"'{key}' is unknown parameter name.")

    return params[key]


def set_params(key: str, val: str):
    # get params
    params = get_params()

    # set params
    params[key] = val

    with open('.params', 'w') as fp:
        for key in params.keys():
            fp.write(f'{key}: {params[key]}\n')
    return


def read_interest(file: str = None):
    if file is None:
        file = get_params('file')

    interest = {}
    with open(file, 'r') as f:
        irk = ''
        for line in f.readlines():
            if line.startswith('=====  Interested '):
                irk = line.replace('=====  Interested ', '').split()[0][:-1].lower()
                interest[irk] = []
            else:
                line = line.rstrip()
                if len(line) > 0:
                    interest[irk].append(line)
    return interest


def _save_interest(interest, file: str = None):
    if file is None:
        file = get_params('file')

    rkey = ['subject', 'author', 'keyword']
    with open(file, 'w') as f:
        for irk in rkey:
            f.write(f'=====  Interested {irk.capitalize()}s  =====\n')
            interest[irk].sort()
            for item in interest[irk]:
                f.write(f'{item}\n')
            f.write('\n')
    # print(f"'{file}' was saved.")
    return None


def init_interest(file: str = None, default: bool = False, overwrite: bool = False):
    if file is None:
        file = get_params('file')

    if default:
        set_params('file', file)
        print(f"The default file name was changed to '{file}'.")

    if os.path.exists(file) and not overwrite:
        raise ValueError(f"'{file}' is already exist. Use add_interest() or remove_interest().")

    rkey = ['subject', 'author', 'keyword']
    with open(file, 'w') as f:
        for irk in rkey:
            f.write(f'=====  Interested {irk.capitalize()}s  =====\n\n')
    print(f"'{file}' was initialized.")
    return None


def add_interest(file: str = None, **kwargs):
    if len(kwargs) == 0:
        return
    
    if file is None:
        file = get_params('file')
    
    interest = read_interest(file)
    update = False

    for key in kwargs:
        if key not in ['subject', 'author', 'keyword']:
            raise KeyError(f"'{key}' is unknown key in the interest.")

        items = kwargs[key]
        if items is None:
            continue

        if type(items) is str:
            items = [items]

        for item in items:
            exist = False
            if key == 'author':
                for name in interest['author']:
                    if who.match(item, name):
                        exist = True
            else:
                if item in interest[key]:
                    exist = True
            if exist:
                print(f"'{item}' is already exist in the '{key}' list.")
            else:
                interest[key].append(item)
                update = True
                print(f"'{item}' is added to the '{key}' list.")
    if update:
        _save_interest(interest)
        print(f"'{file}' was updated.")
    else:
        print('Nothing changed!')
    return None


def remove_interest(file: str = None, **kwargs):
    if len(kwargs) == 0:
        return

    if file is None:
        file = get_params('file')

    interest = read_interest(file)
    update = False
    for key in kwargs:
        if key in ['subject', 'author', 'keyword']:
            items = kwargs[key]
            if items is None:
                continue
            if type(items) is str:
                items = [items]
            for item in items:
                if item in interest[key]:
                    interest[key].remove(item)
                    update = True
                    print(f"'{item}' is removed from the '{key}' list.")
                else:
                    print(f"'{item}' is not exist in the '{key}' list.")
        else:
            return KeyError(f"'{key}' is unknown key in the interest.")
    if update:
        _save_interest(interest)
        print(f"'{file}' was updated.")
    else:
        print('Nothing changed!')
    return None


def _get_search_score(scope, keys, kind=None, link=None):
    score = []
    for i, sub in enumerate(scope):
        score.append(0)
        for k in keys:
            if kind == 'subject':
                if k.upper() in sub:
                    score[i] = 1
            elif kind == 'author':
                for s in sub:
                    if who.match(k, s):
                        print(f"author '{s}' is found in the {kind} of [{i}] ({link[i]})")
                        score[i] += 1
            else:
                if f' {k}'.upper() in sub.upper():
                    print(f"keyword '{k}' is found in the {kind} of [{i}] ({link[i]})")
                    score[i] += 1
    return score


def _make_web_report(body):
    page_header = '<!DOCTYPE html>\n<html>\n' \
                  '<title>New Interested Submissions on Astrophysics in arXiv</title>\n' \
                  '<meta name="viewport" content="width=device-width, initial-scale=1">\n' \
                  '<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n' \
                  '<body>\n'
    page_footer = '\n</body>\n</html>'
    return page_header+body+page_footer


def search_new(file: str = None, cut: list = None, **kwargs):
    if file is None:
        file = get_params('file')

    if cut is None:
        cut = [1, 1, 1, 1]

    interest = read_interest(file)

    refresh = kwargs.pop('refresh') if 'refresh' in kwargs else 30
    newsub = get_new(refresh=refresh)

    # get score based on interest
    score = np.zeros((4, len(newsub['class'])), dtype=int)
    ikeys = ['subject', 'author', 'keyword', 'keyword']
    nkeys = ['subject', 'author', 'title', 'abstract']
    for i, (ikey, nkey) in enumerate(zip(ikeys, nkeys)):
        # print(i, ikey, nkey)
        score[i] = _get_search_score(newsub[nkey], interest[ikey], nkey, newsub['link'])

    # get mask from score
    masks = [(score[i] >= cut[i]) for i in range(4)]
    mask = np.sum(masks, axis=0)
    mask = mask > 1
    if np.all(~mask):
        print('There is no interested submission.')
        # return

    # print interested submissions
    idx = np.where(mask)[0].tolist()
    return newsub, idx


def make_report(prefix: str = 'astro-ph',
                datetag: bool = True,
                timetag: bool = False,
                show: bool = False, **kwargs):
    """
    Main function to make a summary report in HTML format from search results

    Parameters
    ----------
    prefix: str
        Prefix of the HTML file name for saving the summary report.
        Default is 'astro-ph'.

    datetag: bool
        If True, add a date tag to the end of the file name.
        Default is True.

    timetag:
        If True, add a time tag to the end of the file name.
        Default is False.

    show:
        If True, the report will be automatically opened in browser.
        Default is False.

    Returns
    -------
    None
    """
    file = kwargs.pop('file') if 'file' in kwargs else None
    cut = kwargs.pop('cut') if 'cut' in kwargs else None
    refresh = kwargs.pop('refresh') if 'refresh' in kwargs else 30
    newsub, idx = search_new(file=file, cut=cut, refresh=refresh)

    isub_html = '<div class="w3-panel">\n    <h2>New Interested Submissions on Astrophysics in arXiv</h2>\n'
    isub_html += '    <p>Update: {}</p>\n</div>\n'.format(datetime.now().strftime('%B %d, %Y (%H:%M)'))

    for i in idx:
        isub = ''
        sid = newsub['link'][i][-10:]
        isub += '<h3>{}</h3>\n'.format(newsub['title'][i])
        isub += '<p><span class="w3-text-pink"><a href="{}">arXiv:{}</a> '.format(newsub['link'][i], sid)
        isub += '[<a href="https://arxiv.org/pdf/{}">pdf</a>]</span> {} </p>\n'.format(sid, newsub['class'][i])
        isub += '<p><strong>{}</strong></p>\n'.format(', '.join(newsub['author'][i]))
        isub += '<p>{}</p>\n'.format(newsub['abstract'][i])
        isub_html += '<div class="w3-panel w3-leftbar w3-border-gray w3-hover-border-pink">\n{}\n</div>\n'.format(isub)

    isub_page = _make_web_report(isub_html)

    report_name = prefix
    if datetag:
        report_name += '_{}'.format(datetime.now().strftime('%Y%m%d'))
    if timetag:
        report_name += '_{}'.format(datetime.now().strftime('%H%M%S'))
    report_name += '.html'
    with open(report_name, 'w') as f:
        f.write(isub_page)
        print("'{}' was saved.".format(report_name))

    if show:
        _shell_command = get_params('show')
        _path = os.getcwd()
        os.system(f'{_shell_command} {_path}/{report_name}')

    return None


def run_apn(at: str = None, end: str = None, **kwargs):
    if at is None:
        at = '11:00'

    if end is None:
        today = date.today()
        end = today+timedelta(days=4)
        end = [end.year, end.month, end.day]
    else:
        if isinstance(end, str) and len(end) == 10:
            end = [int(i) for i in end.split('-')]
        else:
            raise ValueError("'end' should be given in 'yyyy-mm-dd' format.")

    at = [int(i) for i in at.split(':')]
    end_date = datetime(*end, 23, 59, 59)
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, *at)
    wait = int((start-now).total_seconds())
    if int(wait) < 0:
        make_report(**kwargs)
        start += timedelta(days=1)
        now = datetime.now()
        wait = int((start-now).total_seconds())
    remain = int((end_date-now).total_seconds())
    while remain > 0:
        print('Next searching: {}\nWaiting ...'.format(start.strftime('%Y-%m-%d %H:%M')))
        time.sleep(wait)
        make_report(**kwargs)
        start += timedelta(days=1)
        now = datetime.now()
        wait = int((start-now).total_seconds())
        remain = int((end_date-now).total_seconds())
    return

