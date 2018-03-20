import tableToJSON as ttj
import jsonToDB as jtd
import bubbleMap as bm
import lineGraph as lg
import sqlite3



def print_options():
    print('Options:')
    print('0. Quit\n'
          '1. Updated Table\n'
          '2. Select SQL\n'
          '3. Show Applications by City\n'
          '4. Show Applications by Date')


def choose_options():
    print_options()

    choice = int(input('Enter option:'))

    while choice != 0:
        if choice == 1:
            ttj.table_to_json(EXCEL_FILE_TO_USE)
            jtd.update_tables()

        elif choice == 2:
            try:
                conn = sqlite3.connect('applications.sqlite')
                c = conn.cursor()
                sql_select = input('Enter select statement: ')
                c.execute(sql_select)
                for row in c:
                    print(row)
                c.close()
                conn.close()
            except sqlite3.OperationalError as e:
                print('Sorry that was an invalid entry')
                print(e)
        elif choice == 3:
            bm.create_bubble_map()

        elif choice == 4:
            lg.create_line_graph()

        else:
            print('Invalid input')

        print_options()

        choice = input('Enter option:')
        choice = int(choice)


try:
    choose_options()
except ValueError:
    print("Invalid input")
    choose_options()






