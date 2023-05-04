import numpy as np
#import matplotlib.colors as mcolors
#import matplotlib.pyplot as plt
import openpyxl as op
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
#import plotly.figure_factory as ff
import streamlit as st  # pip install streamlit
import streamlit.components.v1 as components
#import altair as alt
import numpy as np
#import os
from pathlib import Path


st.set_page_config(
    page_title = "Everyone Can Support",
    page_icon = ":phone:",
    initial_sidebar_state="expanded",
    layout="wide",
)



def get_data_from_excel4():
    dfcsi = pd.read_excel(
        io="reports/csi/CSI NM14.xlsx",
        engine="openpyxl",
        sheet_name="CSI Spanish",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )

    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return dfcsi

def get_data_from_excel5():
    dfcsip = pd.read_excel(
        io="reports/csi/CSI NM14.xlsx",
        engine="openpyxl",
        sheet_name="CSI Portuguese",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )

    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return dfcsip

def get_data_from_excel6():
    dfcsie = pd.read_excel(
        io="reports/csi/CSI NM14.xlsx",
        engine="openpyxl",
        sheet_name="CSI English",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )

    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return dfcsie

def get_data_from_excel7():
    dfcsii = pd.read_excel(
        io="reports/csi/CSI NM14.xlsx",
        engine="openpyxl",
        sheet_name="CSI Indonesian",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )

    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return dfcsii



def get_data_from_excel8():
    dfass = pd.read_excel(
        io="reports/Assessment/nmass.xlsx",
        engine="openpyxl",
        sheet_name="Sheet1",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )

    # Add 'hour' column to dataframe
    #df["hour"] = pd.to_datetime(df["receiving time"]).dt.hour
    return dfass


dfg1 = get_data_from_excel4()
dfg2 = get_data_from_excel5()
dfg3 = get_data_from_excel6()
dfg4 = get_data_from_excel7()
dfg5 = get_data_from_excel8()


st.subheader("Welcome to support reports dashboard!")
st.sidebar.header("")

#st.write("https://www.buymeacoffee.com/ustyuzhaniX")
#st.sidebar.header("Choose here")

#file_dir = r'reports/general-dynamics'
#file_name = 'general-dynamics.csv'



df1 = pd.read_csv('reports/general-dynamics/general-dynamics.csv')






  # 👈 Add the caching decorator
def load_data(url):
    dft = pd.read_csv(url)
    return dft

dft = load_data("reports/time/time-2022-03-17_2023-03-17_1679031929.csv")

dft['hour'] = pd.to_datetime(dft['receiving time']).dt.hour
dft['date'] = pd.to_datetime(dft['receiving time']).dt.date

dft['date'] = dft['date'].apply(pd.to_numeric, errors='ignore')
dft['date'] = dft['date'].astype('str').str[-8:]


