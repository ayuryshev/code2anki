import os
import sys
from anki import storage
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.formatters import HtmlFormatter



def save_to_deck(path, filename, code):
    deck_name = path.replace(REPLACE_PART, '').replace('/', '::')
    did = col.decks.id(deck_name)
    mdl_id = col.models.byName('Code')['id']
    col.conf['curModel'] = mdl_id
    note = col.newNote()
    note['Filename'] = filename
    note['Code'] = code
    note['Notes'] = ''
    note.model()['did'] = did
    col.addNote(note)
    col.save()


PATH = '/home/isk/github.com/skycoin/src/skywire'
DECK_NAME = 'skywire'
REPLACE_PART = '/home/isk/github.com/skycoin/src'

# TODO: change to env var
col = storage.Collection('/home/isk/.local/share/Anki2/User 1/collection.anki2')

FORBIDDEN_FILES = ['skywire-node', 'skywire-cli', 'go.sum', 'go.mod' ]
# IGNORED_DIRS="apps cmd"

g = os.walk(PATH)

qty = 0

for path,_, files in g:
    if not '.git' in path:
        print(f"Entering: {path}, see {files[:5]}")
        for filename in [fname for fname in files
                    if not fname.endswith('.pyc')
                    and not fname.startswith('.')
                    and not fname in FORBIDDEN_FILES
                    and not fname.endswith('.gif')
                    and not fname.endswith('.png')
                    and not fname.endswith('.jpg')
                    and not fname.endswith('.min.js')
                    and not fname.endswith('.xlsx')
                    and not fname.endswith('.rtf')
                    and not fname.endswith('.db')
                    # and not
                    ]:
            qty += 1
            if qty>900: 
                print(f'qty = {qty}')
                break
            print(f'Trying: {qty}   {filename}\n')
            try:
                lexer = get_lexer_for_filename(filename)
            except:
                lexer = get_lexer_by_name('text')
            full_filename = os.path.join(path, filename)
            try:
                with open(full_filename) as f:
                    data = f.read()
                    code = highlight(data, lexer, HtmlFormatter())
                    print(code[:128])
            except:
                print (sys.exc_info()[2])
                            

            save_to_deck(path, full_filename.replace(REPLACE_PART, ''), code)

col.close()