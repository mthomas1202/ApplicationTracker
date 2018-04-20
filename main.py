import tableToJSON as ttj
import jsonToDB as jtd
import bubbleMap as bm
import lineGraph as lg
import wordCloud as wc
import emails as em
import sqlite3



def print_options():
    print('Options:')
    print('0. Quit\n'
          '1. Update Table\n'
          '2. Select SQL\n'
          '3. Show Applications by City\n'
          '4. Show Applications by Date\n'
          '5. Show Positon WordCloud\n'
          '6. Check for Status Updates\n'
          '7. Delete Table\n'
          '8. Update SQL')


def choose_options():
    print_options()
    try:
        choice = int(input('Enter option:'))
    except ValueError:
        print("Invalid Input")
        choose_options()

    while choice != 0:
        if choice == 1:
            ttj.table_to_json('Application Table.xlsx')
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

        elif choice == 5:
            wc.generate_wordcloud()
        elif choice == 6:
            em.check_emails()
        elif choice == 7:
            choice = input("Are you sure you want to delete the database? (Y/N)")
            if choice.upper() == "Y":
                choice = inpute("Last chance (Y/N)")
                if choice.upper() == "Y":
                    conn = sqlite3.connect('applications.sqlite')
                    c = conn.cursor()
                    jtd.delete_tables(c)
                    c.close()
                    conn.commit()
                    conn.close()
        elif choice == 8:
            try:
                conn = sqlite3.connect('applications.sqlite')
                c = conn.cursor()
                sql_update = input('Enter update statement: ')
                c.execute(sql_update)
                conn.commit()
                c.close()
                conn.close()
            except sqlite3.OperationalError as e:
                print('Sorry that was an invalid entry')
                print(e)
        else:
            print('Invalid input')

        print_options()

        choice = input('Enter option:')
        choice = int(choice)


choose_options()








