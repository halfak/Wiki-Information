"""
Gathers general information about a set of wikis (???) via a call to
site_info and writes out to a TSV format that mysqlimport appreciates

Usage:
  get_wiki_info [--api=<url>]
  get_wiki_info -h | --help
  get_wiki_info --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --api=<url>   The API URL to connect to [default: https://en.wikipedia.org/w/api.php]
"""
import sys, types

import docopt
import requests

WIKI_URL_STUFF = "?action=sitematrix&format=json"

WIKI_VALUES = [
    'wiki',
    'code',
    'sitename',
    'url',
    'lang_id',
    'lang_code',
    'lang_name',
    'lang_local_name'
]

def main():
    args = docopt.docopt(__doc__, version="0.0.1")
    
    sys.stdout.write("\t".join(WIKI_VALUES))
    sys.stdout.write("\n")
    
    for wiki_info in get(args['--api']):
        
        sys.stdout.write("\t".join(encode(wiki_info[h]) for h in WIKI_VALUES))
        sys.stdout.write("\n")

def get(api_url):
    wiki_url = api_url + WIKI_URL_STUFF
    
    response = requests.get(wiki_url)
    
    doc = response.json()
    
    languages = doc['sitematrix'].items()
    
    for lang_id, language in languages:
        try:
            lang_id = int(lang_id) # fails for non-languages because dumb
        except:
            continue
        lang_code = language.get('code')
        lang_name = language.get('name')
        lang_local_name = language.get('localname')
        
        for wiki_info in language.get('site', []):
            wiki = wiki_info['dbname']
            code = wiki_info.get('code')
            url = wiki_info.get('url')
            sitename = wiki_info.get('sitename')
            closed = 'closed' in wiki_info
            
            yield {
                'wiki': wiki,
                'code': code,
                'sitename': sitename,
                'url': url,
                'lang_id': lang_id,
                'lang_code': lang_code,
                'lang_name': lang_name,
                'lang_local_name': lang_local_name
            }

def encode(val):
    if val == None:
        return "NULL"
    elif isinstance(val, str) or isinstance(val, bytes):
        if isinstance(val, bytes):
            val = str(val, 'utf-8', 'replace')
        
        val = val.replace("\t", "\\t").replace("\n", "\\n")
        
        return val
    else:
        return str(val)


if __name__ == "__main__": main()
