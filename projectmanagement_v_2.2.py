import sqlite3
import streamlit as st
import os
import time
import webbrowser


#webbrowser.open("http://streamlit.io")



conn =sqlite3.connect('Strategy.db')

c=conn.cursor()

# create a table
c.execute(""" CREATE TABLE IF NOT EXISTS strategy(
        strategy_name text UNIQUE,
        port_number integer UNIQUE)

""")

conn.commit()


def AddData(name):

    with sqlite3.connect('Strategy.db') as con:

        cur=con.cursor()
        cur.execute(" SELECT * FROM strategy")


        if cur.fetchone() is not None: # checking if DB is not empty
            cur.execute(" SELECT MAX(port_number) FROM strategy")
            ch=cur.fetchone()
            for a in ch: # ch is a tuple
                print(a)
                port = a + 1


            cur.execute(" INSERT INTO strategy (strategy_name,port_number) VALUES (?,?)",(name,port))
            #cur.commit()
        else:
            port=5001
            cur.execute(" INSERT INTO strategy (strategy_name,port_number) VALUES (?,?)", (name,port))
        con.commit()

def CreateProject(name): #create project

    with sqlite3.connect('Strategy.db') as con:
        cur=con.cursor()
    #subprocess.run(["lean","create-project",name])
        if len(name)>0:
            st.session_state.count = 1
            # Check if name already exists in DATABASE
            cur.execute("SELECT strategy_name FROM strategy WHERE strategy_name =?",(name,))
            check = cur.fetchone()

            if check is None:
                command="lean create-project "+ name
                os.system(command)
                AddData(name) # Add information in Database about new strategy
                st.info("Project is created. Name: "+ name)
            else:st.info("This strategy name already exists. Please enter another name.")
        else:st.info("Please enter a strategy name")
        con.commit()
    # add name to the database.


def Backtest(name):
    #subprocess.run(["lean","backtest",name])

    if len(name)>0:
        st.session_state.bt=1
        backtest="lean backtest " + name
        os.system(backtest)
        st.write("Backtest Performed!")
    else:st.info("Please enter a strategy name")

def OpenResearchBook(name):

    placeholder=st.empty()
    with sqlite3.connect('Strategy.db') as con:

        cur=con.cursor()

        if len(name)>0: # CHECK IF NAME IS ENTERED
            # CHECK IF PROJECT IS CREATED AND NAME IS IN THE DATABASE
            st.session_state.jupyter = 1
            cur.execute("SELECT strategy_name FROM strategy WHERE strategy_name =?",(name,))
            check = cur.fetchone()
            if check is None:
                st.info("Please create project before opening the research notebook") # add error message if you want
                # Question: should we set session state = 0 here since we did not created notebook?
            else:

                cur.execute("SELECT port_number FROM strategy WHERE strategy_name =?",(name,))
                ch = cur.fetchone()

                for a in ch: # ch is a tuple

                    port_num = a

                jbook="lean research " + name + " --port "+ str(port_num)+"&"
                os.system(jbook) # where will this notebook open?
                time.sleep(5)
                url="http://strat1-nufintech-bom4.belugacdn.com:"+ str(port_num)
                #webbrowser.open_new_tab(url)
                with placeholder.container():
                    st.write("Click [open link](%s)" % url)
    placeholder.empty()

    con.commit()

def DisplayDB():

    with sqlite3.connect('Strategy.db') as con:

        cur=con.cursor()

        st.session_state.db=1
        cur.execute("SELECT * FROM Strategy")
        data=cur.fetchall()

        print("Displaying Database")
        for row in data:
            print(row)

        con.commit()


def main():

    st.title("NuFinTech Strategy Management")

    if 'count' not in st.session_state:
        st.session_state.count =0
    if 'bt' not in st.session_state:
        st.session_state.bt=0
    if 'jupyter' not in st.session_state:
        st.session_state.jupyter=0
    if 'db' not in st.session_state:
        st.session_state.db=0
    name = st.text_input("Please provide strategy name")

    create=st.button("Create Strategy",on_click=CreateProject,args=(name,))


    database = st.button("Display Database",on_click=DisplayDB)


    with sqlite3.connect('Strategy.db') as con:

        cur=con.cursor()
        cur.execute("SELECT strategy_name FROM strategy")
        ch = cur.fetchall()
        strat_names =[]
        strat_names.append("SELECT")
        for a in ch:

            strat_names.append(a[0])

        print(strat_names)
        option = st.selectbox("Select a project for backtesting or to launch research book",sorted(strat_names))
        st.write("You selected:", option)

    # Add a list of strategy names to run backtest
    bt=st.button("Backtest your strategy",on_click=Backtest,args=(option,))
    # dropdown for selecting strategy for creating their JNs
    jupyter =st.button("Open Research Notebook",on_click=OpenResearchBook,args=(option,))
    #con.commit()


if __name__ == '__main__':
    main()