with st.expander("Heatmap"):

    with st.form("my_form1"):
        language = st.multiselect(
        "Select the language:",
        options=dft["language"].unique(),
        default=dft["language"].unique()
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            dft = dft.query(
                "language == @language"
                )
        else:
            pass

#dft = pd.read_csv('reports/time/time-2022-03-17_2023-03-17_1679031929.csv')


    def date_category(bad_date):
            if bad_date < '22-03-17':
                return 'date out of frame'
            else:
                return 'date on frame'

    dft['+date'] = dft['date'].apply(date_category)
    df5 = dft.loc[dft['+date'].isin(['date out of frame'])]
    df6 = dft.loc[dft['+date'].isin(['date on frame'])]

    tokens_by_csi = dft.groupby(by=["hour"]).count()[["ticket number"]]
    fig_tokens_by_csi = px.bar(
        tokens_by_csi,
        x=tokens_by_csi.index,
        y="ticket number",
        text="ticket number",
        title="<b>ticket number by hour</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_csi),
        template="plotly_white",
    )
    fig_tokens_by_csi.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    st.plotly_chart(fig_tokens_by_csi, use_container_width=True)






    st.text(f"Heatmap by date:")

    pivot = pd.pivot_table(df6, index='date', columns='hour', values='ticket number', aggfunc='count')
    pivot.fillna(0, inplace=True)
    mean_tickets_per_hour = pivot.values.mean()
    fig = px.imshow(pivot, color_continuous_scale="blues", aspect='auto')
    fig.update_layout(title=f"Mean tickets per hour: {mean_tickets_per_hour:.2f}")
    st.plotly_chart(fig, use_container_width=True)


    st.text(f"Heatmap by a.m.:")
    temp = df6[df6['hour'].isin(range(0, 12))]

    pivot = pd.pivot_table(temp, index='date', columns='hour', values='+date', aggfunc='count')

    piv =  px.imshow(pivot, color_continuous_scale="blues")

    st.plotly_chart(piv, use_container_width=True)


    st.text(f"Heatmap by p.m.:")
    temp1 = df6[df6['hour'].isin([12,13,14,15,16,17,18,19,20,21,22,23])]
    pivot1 = pd.pivot_table(temp1, index='date', columns='hour' , values='+date', aggfunc='count')

    piv =  px.imshow(pivot1, color_continuous_scale="blues")

    st.plotly_chart(piv, use_container_width=True)

    df7 = df5[['ticket number','receiving time','agent','topics','subtopics']].copy()

    st.text( f"Tickets receiving time out of actual time-frame: {len(df7)}")
    st.dataframe(df7.sort_values(by='agent', ascending=True), use_container_width=True)


with st.expander("General dynamics"):

    st.dataframe(df1, use_container_width=True)

    chart_data = pd.DataFrame(df1, columns=['total tickets'])
    st.area_chart(chart_data, use_container_width=True)

    chart_data = pd.DataFrame(df1, columns=['sla'])
    st.area_chart(chart_data, use_container_width=True)

    chart_data = pd.DataFrame(df1, columns=['first response'])
    st.area_chart(chart_data, use_container_width=True)

with st.expander("CSI Spanish"):
    #st.dataframe(dfg1)
    st.text( f"Total CSI index: {len(dfg1)}")
    csi5 = dfg1[dfg1['Por favor, califica la calidad de nuestra respuesta. '] == 5]['Por favor, califica la calidad de nuestra respuesta. '].count()
    meancsi = dfg1['Por favor, califica la calidad de nuestra respuesta. '].mean()
    st.text( f"Average index: {meancsi}")
    st.text( f"Total CSI index = 5: {csi5}")
    st.text( f"Total CSI index %: {csi5 / len(dfg1):.0%}")

    tokens_by_csi = dfg1.groupby(by=["Por favor, califica la calidad de nuestra respuesta. "]).count()[["Token"]]
    fig_tokens_by_csi = px.bar(
        tokens_by_csi,
        x=tokens_by_csi.index,
        y="Token",
        text="Token",
        title="<b>Tokens by csi</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_csi),
        template="plotly_white",
    )
    fig_tokens_by_csi.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    st.plotly_chart(fig_tokens_by_csi, use_container_width=True)

    dfg1['Submitted At'] = pd.to_datetime(dfg1['Submitted At'], format='%Y-%m')
    dfg1['Submitted At'] = dfg1['Submitted At'].dt.strftime('%Y-%m')

    tokens_by_month = dfg1.sort_values(by=["Submitted At"], ascending=True).groupby('Submitted At').count()

    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="Por favor, califica la calidad de nuestra respuesta. ",
        text="Por favor, califica la calidad de nuestra respuesta. ",
        title="<b>Tokens by Date</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )

    st.plotly_chart(fig_tokens_by_month, use_container_width=True)

    tokens_by_month = dfg1.sort_values(by=["Submitted At"], ascending=True).groupby('Submitted At')['Por favor, califica la calidad de nuestra respuesta. '].mean()

    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="Por favor, califica la calidad de nuestra respuesta. ",
        text="Por favor, califica la calidad de nuestra respuesta. ",
        title="<b>Average index by date</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )

    st.plotly_chart(fig_tokens_by_month, use_container_width=True)

with st.expander("CSI Indonesian"):
    #st.dataframe(dfg1)
    st.text( f"Total CSI index: {len(dfg4)}")
    csi5 = dfg4[dfg4['Tolong penuhi syarat kualitas jawaban kami.'] == 5]['Tolong penuhi syarat kualitas jawaban kami.'].count()
    meancsi = dfg4['Tolong penuhi syarat kualitas jawaban kami.'].mean()

    st.text( f"Average index: {meancsi}")
    st.text( f"Total CSI index = 5: {csi5}")
    st.text( f"Total CSI index %: {csi5 / len(dfg4):.0%}")

    tokens_by_csi = dfg4.groupby(by=["Tolong penuhi syarat kualitas jawaban kami."]).count()[["Token"]]
    fig_tokens_by_csi = px.bar(
        tokens_by_csi,
        x=tokens_by_csi.index,
        y="Token",
        text="Token",
        title="<b>Tokens by csi</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_csi),
        template="plotly_white",
    )
    fig_tokens_by_csi.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    st.plotly_chart(fig_tokens_by_csi, use_container_width=True)

    dfg4['Submitted At'] = pd.to_datetime(dfg4['Submitted At'], format='%Y-%m')
    dfg4['Submitted At'] = dfg4['Submitted At'].dt.strftime('%Y-%m')

    tokens_by_month = dfg4.sort_values(by=["Submitted At"], ascending=True).groupby('Submitted At').count()

    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="Tolong penuhi syarat kualitas jawaban kami.",
        text="Tolong penuhi syarat kualitas jawaban kami.",
        title="<b>Tokens by Date</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )

    st.plotly_chart(fig_tokens_by_month, use_container_width=True)

    tokens_by_month = dfg4.sort_values(by=["Submitted At"], ascending=True).groupby('Submitted At').mean(numeric_only=True)

    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="Tolong penuhi syarat kualitas jawaban kami.",
        text="Tolong penuhi syarat kualitas jawaban kami.",
        title="<b>Average index by date</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )

    st.plotly_chart(fig_tokens_by_month, use_container_width=True)

with st.expander("CSI Portuguese"):
    #st.dataframe(dfg2)
    meancsi = dfg2['Estime a qualidade da nossa resposta, por favor.'].mean()
    st.text( f"Average index: {meancsi}")
    st.text( f"Total CSI index: {len(dfg2)}")
    csi5 = dfg2[dfg2['Estime a qualidade da nossa resposta, por favor.'] == 5]['Estime a qualidade da nossa resposta, por favor.'].count()
    st.text( f"Total CSI index = 5: {csi5}")
    st.text( f"Total CSI index %: {csi5 / len(dfg2):.0%}")



    tokens_by_csi = dfg2.groupby(by=["Estime a qualidade da nossa resposta, por favor."]).count()[["Token"]]
    fig_tokens_by_csi = px.bar(
        tokens_by_csi,
        x=tokens_by_csi.index,
        y="Token",
        text="Token",
        title="<b>Tokens by csi</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_csi),
        template="plotly_white",
    )
    fig_tokens_by_csi.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    st.plotly_chart(fig_tokens_by_csi, use_container_width=True)

    dfg2['Submitted At'] = pd.to_datetime(dfg2['Submitted At'], format='%Y-%m')
    dfg2['Submitted At'] = dfg2['Submitted At'].dt.strftime('%Y-%m')

    tokens_by_month = dfg2.sort_values(by=["Submitted At"], ascending=True).groupby('Submitted At').count()

    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="Estime a qualidade da nossa resposta, por favor.",
        text="Estime a qualidade da nossa resposta, por favor.",
        title="<b>Tokens by Date</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )



    st.plotly_chart(fig_tokens_by_month, use_container_width=True)



    tokens_by_month = dfg2.sort_values(by=["Submitted At"], ascending=True).groupby('Submitted At').mean(numeric_only=True)

    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="Estime a qualidade da nossa resposta, por favor.",
        text="Estime a qualidade da nossa resposta, por favor.",
        title="<b>Average index by date</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )



    st.plotly_chart(fig_tokens_by_month, use_container_width=True)

with st.expander("CSI English"):
    #st.dataframe(dfg3)
    meancsi = dfg3['Please, qualify the quality of our answer'].mean()
    st.text( f"Average index: {meancsi}")
    st.text( f"Total CSI index: {len(dfg3)}")
    csi5 = dfg3[dfg3['Please, qualify the quality of our answer'] == 5]['Please, qualify the quality of our answer'].count()
    st.text( f"Total CSI index = 5: {csi5}")
    st.text( f"Total CSI index %: {csi5 / len(dfg3):.0%}")

    tokens_by_csi = dfg3.groupby(by=["Please, qualify the quality of our answer"]).count()[["Token"]]
    fig_tokens_by_csi = px.bar(
        tokens_by_csi,
        x=tokens_by_csi.index,
        y="Token",
        text="Token",
        title="<b>Tokens by csi</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_csi),
        template="plotly_white",
    )
    fig_tokens_by_csi.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    st.plotly_chart(fig_tokens_by_csi, use_container_width=True)


    dfg3['Submitted At'] = pd.to_datetime(dfg3['Submitted At'], format='%Y-%m')
    dfg3['Submitted At'] = dfg3['Submitted At'].dt.strftime('%Y-%m')

    tokens_by_month = dfg3.sort_values(by=["Submitted At"], ascending=True).groupby('Submitted At').count()

    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="Please, qualify the quality of our answer",
        text="Please, qualify the quality of our answer",
        title="<b>Tokens by Date</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )



    st.plotly_chart(fig_tokens_by_month, use_container_width=True)



    tokens_by_month = dfg3.sort_values(by=["Submitted At"], ascending=True).groupby('Submitted At').mean(numeric_only=True)

    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="Please, qualify the quality of our answer",
        text="Please, qualify the quality of our answer",
        title="<b>Average index by date</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )



    st.plotly_chart(fig_tokens_by_month, use_container_width=True)

with st.expander("Assessment"):

    with st.form("my_form"):
        Agent = st.multiselect(
        "Select the Agents:",
        options=dfg5["Agent"].unique(),
        default=dfg5["Agent"].unique()
    )
        submitted = st.form_submit_button("Submit")
        if submitted:
            dfg5 = dfg5.query(
                "Agent == @Agent"
            )

        else:
            pass

    #pivot = pivot * 100
    dfg5['total'] = dfg5.mean(axis=1,numeric_only=True)
    #dfg5.sort_values(by='total', ascending=False, inplace=True)
    #dfg5 = dfg5.fillna(0)
    meantime = dfg5['total'].mean()

    st.metric(label="Assesment by selected agents", value=meantime)

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    # Define custom colormap
    red = '#ff0000'  # pure red
    green = '#00ff00'  # pure green
    yellow = '#ffff00'  # pure yellow
    colors = [red, yellow, green]
    cmap = ListedColormap(colors, name='my_cmap')
    bounds = [0.91, 1.0]  # boundaries for each color in the colormap
    norm = plt.Normalize(bounds[0], bounds[-1])

    # Apply custom colormap to DataFrame
    dfg5 = dfg5.style.background_gradient(cmap=cmap, vmin=bounds[0], vmax=bounds[-1])
    st.dataframe(dfg5, use_container_width=True)









    #dfg5 = dfg5.style.format('{:0.0%}', subset=['total']).background_gradient(cmap='ocean_r')
    #st.dataframe(dfg5)
