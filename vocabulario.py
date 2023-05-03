import csv
import sqlite3
import random
from time import time, sleep

from prueba import *

### 🗣️🇪🇸
    
def vocabulario(tiempo_prueba, datos_vocabulario):
    tiempo_inicio = time() # record initial time
    max_execution_time = 60*tiempo_prueba #max execution time in seconds
    
    vocabulary_incorrect_count = 0
    vocabulary_correct_count = 0
    
    vocabulary_incorrect = []
    
    
    while True:
    
        # Check the elapsed time
        elapsed_time = time() - tiempo_inicio
        if elapsed_time > max_execution_time:
            # Exit the program and print if the elapsed time exceeds the limit
            print('Sesión de práctica de vocabulario de {} minutos completada.'.format(tiempo_prueba))
            print('Completed {} minute vocabulary practice session.\n'.format(tiempo_prueba))
            sleep(1)
            
            print('{} out of {} correct ({}%)'.format(vocabulary_correct_count,vocabulary_incorrect_count + vocabulary_correct_count, round(100*(vocabulary_correct_count)/(vocabulary_incorrect_count + vocabulary_correct_count))))
            print('\n')
            sleep(1)
            
            
            if vocabulary_incorrect:
                print('Now, a retest of items that were incorrect from this session:\n')
                for vocabulary_row in vocabulary_incorrect:
                    prueba = prueba_vocabulario(vocabulary_row[0], vocabulary_row[1], vocabulary_row[2], vocabulary_row[3], vocabulary_row[4])
                    if prueba: vocabulary_incorrect.append(prueba)
            
            break

        # Otherwise, continue with program execution
        
        # connect to incorrect_vocabulary sql database
        conn = sqlite3.connect('incorrect_vocabulary.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vocabulary(id INTEGER PRIMARY KEY AUTOINCREMENT, palabra text, word text, frase text, sentence text, palabra_alterna text)''')
        
        # Count number of rows in incorrect_vocabulary sql database
        incorrect_vocabulary_row_count = cursor.execute('''SELECT COUNT(*) FROM vocabulary''').fetchall()[0][0]
        
        
        print(incorrect_vocabulary_row_count, 'rows in vocabulary_incorrect.db\n\n')
        
        # If there are less than 200 rows in incorrect_vocabulary sql database, quiz from data in .csv files, otherwise quiz from data in incorrect_vocabulary sql database
        if incorrect_vocabulary_row_count < 200:
            # Choose random filename fromn 'datos_vocabulario_active' set
            csv_filename = 'datos-vocabulario/' + random.choice(list(datos_vocabulario))
            print(csv_filename)
            
            # Determine number of rows in csv file and randomly choose a row index
            with open(csv_filename, encoding='utf8') as csv_file:
                
                # Read entire file into list
                with open(csv_filename, encoding='utf8') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

                    # Choose random row from list and quiz
                    random_row = random.choice(list(csv_reader))
                    print(random_row)
                    
                    prueba = prueba_vocabulario(random_row[0], random_row[1], random_row[2], random_row[3], random_row[4])
                    # if incorrect add to vocabulary_incorrect to sql database 5 times a and increment vocabulary_incorrect_count
                    if prueba:
                        vocabulary_incorrect.append(random_row)
                        add_incorrect_to_db(random_row[0], random_row[1], random_row[2], random_row[3], random_row[4])
                        vocabulary_incorrect_count += 1
                    # if increment vocabulary_correct_count
                    else: vocabulary_correct_count  += 1
        else:
                retest_query = 'SELECT palabra, word, frase, sentence, palabra_alterna, id FROM vocabulary ORDER BY RANDOM() LIMIT 1'
                res = cursor.execute(retest_query)
                incorrect_retest_rows = res.fetchall()

                for random_row in incorrect_retest_rows:
                    prueba = prueba_vocabulario(random_row[0], random_row[1], random_row[2], random_row[3], random_row[4])
                    # if incorrect add to vocabulary_incorrect to sql database 5 times a and increment vocabulary_incorrect_count
                    if prueba:
                        vocabulary_incorrect.append(random_row)
                        add_incorrect_to_db(random_row[0], random_row[1], random_row[2], random_row[3], random_row[4])
                        vocabulary_incorrect_count += 1
                    # if increment vocabulary_correct_count
                    else:
                        vocabulary_correct_count  += 1
                        # remove row from vocabulary_incorrect to sql database if correct
                        cursor.execute('DELETE FROM vocabulary WHERE id = {}'.format(random_row[5]))
        conn.commit()
                    
            
        
# open file 'datos-vocabulario/datos-vocabulario-active.csv' that contains list of active vocabulary data filenames to read and add to set 'datos_vocabulario_active'
with open('datos-vocabulario/datos-vocabulario-active.csv', encoding='utf8') as f:
    datos_vocabulario_active = {row.strip() for row in f}
vocabulario(10, datos_vocabulario_active)
