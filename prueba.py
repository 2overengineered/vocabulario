import re
import sqlite3
from unicodedata import normalize


def prueba_vocabulario(palabra, word, frase, sentence, palabra_alterna):
    print('type the missing word or phrase\n')
    print('\n')
    print(sentence)
    answer = input(re.sub(r'\b%s\b' % palabra,'_____', frase, flags=re.I) + '\n\n')
    
    if (normalize('NFC', answer).lower() == normalize('NFC', palabra).lower() or ((normalize('NFC', answer).lower()  == normalize('NFC', palabra_alterna).lower()) and answer)):
        print('correcto\n')
    else:
        print('incorrecto')
        print('\n')
        print(palabra)
        print(frase,'\n')
        print('type the entire phrase correctly 5 times')
        for i in range(1, 5):
            prueba_vocabulario_frase(palabra, word, frase, sentence, palabra_alterna)
        return (palabra, word, frase, sentence, palabra_alterna)

def prueba_vocabulario_frase(palabra, word, frase, sentence, palabra_alterna):
    print('type the ENTIRE sentence/phrase\n')
    print('\n')
    print(sentence)
    answer = input(re.sub(r'\b%s\b' % palabra,'_____', frase, flags=re.I) + '\n\n')
    if normalize('NFC', answer).lower() == normalize('NFC', frase).lower():
        print('correcto\n')
    else:
        print('incorrecto')
        print('\n')
        print(palabra)
        print(frase,'\n')
        prueba_vocabulario_frase(palabra, word, frase, sentence, palabra_alterna)
        
def add_incorrect_to_db(palabra, word, frase, sentence, palabra_alterna):
    # adds to incorrect_vocabulary.db sql database 5 times

    # connect to incorrect_vocabulary sql database
    conn = sqlite3.connect('incorrect_vocabulary.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vocabulary(id INTEGER PRIMARY KEY AUTOINCREMENT, palabra text, word text, frase text, sentence text, palabra_alterna text)''')
    
    
    # add each item in vocabulary_incorrect to sql database 5 times
    
    for i in range(0, 5):
        query = 'INSERT INTO vocabulary (palabra, word, frase, sentence, palabra_alterna) VALUES (?, ?, ?, ?, ?)'
        values = (palabra, word, frase, sentence, palabra_alterna)
        cursor.execute(query, values)
    conn.commit()
