# Importing Libraries
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image


# Creating connection with mysql workbench to access the data in phonepe database

mydb = sql.connect(host="localhost",
                   user="root",
                   password="1234",
                   database="phonepe"
                   )
mycursor = mydb.cursor(buffered=True)



# Setting up page configuration

icon = Image.open("C:\\Users\\DIVAHAR\\PycharmProjects\\P18_1\\phonepe\\ICN.png")
st.set_page_config(page_title="Phonepe Pulse Data Visualization ",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded",)

st.sidebar.header(" Welcome to Phonepe Pulse Data Visualization")
st.sidebar.subheader(" Use the below options to explore the data")



# Creating options menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Top 10 Charts", "Geo Visualization", "Additional Data exploration","About"],
                           icons=["house", "graph-up-arrow", "graph-up-arrow","rocket", "exclamation-circle"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px",
                                                "--hover-color": "#000080"},
                                   "nav-link-selected": {"background-color":  "#89CFF0"}})

# In[ ]:


# MENU 1 - HOME
if selected == "Home":
    st.markdown("# :blue[Data Visualization and Exploration]")
    st.markdown("## :blue[A User-Friendly Tool Using Streamlit and Plotly]")
    st.write(" ")
    st.write(" ")
    st.markdown("### :blue[Domain :] Financial Tech")
    st.markdown(
    "### :blue[Technologies Used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
    st.markdown(
    "### :blue[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")

# MENU 2 - TOP CHARTS
if selected == "Top 10 Charts":
    st.markdown("## :blue[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with col2:
        st.info(
            """
            #### From this section we can get the below insights:
            01) When Type = Transactions option :
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total value of transaction and Total amount transferred on phonepe.
            02) When Type = Users option:
            - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage based on the how many people use phonepe.
            """,
        )

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        ### Top 10 States Transactions
        st.header(":blue[State Wise Details]")
        st.subheader(" :blue[Top 10 States Transaction total Amount]")

        if Year == 2023 and Quarter in [3, 4]:
            st.markdown("#### Sorry No Data to Display for 2023 Qtr 3,4")
        else:
            mycursor.execute(
                f"""SELECT state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total 
                FROM df_agg_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY Total DESC LIMIT 10""")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])

            # Create a bar chart with the Viridis color scheme
            fig = px.bar(df, x='State', y='Total_Amount', color='State',
                         title='Top 10 States',
                         labels={'State': 'State', 'Total_Amount': 'Total Amount'},
                         hover_data={'Total_Amount': ':,.2f', 'Transactions_Count': ':,.0f'},
                         color_discrete_sequence=px.colors.sequential.Viridis)

            # Set the height of the chart (adjust this value as needed)
            fig.update_layout(height=600)

            # Add data labels inside each bar with bold, larger font, Rupee symbol, and comma separator
            fig.update_traces(texttemplate='₹%{y:,.2f}<b>', textposition='inside',
                              textfont=dict(size=18, color='black'))

            # Increase the size of the text for the entire chart
            fig.update_layout(font=dict(size=20))

            st.plotly_chart(fig, use_container_width=True)


        ### Top 10 Districts Transactions

        st.header(":blue[District Wise Details]")
        st.subheader(":blue[Top 10 Districts Transaction Total Amount]")

        if Year == 2023 and Quarter in [3, 4]:
            st.markdown("#### Sorry No Data to Display for 2023 Qtr 3,4")
        else:
            mycursor.execute(
                f"""SELECT district, sum(Count) as Total_Count, sum(Amount) as Total FROM df_map_trans WHERE year = {Year} 
                AND quarter = {Quarter} GROUP BY district ORDER BY Total DESC LIMIT 10""")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            # Create a bar chart with the Agsunset color scheme
            fig = px.bar(df, x='District', y='Total_Amount', color='District',
                         title='Top 10 Districts',
                         labels={'District': 'District', 'Total_Amount': 'Total Amount'},
                         hover_data={'Total_Amount': ':,.2f', 'Transactions_Count': ':,.0f'},
                         color_discrete_sequence=px.colors.sequential.Viridis)  # Set the color scheme

            # Set the height of the chart (adjust this value as needed)
            fig.update_layout(height=600)

            # Add data labels inside each bar with bold, larger font, Rupee symbol, and comma separator
            fig.update_traces(texttemplate='₹%{y:,.2f}<b>', textposition='inside',
                              textfont=dict(size=18, color='black'))

            # Increase the size of the text for the entire chart
            fig.update_layout(font=dict(size=20))

            st.plotly_chart(fig, use_container_width=True)


        # Top 10 Pincode Transactions

        st.header(":blue[Pincode]")
        st.subheader(":blue[Top 10 Pincode Transaction Percentage]")

        if Year == 2023 and Quarter in [3, 4]:
            st.markdown("#### Sorry No Data to Display for 2023 Qtr 3,4")
        else:
            mycursor.execute(
                f"""select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total 
                from df_top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10""")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='Pincode',
                         title='Top 10 Pincodes',
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            # Set the height of the chart (adjust this value as needed)
            fig.update_layout(height=600)

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Top Charts - USERS
    if Type == "Users":
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            st.markdown("### :blue[Phone Brands]")
            st.markdown("#### Phone Brand Wise User Details:")
            if Year == 2023 and Quarter in [ 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 3,4")
            else:
                mycursor.execute(
                    f"""SELECT brands, SUM(count) AS Total_Count, ROUND(AVG(percentage)*100,2) AS Avg_Percentage
                     FROM df_agg_user WHERE year = {Year} AND quarter = {Quarter} GROUP BY brands ORDER BY Total_Count DESC LIMIT 10""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])

                # Create a vertical bar chart with the Viridis color scheme
                fig = px.bar(df, x='Brand', y='Total_Users', color='Avg_Percentage',
                             title='Top 10 Brands by Total Users',
                             labels={'Brand': 'Brand', 'Total_Users': 'Total Users',
                                     'Avg_Percentage': 'Average Percentage'},
                             color_continuous_scale=px.colors.sequential.Viridis)

                # Set the height of the chart (adjust this value as needed)
                fig.update_layout(height=600)

                # Add Avg_Percentage inside each bar with bold, larger font
                fig.update_traces(texttemplate='%{y}', textposition='inside',
                                  textfont=dict(size=18, color='black'))

                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :blue[District]")
            st.markdown("#### District Wise User Details:")
            if Year == 2023 and Quarter in [3, 4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 3,4")
            else:
                mycursor.execute(
                    f"""SELECT district, SUM(RegisteredUser) AS Total_Users, SUM(AppOpens) AS Total_Appopens FROM df_map_user 
                    WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total_Users DESC LIMIT 10""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
                df['Total_Users'] = df['Total_Users'].astype(float)

                # Create a vertical bar chart with the Rainbow color scheme
                fig = px.bar(df, x='District', y='Total_Users', color='Total_Users',
                             title='Top 10 Districts by Total Users',
                             labels={'District': 'District', 'Total_Users': 'Total Users',
                                     'Total_Appopens': 'Total App Opens'},
                             color_continuous_scale=px.colors.sequential.Viridis,
                             text='Total_Users',
                             hover_data=['District','Total_Appopens'])

                # Set the height of the chart (adjust this value as needed)
                fig.update_layout(height=600)
                # Customize the text font for Total_Users inside the bar to make it bold
                fig.update_traces(texttemplate='%{y}', textposition='inside',
                                  textfont=dict(size=18, color='black'))
                st.plotly_chart(fig, use_container_width=True)


        with col3:
            st.markdown("### :blue[Pincode]")
            st.markdown("#### Pincode Wise User Details:")
            if Year == 2023 and Quarter in [ 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 3,4")
            else:
                mycursor.execute(
                    f"""select Pincode, sum(RegisteredUser) as Total_Users from df_top_user 
                    where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
                fig = px.pie(df,
                             values='Total_Users',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Viridis,
                             hover_data=['Total_Users'])
                fig.update_layout(height=600)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.markdown("### :blue[State]")
            st.markdown("#### State Wise User Details:")
            if Year == 2023 and Quarter in [3, 4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 3,4")
            else:
                mycursor.execute(
                    f"""SELECT State, SUM(RegisteredUser) AS Total_Users, SUM(AppOpens) AS Total_Appopens FROM df_map_user
                     WHERE year = {Year} AND quarter = {Quarter} GROUP BY State ORDER BY Total_Users DESC LIMIT 10""")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
                df['Total_Users'] = df['Total_Users'].astype(float)

                # Create a bar chart
                fig = px.bar(df, x='State', y='Total_Users',color='Total_Users',
                             title='Top 10 States by Total Users',
                             labels={'State': 'State', 'Total_Users': 'Total Users',
                                     'Total_Appopens': 'Total App Opens'},
                             color_continuous_scale=px.colors.sequential.Viridis,
                             text='Total_Users',
                             hover_data=['State', 'Total_Users','Total_Appopens'])
                # Set the height of the chart (adjust this value as needed)
                fig.update_layout(height=600)
                # Customize the text font for Total_Users inside the bar to make it black
                fig.update_traces(texttemplate='%{y}', textposition='inside',
                                  textfont=dict(size=18, color='black'))
                st.plotly_chart(fig, use_container_width=True)

# MENU 3 - Geo Visualization
if selected == "Geo Visualization":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1, col2 = st.columns(2)

    st.info(
        """
        #### From this section we can get the below insights:
        01) When Type = Transactions option :
        - Overall State Data- It will display the total amount that is transferred in each state using Phonepe.
        - Overall State Data- It will display the total count of transactions in each state using Phonepe.
        02) When Type = Users option:
        - Overall State Data- It will display the total of number of times app was opened in each state.
        """,
    )

    # Geo Visualization - TRANSACTIONS
    if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP

            st.markdown("## :blue[Overall State Data - Transactions Amount]")
            mycursor.execute(
                f"""select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from df_map_trans 
                where year = {Year} and quarter = {Quarter} group by state order by state""")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv("C:/Users/DIVAHAR/phonepe/Statenames.csv")
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_amount',
                                color_continuous_scale='Rainbow')

            # Define the hovertemplate to format Total_amount
            fig.update_traces(hovertemplate='State: %{location}<br>' +
                                    'Total Amount: ₹%{z:,.2f}<extra></extra>',
                                    z=df1['Total_amount'].values)

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(height=700, geo=dict(bgcolor='lightblue'))

            st.plotly_chart(fig, use_container_width=True)


        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP

            st.markdown("## :blue[Overall State Data - Transactions Count]")
            mycursor.execute(
                f"""select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from df_map_trans 
                where year = {Year} and quarter = {Quarter} group by state order by state""")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv("C:/Users/DIVAHAR/phonepe/Statenames.csv")
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                color_continuous_scale='Rainbow')
            fig.update_traces(hovertemplate='State: %{location}<br>' +
                                            'Total Transactions: %{z:,.0f}<extra></extra>',
                              z=df1['Total_Transactions'].values)

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(height=700, geo=dict(bgcolor='lightblue'))
            st.plotly_chart(fig, use_container_width=True)

    # Geo Visualization - USERS
    if Type == "Users":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :blue[Overall State Data - User App opening frequency]")
        mycursor.execute(
            f"""select State, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from df_map_user
             where year = {Year} and quarter = {Quarter} group by State order by State""")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        df2 = pd.read_csv("C:/Users/DIVAHAR/phonepe/Statenames.csv")
        df1.Total_Appopens = df1.Total_Appopens.astype(int)
        df1.State = df2

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Appopens',
                            color_continuous_scale='Rainbow')
        fig.update_traces(hovertemplate='State: %{location}<br>' +
                                        'Total App Opens: %{z:,.0f}<extra></extra>',
                          z=df1['Total_Appopens'].values)

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(height=700, geo=dict(bgcolor='lightblue'))
        st.plotly_chart(fig, use_container_width=True)

# MENU 4 - Additional Data exploration

if selected == "Additional Data exploration":
    st.info(
        """
        #### From this section we can get the below insights:
        01) When Type = Transactions option :
        - Payment Type- It will display info with respect to different types of transaction .
        - State Type - It will give info about each disticts in each state.
        02) When Type = Users option:
        - Overall State Data- It will display the total of number of times app was opened in each state.
        """,)

    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    if Type == "Transactions":
        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :blue[Payment Type]")
        st.markdown("## :blue[Total Transaction with respect to Different type of transactions]")
        mycursor.execute(
            f"""select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount
             from df_agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type""")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Rainbow)
        hover_template = '<b>Total Transactions</b>: %{y:,.0f}<br>' + \
                         '<b>Total Amount</b>: ₹%{customdata:,.2f}'

        # Update hover template and customdata
        fig.update_traces(hovertemplate=hover_template, customdata=df['Total_amount'])

        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("## :blue[State Type]")
        st.markdown("## :blue[Gives information of each districts in a state]")
        st.markdown("## :blue[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman and nicobar islands', 'andhra pradesh', 'arunachal pradesh', 'assam',
                                       'bihar', 'chandigarh', 'chhattisgarh', 'dadra and nagar haveli and daman and diu',
                                       'delhi', 'goa', 'gujarat', 'haryana', 'himachal pradesh', 'jammu and kashmir',
                                       'jharkhand', 'karnataka', 'kerala','ladakh', 'lakshadweep',
                                       'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil nadu', 'telangana', 'tripura', 'uttar pradesh', 'uttarakhand',
                                       'west bengal'), index=30)

        mycursor.execute(
            f"""select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from df_map_trans
             where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district""")

        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                         'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Rainbow)

        # Define a custom hover template with line breaks <br> for each line
        hover_template = '<b>District</b>: %{x}<br>' + \
                         '<b>Total Transactions</b>: %{y:,.0f}<br>' + \
                         '<b>Total Amount</b>: ₹%{customdata:,.2f}'

        # Update hover template and customdata
        fig.update_traces(hovertemplate=hover_template, customdata=df1['Total_amount'])

        # Set the height of the chart
        fig.update_layout(height=700)

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)


    if Type == "Users":
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA
        st.markdown("## :blue[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman and nicobar islands', 'andhra pradesh', 'arunachal pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra and nagar haveli and daman and diu',
                                       'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal pradesh', 'jammu and kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil nadu', 'telangana', 'tripura', 'uttar pradesh', 'uttarakhand',
                                       'west bengal'), index=30)

        mycursor.execute(
            f"""select State,Year,Quarter,District,sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from df_map_user
             where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,Year,Quarter order by State,District""")

        df = pd.DataFrame(mycursor.fetchall(),
                          columns=['State', 'Year', 'Quarter', 'District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Rainbow)

        # Define a custom hover template with line breaks <br> for each line
        hover_template = '<b>District</b>: %{x}<br>' + \
                         '<b>Total Users</b>: %{y:,.0f}<br>' + \
                         '<b>Total App Opens</b>: %{customdata:,.0f}'

        # Update hover template and customdata
        fig.update_traces(hovertemplate=hover_template, customdata=df['Total_Appopens'])
        # Set the height of the chart
        fig.update_layout(height=700)

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

# MENU 4 - ABOUT
if selected == "About":
        st.write(" ")
        st.write(" ")
        st.markdown("### :blue[About PhonePe Pulse:] ")
        st.write(
            "##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")

        st.write(
            "##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")

        st.markdown("### :blue[About PhonePe:] ")
        st.write(
            "##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")

        st.markdown("### :blue[Contact:] ")
        st.write(
            """##### Feel free to customize and extend the script to suit your specific requirements.Contact For any questions, support, or suggestions, feel free to contact Divahar Murugan at divahar2896@gmail.com."""
        )



