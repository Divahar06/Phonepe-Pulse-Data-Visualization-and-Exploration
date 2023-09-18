# Phonepe-Pulse-Data-Visualization-and-Exploration
PhonePe Pulse Data Viz: Explore PhonePe's fintech data with interactive charts &amp; maps. Built with Python, Pandas, Streamlit, and Plotly. Gain insights on transactions, user behavior, and more!
# PhonePe Pulse Data Visualization

## Overview
This is a Streamlit web application for visualizing and exploring data from PhonePe Pulse, India's leading fintech platform. The app provides insights into transactions, user data, and more, using interactive charts and maps.

## Technologies Used
- Python
- Pandas
- MySQL
- mysql-connector-python
- Streamlit
- Plotly
- PIL (Python Imaging Library)
- Streamlit Option Menu (Custom Streamlit Component)

## Features

### Home
- Provides an overview of the application, domain, and technologies used.

### Top 10 Charts
- Allows users to explore top charts for transactions and users.
- Charts include:
  - Top 10 States by Total Transaction Amount
  - Top 10 Districts by Total Transaction Amount
  - Top 10 Pincodes by Transaction Percentage
  - Top 10 Phone Brands by Total Users
  - Top 10 Districts by Total Users
  - Top 10 Pincodes by User Percentage
  - Top 10 States by Total Users

### Geo Visualization
- Visualizes data on India's map.
- Users can choose to visualize transactions or user data.
- Charts include:
  - India Map: Total Transaction Amount by State
  - India Map: Total Transaction Count by State
  - India Map: Total App Opens by State

### Additional Data Exploration
- Provides additional insights into data.
- Users can explore payment types and state-wise data.
- Charts include:
  - Total Transaction Types and Amounts
  - State-wise Transaction Data
  - State-wise User Data

### About
- Provides information about PhonePe Pulse and PhonePe.
- Includes contact information for inquiries.

## How to Run
1. Make sure you have the required libraries installed (`pandas`, `mysql-connector-python`, `streamlit`, `plotly`, `PIL`, `streamlit-option-menu`).
2. Configure your MySQL connection parameters in the code.
3. Run the Streamlit application with the command `streamlit run app.py` (where `app.py` is your code file).

## Contact
For any questions, support, or suggestions, feel free to contact Divahar Murugan at divahar2896@gmail.com.

