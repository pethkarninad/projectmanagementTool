import streamlit as st
import os
import sqlite3

def CreateDB():
    conn =sqlite3.connect('Strategy.db')

    c=conn.cursor()

    # create a table
    c.execute(""" CREATE TABLE IF NOT EXISTS strategy(
            strategy_name text,
            port_number integer,
            UNIQUE(strategy_name,port_number)
    """)

    conn.commit()


def AddData(name):
    if c.fetchone() not None: # checking if DB is not empty
        port=c.execute("SELECT MAX(port_number)) FROM strategy")  # retrieve max port number from Database
        c.execute(f"INSERT INTO strategy VALUES ({name},{port}+1)") # add new strategy to dabase with name and portnumber
        conn.commit() # commit changes to DB
    else:
        port=5001
        c.execute(f" INSERT INTO strategy VALUES ({name},{port})")
        conn.commit()
#-----------------------------------------------------------------------------------
def CreateProject(name): #create project

    #subprocess.run(["lean","create-project",name])
    if len(name)>0:
        st.session_state.count = 1
        command="lean create-project "+ name
        os.system(command)
        AddData(name) # Add information in Database about new strategy
        st.info("Project is created. Name: "+ name)
    else:st.info("Please enter a strategy name")
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

    if len(name)>0: # CHECK IF NAME IS ENTERED
        # CHECK IF PROJECT IS CREATED AND NAME IS IN THE DATABASE
        st.session_state.jupyter = 1
        c.execute("SELECT name FROM stregy WHERE name =?",(name,))
        check = c.fetchone()
        if check is None:
            st.info("Please create project before opening the research notebook") # add error message if you want
            # Question: should we set session state = 0 here since we did not created notebook?
        else:

            c.execute("SELECT port_number FROM strategy WHERE name =?",(name,))
            port_num = c.fetchone()
            jbook="lean research " + name + " --port "+ port_num 
            os.system(jbook) # where will this notebook open?

def main():
    createDB() # Initialize connection with Database

    st.title("NuFinTech Strategy Management")

    if 'count' not in st.session_state:
        st.session_state.count =0
    if 'bt' not in st.session_state:
        st.session_state.bt=0
    if 'jupyter' not in st.session_state:
        st.session_state.jupyter=0

    name = st.text_input("Please provide strategy name")

    create=st.button("Create Strategy",on_click=CreateProject,args=(name,))
    # Add a list of strategy names to run backtest
    bt=st.button("Backtest your strategy",on_click=Backtest,args=(name,))
    # dropdown for selecting strategy for creating their JNs
    jupyter =st.button("Open Research Notebook: ",on_click=OpenResearchBook,args=(name,))


    #st.write('count=',st.session_state.count)

if __name__ == '__main__':
    main()
