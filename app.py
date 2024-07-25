import streamlit as st

from My_SQL_Connection import database_details, tables_in_this_DB, printing_tables, create_table_command,retrieve_result
from streamlit_option_menu import option_menu
from model_functions import LOAD_GEMMA,DeepSeekCoder
import torch
import mysql.connector

st.set_page_config(page_title="Querio Lingua", page_icon="🔍", layout="centered", initial_sidebar_state="expanded")


if 'localhost' not in st.session_state:
    st.session_state.localhost = ''
    st.session_state.user = ''
    st.session_state.password = ''
    st.session_state.table_commands = """ """

with st.sidebar:
    selected = option_menu("Speak2Sql💬", ["Log In", 'Database Querying','Chat with AI'],
                           icons=['person-circle', 'info-circle-fill', 'chat-fill'], menu_icon="cast", default_index=0,
                           styles={
                        "container": {"padding": "5!important","background-color":'gray'},
                        "icon": {"color": "white", "font-size": "23px"}, 
                        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "gray"},
                        "nav-link-selected": {"background-color": "#1B2135"},})

if selected == 'Log In':
    custom_style = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Curlz+MT&display=swap');
        .center-top-container {
            text-align: center;
            padding-top: 15vh; /* Adjust the top padding as needed */
        }
        .custom-title {
            font-family: 'Sans serif', cursive;
            font-size: 5em;
            font-style: italic;
            font-weight: bold;
            margin: 0; /* Remove default margin */
        }
        .custom-title .red-2 {
            color: red; /* Make the 2 red */
        }
    </style>
    """

    st.markdown(custom_style, unsafe_allow_html=True)

    st.markdown('<div class="center-top-container"><p class="custom-title">Speak<span class="red-2">2</span>SQL</p></div>', unsafe_allow_html=True)



    st.subheader('Please Log in into your MySql server by providing the following details ~ ')

    st.session_state.localhost = st.text_input("what is your host, (localhost if in local) or give the url", 'localhost',help='host')
    st.session_state.user = st.text_input("what is your user name (usually root)", 'root')
    st.session_state.password = st.text_input('Password', type='password')

elif selected == 'Database Querying':

    custom_style = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Curlz+MT&display=swap');
        .center-top-container {
            text-align: center;
            padding-top: 15vh; /* Adjust the top padding as needed */
        }
        .custom-title {
            font-family: 'Sans serif', cursive;
            font-size: 5em;
            font-style: italic;
            font-weight: bold;
            margin: 0; /* Remove default margin */
        }
        .custom-title .red-2 {
            color: red; /* Make the 2 red */
        }
    </style>
    """

    st.markdown(custom_style, unsafe_allow_html=True)
    st.markdown('<div class="center-top-container"><p class="custom-title">Speak<span class="red-2">2</span>SQL</p></div>', unsafe_allow_html=True)
    
    if st.button('All your databases ~ '):
        try:
            db, l = database_details(st.session_state.localhost, st.session_state.user, st.session_state.password)
            st.table(db)
        except mysql.connector.Error as e:
            error_code = e.errno
            st.warning(f"An error occurred (Error Code: {error_code}). Please check your login details.")


    st.subheader('Now we will see details of any database~ ')
    st.session_state.db_name = st.text_input('Which Database you want')

    if st.button('All tables present in that particular database'):
        if not st.session_state.db_name:
            st.warning('Input database name first')
        else:
            try:
                tables, l = tables_in_this_DB(st.session_state.localhost, st.session_state.user, st.session_state.password, st.session_state.db_name)
                st.write(f'There is only {l} tables present in this database')
                st.markdown(f"**:rainbow[{tables[0][0]}]**")
            except mysql.connector.Error as e:
                st.warning("An error occured. Please select the correct database from the above list or check that you are loged in into your server.")
    st.subheader('check out tables~ ')

    if st.button('Print the tables~'):
        try:
            tables_data = printing_tables(st.session_state.localhost, st.session_state.user, st.session_state.password, st.session_state.db_name)
            for table_name, table_data in tables_data.items():
                st.write(f"Table: {table_name}")
                st.table(table_data)
        except mysql.connector.Error as e:
            st.warning("An error occured. Please check that you have selected a database or have loged in into your server.")

    st.subheader('Retrieve the CREATE TABLE Statements')

    statement_options = st.radio("Choose the Context option for chat",["Generate the Context for chat AI based on your tables",
                                                                       "Give custom chat context"])
    if statement_options == 'Generate the Context for chat AI based on your tables':
        if st.button('Generate context'):
            try:
                statements = create_table_command(st.session_state.localhost, st.session_state.user, st.session_state.password, st.session_state.db_name)
                for table_name, table_statements in statements.items():
                    st.write(f'{table_name}')
                    st.session_state.table_commands = table_statements
                    st.code(table_statements)
            except mysql.connector.Error as e:
                st.warning('An error occured. Please check that you have selected a database or have loged in into your server.')
    elif statement_options == 'Give custom chat context':
        context = st.text_area("Paste your context here (Usually the tables schema)")
        st.session_state.table_commands = context


