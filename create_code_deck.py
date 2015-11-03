from anki import storage
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os
import os.path

PATH = '/home/idms/helpdesk'
DECK_NAME = 'helpdesk'
REPLACE_PART = '/home/idms/'


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



col = storage.Collection('/home/idms/Documents/Anki/User 1/collection.anki2')

FORBIDDEN_FILES = ['login.pl', ]

g = os.walk(PATH)

qty = 0

for path,_, files in g:
    if not '.svn' in path:
        print path, files
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

                    # and not
                    ]:
            qty += 1
            print 'Trying: %s   %s' % (qty, filename)
            try:
                lexer = get_lexer_for_filename(filename)
            except:
                lexer = get_lexer_by_name('text')
            full_filename = os.path.join(path, filename)
            with open(full_filename) as f:
                data = f.read()
            code = highlight(data, lexer, HtmlFormatter())
            save_to_deck(path, full_filename.replace(REPLACE_PART, ''), code)


col.close()