elif selected == 'Chat with AI':
    custom_style = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Curlz+MT&display=swap');
        .center-top-container {
            text-align: center;
            padding-top: 15vh; /* Adjust the top padding as needed */
        }
        .custom-title {
            font-family: 'Sans serif', cursive;
            font-size: 5em;
            font-style: italic;
            font-weight: bold;
            margin: 0; /* Remove default margin */
        }
        .custom-title .red-2 {
            color: red; /* Make the 2 red */
        }
    </style>
    """

    st.markdown(custom_style, unsafe_allow_html=True)
    st.markdown('<div class="center-top-container"><p class="custom-title">Speak<span class="red-2">2</span>SQL</p></div>', unsafe_allow_html=True)
    
    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "past" not in st.session_state:
        st.session_state["past"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "stored_session" not in st.session_state:
        st.session_state["stored_session"] = []

    def get_text():
        """
        Get the user input text.

        Returns:
            (str): The text entered by the user
        """
        input_text = st.text_input("You: ", st.session_state["input"], key="input",
                                placeholder="Your AI assistant here! Ask me anything ...", 
                                label_visibility='hidden')
        return input_text
    
    def new_chat():
        """
        Clears session state and starts a new chat.
        """
        save = []
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            save.append("User:" + st.session_state["past"][i])
            save.append("Bot:" + st.session_state["generated"][i])        
        st.session_state["stored_session"].append(save)
        st.session_state["generated"] = []
        st.session_state["past"] = []
        st.session_state["input"] = ""
    
    #with st.sidebar.expander("Available Fine Tuned Models", expanded=False):
    MODEL = st.sidebar.selectbox(label='Available Fine Tuned Models', options=['GEMMA-2B','DeepSeekCoder 1.3B'])
    st.sidebar.warning('Load only one model at a time as it loads the model into cache so it may cause cache overload',icon="⚠️")

    st.markdown("Your own SQL code helper🤖⭐ Powered by GEMMA & DeepSeek🚀")
    #st.markdown(" ")


    st.sidebar.button("New Chat", on_click = new_chat, type='primary')

    user_input = get_text()
    submit = st.button('submit',type='primary')
    
    if submit:
        if MODEL == 'GEMMA-2B':

            gemma_tokenizer,gemma_model = LOAD_GEMMA()
            device = torch.device("cpu")
            alpeca_prompt = f"""Below are sql tables schemas paired with instruction that describes a task. Using valid SQLite, write a response that appropriately completes the request for the provided tables.
            ### Instruction: {user_input}. ### Input: {st.session_state.table_commands}
                                ### Response:
                                """
            with st.status('Generating Result',expanded=False) as status:
                inputs = gemma_tokenizer([alpeca_prompt], return_tensors="pt").to(device)
                outputs = gemma_model.generate(**inputs, max_new_tokens=30)
                output = gemma_tokenizer.decode(outputs[0], skip_special_tokens=True)
                response_portion = output.split("### Response:")[-1].strip()

                st.session_state.past.append(user_input)  
                st.session_state.generated.append(response_portion)

                status.update(label="Result Generated!", state="complete", expanded=False)

        elif MODEL == 'DeepSeekCoder 1.3B':
            
            with st.status('Generating Result',expanded=False) as status:
                try:
                    response_portion = DeepSeekCoder(user_input,st.session_state.table_commands)
                    final_output = response_portion + f"\n {retrieve_result(st.session_state.localhost, st.session_state.user, st.session_state.password, st.session_state.db_name,response_portion)}"

                    st.session_state.past.append(user_input)  
                    st.session_state.generated.append(final_output)
                    print(final_output)
                except mysql.connector.Error as e:
                    
                    st.session_state.past.append(user_input)  
                    st.session_state.generated.append(response_portion + '{Query not executable}')

                status.update(label="Result Generated!", state="complete", expanded=False)


    download_str = []
    # Display the conversation history using an expander, and allow the user to download it
    with st.expander("Conversation", expanded=True):
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            st.info(st.session_state["past"][i],icon="🧐")
            st.success(st.session_state["generated"][i], icon="🤖")
            download_str.append(st.session_state["past"][i])
            download_str.append(st.session_state["generated"][i]) 

        # Can throw error - requires fix
        download_str = '\n'.join(download_str)
        if download_str:
            st.download_button('Download',download_str)

    # Display stored conversation sessions in the sidebar
    for i, sublist in enumerate(st.session_state.stored_session):
            with st.sidebar.expander(label= f"Conversation-Session:{i}"):
                st.write(sublist)

    # Allow the user to clear all stored conversation sessions
    if st.session_state.stored_session:   
        if st.sidebar.button("Clear-all"):
            del st.session_state.stored_session 