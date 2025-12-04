#initialization
import pandas as pd
import numpy as np
import os

#for dashboard
import dash
from dash import html, dcc, Input, Output

#for visualizations
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
from PIL import Image
from collections import Counter
from sklearn.preprocessing import LabelEncoder

#loading dataset
dir_path = os.getcwd()
dir_path = os.path.join(dir_path, 'dataset_for_analysis.csv')
df = pd.read_csv(dir_path)
                        

#graph functions
#Option 1 : overall sentiment distribution analysis
def customer_analysis(df):
    #get data customer segment and sentiment
    temp_df = pd.DataFrame()
    temp_df[['id','customer','sentiment']] = df[['feedback_id','customer_segment','sentiment']]

    #group customer segment and sentiment
    temp_df = temp_df.groupby(['customer','sentiment'])['id'].count().reset_index(name='count')

    #plotting graph
    fig = px.bar(temp_df,x='customer',y='count',color='sentiment',text='count',title='Sentiment by Customer Type', barmode='group',
                 labels={'customer':'Customer Type','count':'No.of Feedback','sentiment':'Sentiment'})
    
    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05


    fig.update_traces(textposition='outside',textfont_size=12,cliponaxis=False,textfont_weight='bold')
    fig.update_yaxes(griddash="dot", gridcolor="#534B23",layer="below traces")
    fig.add_shape(type="rect",xref="paper",  yref="paper",x0=0,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5))
    fig.update_layout(title_x=0.5, title_font_weight='bold', paper_bgcolor="#000000",plot_bgcolor="#000000", title_font_family= 'Bahnschrift',
                      title_font_color="#FFFFFF",title_font_size = 24, font_color="#FFFFFF",yaxis_range=[0, max(temp_df['count'])+100],
                      xaxis_title_font_weight='bold',yaxis_title_font_weight='bold',legend_title=dict(text="<b>Sentiment</b>"))

    return fig 
def category_analysis(df):
    
    #get data feedback category and sentiment
    temp_df = pd.DataFrame()
    temp_df[['id','category','sentiment']] = df[['feedback_id','feedback_category','sentiment']]

    #group feedback category and sentiment
    temp_df = temp_df.groupby(['category','sentiment'])['id'].count().reset_index(name='count')

    #plotting graph
    fig = px.bar(temp_df,x='category',y='count',color='sentiment',text='count',title='Sentiment by Feedback Category', barmode='group',
                 labels={'category':'Feedback Category','count':'No.of Feedback','sentiment':'Sentiment'})
    
    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05

    fig.update_traces(textposition='outside',textfont_size=12,cliponaxis=False,textfont_weight='bold')
    fig.update_yaxes(griddash="dot", gridcolor="#534B23",layer="below traces")
    fig.add_shape(type="rect",xref="paper",  yref="paper",x0=0,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5))
    fig.update_layout(title_x=0.5, title_font_weight='bold', paper_bgcolor="#000000",plot_bgcolor="#000000",title_font_family= 'Bahnschrift',
                      title_font_color="#FFFFFF",title_font_size = 24, font_color="#FFFFFF",yaxis_range=[0, max(temp_df['count'])+100],
                      xaxis_title_font_weight='bold',yaxis_title_font_weight='bold',legend_title=dict(text="<b>Sentiment</b>"))
    return fig
def count_analysis(df):

    #get data for sentiment 
    temp_df = pd.DataFrame()
    temp_df[['id','sentiment']] = df[['feedback_id','sentiment']]

    #group by sentiment 
    temp_df = temp_df.groupby(['sentiment'])['id'].count().reset_index(name='count')
    
    #graph for boxplot sentiment/count
    fig = make_subplots(rows=1,cols=2,subplot_titles=('Sentiment Distribution (Bar)','Sentiment Distribution (Pie)'),
                        specs=[[{'type':'bar'},{'type':'pie'}]])
    fig1 = px.bar(temp_df,x='sentiment',y='count',color='sentiment',color_discrete_sequence=px.colors.qualitative.Plotly)

    #graph for pie sentiment/count
    fig2 = px.pie(temp_df,values='count',names='sentiment')

    #section for both graphs
    for trace in fig1.data:
        fig.add_trace(trace,row=1,col=1)
    for trace in fig2.data:
        fig.add_trace(trace,row=1,col=2)

    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05
        annotation['font']['family'] = 'Bahnschrift'
        annotation['font']['size'] = 20
    
    fig.update_xaxes(title_text="<b>Sentiment</b>", row=1, col=1)
    fig.add_shape(type="rect",xref="x1",  yref="y1",x0=-0.5,y0=0,x1=2.5, y1=max(temp_df['count']) * 1.1, line=dict(color="#FCFF46",width=2.5))
    fig.update_yaxes(title_text="No. of Feedback", griddash="dot", gridcolor="#534B23",layer="below traces",row=1, col=1)
    fig.update_traces(textinfo='label + percent',textfont_size=18,textfont_color="#FFFFFF",textfont_weight='bold',row=1,col=2)
    fig.update_layout(height=600,showlegend=False,paper_bgcolor="#000000",plot_bgcolor="#000000", 
                      title_font_color="#FFFFFF", font_color="#FFFFFF",xaxis_title_font_weight='bold',yaxis_title_font_weight='bold')
    return fig
def delivery_analysis(df):

    #get data for delivery and sentiment
    temp_df = pd.DataFrame()
    temp_df[['id','sentiment','status','delay_time']] = df[['feedback_id','sentiment','delivery_status','delivery_time_mins']]

    #group by delivery status
    temp_df1 = temp_df.groupby(['status','sentiment'])['id'].count().reset_index(name='count')
    
    #group by delivery mins
    temp_df2 = temp_df.groupby(['delay_time','sentiment'])['id'].count().reset_index(name='count')
    temp_df2 = temp_df2.sort_values(by='delay_time',ascending=True)
    
    #plotting graph for sunburst on delivery status/sentiment
    fig = make_subplots(rows=1,cols=2,subplot_titles=('Sentiment Distribution on Delivery Status','Sentiment Distribution on Delivery Minutes'),
                        specs=[[{'type':'sunburst'},{'type':'xy'}]])
    fig1 = px.sunburst(temp_df1,path=['status','sentiment'],values='count',color='status', color_discrete_sequence=px.colors.qualitative.Plotly)
    fig1.update_traces(textinfo='label+percent entry',textfont_size=18,textfont_color="#ffffff")

    #plotting graph for line on delivery delay/sentiment
    fig2 = px.line(temp_df2,x='delay_time',y='count',color='sentiment',markers=True)

    #section for both graphs
    for trace in fig1.data:
        fig.add_trace(trace,row=1,col=1)
    for trace in fig2.data:
        fig.add_trace(trace,row=1,col=2)

    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05
        annotation['font']['family'] = 'Bahnschrift'
        annotation['font']['size'] = 20

    fig.update_xaxes(title_text='<b>Delay (mins)</b>',showline=False,showgrid=False,zeroline=False,row=1,col=2)
    fig.update_yaxes(title_text='<b>No.of Feedback</b>',showline=False, zeroline=False,griddash="dot", gridcolor="#534B23",
                     layer="below traces",title_font_color="#FFFFFF",row=1,col=2)
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0.55,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_layout(height=650,legend=dict(title="Sentiment",x=0.8,y=-0.2,orientation='h',xanchor='center',yanchor='bottom'),
                      paper_bgcolor="#000000",plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF")
    return fig

#Option 2 : time-series analysis
def year_analysis(df):
    #get data year and sentiment
    temp_df = pd.DataFrame()
    temp_df[['id','sentiment','year']] = df[['feedback_id','sentiment','feedback_year']]

    #group year
    temp_df = temp_df.groupby(['year','sentiment'])['id'].count().reset_index(name='count')

    #plotting graph
    fig = px.bar(temp_df,x='year',y='count',color='sentiment',text='count',title='Sentiment Trend by Year', barmode='group',
                 labels={'year':'Year','count':'No.of Feedback','sentiment':'Sentiment'})
    
    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05

    fig.update_traces(textposition='outside',textfont_size=12,cliponaxis=False,textfont_weight='bold')
    fig.update_yaxes(griddash="dot", gridcolor="#534B23",layer="below traces")
    fig.update_xaxes(tickvals=(2023,2024))
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5))
    fig.update_layout(title_x=0.5, title_font_weight='bold',paper_bgcolor="#000000",plot_bgcolor="#000000", title_font_family='Bahnschrift',
                      title_font_size=24, title_font_color="#FFFFFF",font_color="#FFFFFF",yaxis_range=[0, max(temp_df['count'])+200],
                      xaxis_title_font_weight='bold',yaxis_title_font_weight='bold',legend_title=dict(text="<b>Sentiment</b>"))
    return fig
def month_analysis(df):
    #get data month and sentiment
    temp_df = pd.DataFrame()
    temp_df[['id','sentiment','month']] = df[['feedback_id','sentiment','feedback_month']]

    #map month to monthname
    monthMap = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    temp_df['monthName'] = temp_df['month'].map(lambda x:monthMap[x])

    #group month and sentiment
    temp_df = temp_df.groupby(['month','monthName','sentiment'])['id'].count().reset_index(name='count')
    temp_df.sort_values(by='month',ascending=True)

    #plotting graph
    fig = px.line(temp_df,x='monthName',y='count',color='sentiment',markers=True, title='Sentiment Trend by Month',
                  labels={'monthName':'Month','count':'No.of Feedback','sentiment':'Sentiment'})
    
    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05

    fig.update_xaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(griddash="dot", gridcolor="#534B23",layer="below traces")
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_layout(title_x=0.5, title_font_weight='bold',paper_bgcolor="#000000",plot_bgcolor="#000000", title_font_family='Bahnschrift',
                      title_font_size=24,title_font_color="#FFFFFF",font_color="#FFFFFF",xaxis_title_font_weight='bold', 
                      yaxis_title_font_weight='bold',legend_title=dict(text="<b>Sentiment</b>"))

    #plotting min and max for each sentiment
    for sentiment in temp_df['sentiment'].unique():
        df_sent = temp_df[temp_df['sentiment'] == sentiment]
        #find max
        max_row = df_sent[df_sent['count'] == df_sent['count'].max()]
        for _, row in max_row.iterrows():
            fig.add_annotation(
                x=row['monthName'], 
                y=row['count'],
                text=f"Max: {row['count']}", font=dict(color="#70ff2e", size=10.5),
                showarrow=True, arrowhead=2, ax=0, ay=-15
            )
        #find min
        min_row = df_sent[df_sent['count'] == df_sent['count'].min()]
        for _, row in min_row.iterrows():
            fig.add_annotation(
                x=row['monthName'],
                y=row['count'],
                text=f"Min: {row['count']}", font=dict(color="#ff0000", size=10.5),
                showarrow=True, arrowhead=2, ax=0, ay=50
            )
    return fig
def day_analysis(df):
    #get data day,month,year and sentiment
    temp_df = pd.DataFrame()
    temp_df[['id','sentiment','day_type','year','month','day']] = df[['feedback_id','sentiment','day_type','feedback_year', 'feedback_month', 'feedback_day']]
    temp_df['date'] =  pd.to_datetime(temp_df[['year', 'month', 'day']])
    temp_df['dayName'] = temp_df['date'].dt.day_name()
    temp_df.drop(columns=['date','day','month'])
    
    #group day_type, day and sentiment
    dayMap = {'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4,'Friday':5,'Saturday':6,'Sunday':7}
    temp_df['dayNo'] = temp_df['dayName'].map(lambda x:dayMap[x])
    temp_df = temp_df.groupby(['day_type','dayNo','dayName','sentiment'])['id'].count().reset_index(name='count')
    temp_df = temp_df.sort_values(by='dayNo',ascending=True)
   
    #plotting graph for day_type and sentiment
    fig = make_subplots(rows=1,cols=2, subplot_titles=('Sentiment Distribution in Weekday/Weekend','Sentiment Trend by Day'), 
                        specs=[[{'type':'sunburst'},{'type':'bar'}]])
    fig1 = px.sunburst(temp_df,path=['day_type','dayName','sentiment'],values='count',color='dayName', color_discrete_sequence=px.colors.qualitative.Plotly)
    fig1.update_traces(textinfo='label+percent entry',textfont_size=18,textfont_color="#ffffff")
    
    #Plotting graph for day and sentiment
    fig2 = px.bar(temp_df,x='dayName',y='count',color='sentiment',barmode='group')

    #adding to one figure
    for trace in fig1.data:
        fig.add_trace(trace,row=1,col=1)
    for trace in fig2.data:
        fig.add_trace(trace,row=1,col=2)

    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05
        annotation['font']['family'] = 'Bahnschrift'
        annotation['font']['size'] = 20

    fig.update_xaxes(title_text="<b>Day</b>",row=1, col=2)
    fig.update_xaxes(title_text='<b>Delay (mins)</b>',showline=False,showgrid=False,zeroline=False,row=1,col=2)
    fig.update_yaxes(title_text="<b>No. of Feedback</b>", row=1, col=2)
    fig.update_yaxes(showline=False, zeroline=False,griddash="dot", gridcolor="#534B23",layer="below traces",
                     title_font_color="#FFFFFF",row=1,col=2)
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0.55,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_layout(height=650,legend=dict(title="<b>Sentiment</b>",x=0.8,y=-0.2,orientation='h',xanchor='center',yanchor='bottom'),
                      paper_bgcolor="#000000",plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF")
    return fig
def hour_analysis(df):

    #get hour,hour_type and sentiment
    temp_df = pd.DataFrame()
    temp_df[['id','sentiment','order_time']] = df[['feedback_id','sentiment','orders_time']]
    temp_df['hour'] = pd.to_datetime(temp_df['order_time'], format='%H:%M').dt.hour
    temp_df['hr_type'] = temp_df['hour'].apply(get_hrType)

    #group hour, hour_type and sentiment
    temp_df = temp_df.groupby(['hr_type','hour','sentiment'])['id'].count().reset_index(name='count')
    temp_df = temp_df.sort_values(by='hour',ascending=True)
    
    #plotting graph for hour_type and sentiment
    fig = make_subplots(rows=1,cols=2, subplot_titles=('Sentiment Distribution in Morning/Afternoon/Evening/Night','Sentiment Trend by Hour'), 
                        specs=[[{'type':'sunburst'},{'type':'xy'}]])
    fig1 = px.sunburst(temp_df,path=['hr_type','sentiment'],values='count',color='hr_type', color_discrete_sequence=px.colors.qualitative.Plotly)
    fig1.update_traces(textinfo='label+percent entry',textfont_size=18,textfont_color="#ffffff")

    #plotting graph for hour and sentiment
    fig2 = px.line(temp_df,x='hour',y='count',color='sentiment',markers=True)

    #adding to one figure
    for trace in fig1.data:
        fig.add_trace(trace,row=1,col=1)
    for trace in fig2.data:
        fig.add_trace(trace,row=1,col=2)

    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05
        annotation['font']['family'] = 'Bahnschrift'
        annotation['font']['size'] = 20

    fig.update_xaxes(title_text="<b>Hour</b>", row=1, col=2)
    fig.update_xaxes(range=[0,24],dtick=2,showline=False, zeroline=False, showgrid=False,row=1,col=2)
    fig.update_yaxes(title_text="<b>No. of Feedback</b>", row=1, col=2)
    fig.update_yaxes(showline=False, zeroline=False,griddash="dot", gridcolor="#534B23",layer="below traces",
                     title_font_color="#FFFFFF",row=1,col=2)
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0.55,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_layout(height=650,legend=dict(title="<b>Sentiment</b>",x=0.8,y=-0.2,orientation='h',xanchor='center',yanchor='bottom'),
                      paper_bgcolor="#000000",plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF")
    return fig
def get_hrType(hour):
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 16:
        return 'Afternoon'
    elif 16 <= hour < 20:
        return 'Evening'
    else:
        return 'Night'

#Option 3 : geographical analysis
#geographical analysis
def geo_analysis(df):
    #get data area and sentiment
    temp_df = pd.DataFrame()
    temp_df[['id','sentiment','area']] = df[['feedback_id','sentiment','area']]

    #group sentiment and (top 5)
    temp_df = temp_df.groupby(['area','sentiment'])['id'].count().reset_index(name='count')
    top_areas = temp_df.groupby('area')['count'].sum().nlargest(5).index
    temp_df_top = temp_df[temp_df['area'].isin(top_areas)]

    #graph for top5 areas/sentiment
    fig1 = px.bar(temp_df_top,x='area',y='count',color='sentiment', text='count', barmode='group',
                 labels={'area':'Area','sentiment':'Sentiment','count':'No.of Feedback'})
    
    fig2 = px.scatter(temp_df_top,y='area',x='count',color='sentiment',symbol='sentiment')

    fig1.update_traces(textposition='outside',textfont_size=12,cliponaxis=False,textfont_weight='bold')
    fig2.update_traces(marker_size=10)

    #section for both graphs
    fig = make_subplots(rows=1, cols=2,subplot_titles = ('Top 5 Areas with Most Feedback', 'Sentiment Distribution in Top 5 Areas'),
                              specs=[[{'type':'bar'},{'type':'scatter'}]])
    for trace in fig1.data:
        trace.legend = "legend1"
        fig.add_trace(trace,row=1,col=1)
    for trace in fig2.data:
        trace.legend = "legend2"
        fig.add_trace(trace,row=1,col=2)

    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] += 0.05
        annotation['font']['family'] = 'Bahnschrift'
        annotation['font']['size'] = 20

    fig.update_yaxes(range=[None,max(temp_df_top['count'])],row=1,col=1)
    fig.update_yaxes(griddash="dot", gridcolor="#534B23",layer="below traces",title_font_color="#FFFFFF",row=1,col=1)
    fig.update_yaxes(griddash="dot", gridcolor="#534B23",layer="below traces",title_font_color="#FFFFFF",row=1,col=2)
    fig.update_xaxes(griddash="dot", gridcolor="#534B23",layer="below traces",title_font_color="#FFFFFF",row=1,col=2)
    fig.update_xaxes(range=[min(temp_df_top['count'])-2,max(temp_df_top['count'])+2], dtick=2, row=1, col=2)

    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0,y0=0,x1=0.45, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0.55,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")

    fig.update_layout(height=650,legend1=dict(title='<b>Sentiment</b>',x=0.23,y=-0.22,xanchor="center",yanchor="bottom",orientation="h"),
                      legend2=dict(title='<b>Sentiment</b>',x=0.78,y=-0.22,xanchor="center",yanchor="bottom",orientation="h"),
                      xaxis_title='<b>Area</b>',yaxis_title='<b>No.of Feedback</b>',xaxis2_title='<b>No.of Feedback</b>',yaxis2_title='<b>Area</b>',
                      paper_bgcolor="#000000",plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF")
    return fig

#Option 4 : word analysis
def wordcloud_analysis(df):
    #get data for wordcloud images
    dir_path = os.getcwd()
    dir_path = os.path.join(dir_path,'graph_image')
    pos_file = os.path.join(dir_path,'positive_wordcloud.png')
    neg_file = os.path.join(dir_path,'negative_wordcloud.png')
    neu_file = os.path.join(dir_path,'neutral_wordcloud.png')

    pos_img = Image.open(pos_file)
    neg_img = Image.open(neg_file)
    neu_img = Image.open(neu_file)

    #figures for images
    fig1 = px.imshow(pos_img)
    fig2 = px.imshow(neg_img)
    fig3 = px.imshow(neu_img)

    #plotting graph
    fig = make_subplots(rows=1,cols=3,subplot_titles=('Positive Wordcloud','Negative Wordcloud','Neutral Wordcloud'))

    for trace in fig1.data:
        fig.add_trace(trace,row=1,col=1)
    for trace in fig2.data:
        fig.add_trace(trace,row=1,col=2)
    for trace in fig3.data:
        fig.add_trace(trace,row=1,col=3)

    for annotation in fig['layout']['annotations']:
        annotation['font']['weight'] = 'bold'
        annotation['y'] -=0.08
        annotation['font']['family'] = 'Bahnschrift'
        annotation['font']['size'] = 20

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=650,paper_bgcolor="#000000",plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF",
                      showlegend=False)
    return fig
def com_word_analysis(df):
    #get feedback text and sentiment
    temp_df = pd.DataFrame()
    temp_df[['text','sentiment']] = df[['feedback_text','sentiment']]
    temp_df['text'] = temp_df['text'].str.lower()
    temp_df['text_list'] = temp_df['text'].apply(lambda x:str(x).split())
    
    #finding 20 most common words used
    all_word = [word for words in temp_df['text_list'] for word in words if len(word)>5]
    top_word = Counter(all_word).most_common(20)
    top_word = sorted(top_word,key=lambda x:x[1],reverse=True)
    
    #extract word and frequency count 
    words = [word for word,freq in top_word]
    freq = [freq for word,freq in top_word]

    #color mapping
    colorscale = [(0,"#dcc0e7"),(0.3,"#b979d4"),(0.6,"#8e2eb8"),(1,"#70069d")]
    min_freq = min(freq)
    max_freq = max(freq)
    color_values = [(f - min_freq) / (max_freq - min_freq) for f in freq]

    #plotting horizontal bar graph
    fig = px.bar(x=freq, y=words, color=color_values, color_continuous_scale=colorscale, orientation='h')
    fig.update_xaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(autorange='reversed')
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_layout(title='Top 20 Most Common Words', yaxis_title="<b>Word</b>", xaxis_title="<b>Frequency</b>", coloraxis_showscale=False, 
                      title_font_family = 'Bahnschrift', title_font_size=24, title_font_weight='bold',paper_bgcolor="#000000",
                      plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF")
    return fig
def pos_word_analysis(df):
    #get feedback text and sentiment
    temp_df = pd.DataFrame()
    temp_df[['text','sentiment']] = df[['feedback_text','sentiment']]
    temp_df['text'] = temp_df['text'].str.lower()
    temp_df['text_list'] = temp_df['text'].apply(lambda x:str(x).split())
    
    #finding 10 most positive words used
    all_word = [word for words in temp_df[temp_df['sentiment']=='positive']['text_list'] for word in words if len(word)>5] 
    top_word = Counter(all_word).most_common(10)
    top_word = sorted(top_word,key=lambda x:x[1],reverse=True)

    #extract word and frequency count 
    words = [word for word,freq in top_word]
    freq = [freq for word,freq in top_word]

    #color mapping
    colorscale = [(0,"#bed8dc"),(0.3,"#88c6dd"),(0.6,"#2e93b8"),(1,"#067f9d")]
    min_freq = min(freq)
    max_freq = max(freq)
    color_values = [(f - min_freq) / (max_freq - min_freq) for f in freq]

    #plotting horizontal bar graph
    fig = px.bar(x=freq, y=words, color=color_values, color_continuous_scale=colorscale, orientation='h')
    fig.update_xaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(autorange='reversed')
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_layout(title='Top 10 Most Common Positive Words', yaxis_title="<b>Word</b>", xaxis_title="<b>Frequency</b>", coloraxis_showscale=False, 
                      title_font_weight='bold',title_font_family='Bahnschrift', title_font_size=24,paper_bgcolor="#000000",
                      plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF")
    return fig
def neg_word_analysis(df):
    #get feedback text and sentiment
    temp_df = pd.DataFrame()
    temp_df[['text','sentiment']] = df[['feedback_text','sentiment']]
    temp_df['text'] = temp_df['text'].str.lower()
    temp_df['text_list'] = temp_df['text'].apply(lambda x:str(x).split())
    
    #finding 10 most negative words used
    all_word = [word for words in temp_df[temp_df['sentiment']=='negative']['text_list'] for word in words if len(word)>5] 
    top_word = Counter(all_word).most_common(10)
    top_word = sorted(top_word,key=lambda x:x[1],reverse=True)

    #extract word and frequency count 
    words = [word for word,freq in top_word]
    freq = [freq for word,freq in top_word]

    #color mapping
    colorscale = [(0,"#dcbed6"),(0.3,"#dd88cb"),(0.6,"#b82ea8"),(1,"#9d067c")]
    min_freq = min(freq)
    max_freq = max(freq)
    color_values = [(f - min_freq) / (max_freq - min_freq) for f in freq]

    #plotting horizontal bar graph
    fig = px.bar(x=freq, y=words, color=color_values, color_continuous_scale=colorscale, orientation='h')
    fig.update_xaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(autorange='reversed')
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_layout(title='Top 10 Most Common Negative Words', yaxis_title="<b>Word</b>", xaxis_title="<b>Frequency</b>", coloraxis_showscale=False, 
                      title_font_weight='bold',title_font_family='Bahnschrift', title_font_size=24,paper_bgcolor="#000000",
                      plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF")
    return fig
def neu_word_analysis(df):
    #get feedback text and sentiment
    temp_df = pd.DataFrame()
    temp_df[['text','sentiment']] = df[['feedback_text','sentiment']]
    temp_df['text'] = temp_df['text'].str.lower()
    temp_df['text_list'] = temp_df['text'].apply(lambda x:str(x).split())
    
    #finding 10 most neutral words used
    all_word = [word for words in temp_df[temp_df['sentiment']=='neutral']['text_list'] for word in words if len(word)>5] 
    top_word = Counter(all_word).most_common(10)
    top_word = sorted(top_word,key=lambda x:x[1],reverse=True)

    #extract word and frequency count 
    words = [word for word,freq in top_word]
    freq = [freq for word,freq in top_word]

    #color mapping
    colorscale = [(0,"#d3ab8c"),(0.3,"#cc985d"),(0.6,"#b86b27"),(1,"#9f4e08")]
    min_freq = min(freq)
    max_freq = max(freq)
    color_values = [(f - min_freq) / (max_freq - min_freq) for f in freq]

    #plotting horizontal bar graph
    fig = px.bar(x=freq, y=words, color=color_values, color_continuous_scale=colorscale, orientation='h')
    fig.update_xaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(showline=False,showgrid=False,zeroline=False)
    fig.update_yaxes(autorange='reversed')
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=0,y0=0,x1=1.0, y1=1.0, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_layout(title='Top 10 Most Common Neutral Words', yaxis_title="<b>Word</b>", xaxis_title="<b>Frequency</b>", coloraxis_showscale=False, 
                      title_font_weight='bold',title_font_family='Bahnschrift', title_font_size=24,paper_bgcolor="#000000",
                      plot_bgcolor="#000000",title_font_color="#FFFFFF",font_color="#FFFFFF")
    return fig

#Option 5 : others
def correlation_analysis(df):
    #correlation analysis to find relationships between features
    df_sub = pd.DataFrame()
    df_sub = df.copy()
    df_sub.drop(columns=['feedback_id','order_id','customer_id','orders_time'],inplace=True)
    df_sub['hour'] = pd.to_datetime(df['orders_time'],format='%H:%M').dt.hour
    le = LabelEncoder()
    for col in df_sub.select_dtypes(include=['object']).columns:
        df_sub[col] = le.fit_transform(df_sub[col])
    corr = df_sub.corr(numeric_only=True)

    fig = px.imshow(corr.round(4),text_auto=True,color_continuous_scale='RdYlGn',aspect='auto')
    fig.update_xaxes(tickangle=45,tickfont_family='Bahnschrift',tickfont_size=13)
    fig.update_yaxes(tickfont_family='Bahnschrift',tickfont_size=13)
    #highlight sentiment
    highlight_col = ['sentiment']
    n = len(corr)
    shapes = []
    for col in highlight_col:
        if col in corr.columns:
            idx = corr.columns.get_loc(col)
            # vertical line
            shapes.append(dict(type="rect",
                            x0=idx-0.5, x1=idx+0.5,
                            y0=-0.5, y1=n-0.5,
                            line=dict(color="blue", width=3),
                            fillcolor="rgba(0,0,0,0)"))
            # horizontal line
            shapes.append(dict(type="rect",
                            x0=-0.5, x1=n-0.5,
                            y0=idx-0.5, y1=idx+0.5,
                            line=dict(color="blue", width=3),
                            fillcolor="rgba(0,0,0,0)"))
            fig.update_layout(shapes=shapes,title_font_weight='bold',paper_bgcolor="#000000",plot_bgcolor="#000000",
                              title_font_color="#FFFFFF",font_color="#FFFFFF")
    fig.add_shape(type="rect",xref="paper",yref="paper",x0=-0.105,y0=-0.35,x1=1.095, y1=1.1, line=dict(color="#FCFF46",width=2.5),layer="below")
    fig.update_traces(textfont_weight='bold')
    return fig
def model_analysis(df):
    report_file = 'model_classification_report.txt'
    try:
        with open(report_file,'r') as file:
            content = file.read()
            content_fixed = content.replace(" ", "\u00A0")
            return html.Pre(content, className='text-style')
    except FileNotFoundError:
        return html.Div(f'File {report_file} was not found.')
    except Exception as e:
        return html.Div(f'Unknown error occured, {e}.')
def summary_analysis(df):
    summary_file = 'feedback_analysis_summary.txt'
    try:
        with open(summary_file,'r',encoding='utf-8') as file:
            content = file.read()
            return html.Pre(content,className='text2-style')
    except FileNotFoundError:
        return html.Div(f'File {summary_file} was not found.')
    except Exception as e:
        return html.Div(f'Unknown error occured, {e}.')
    
#dash app and layout
app = dash.Dash(__name__,suppress_callback_exceptions=True)

app.layout = html.Div([ 
    #overall dashboard
    html.H2("Feedback based Sentiment Analytics Dashboard"),
    html.Div ([ 
        #tab area
        html.Div([ 
            html.H3("Tab Menu"),
            dcc.Tabs(
                id='main_tab_option', value='option-1',
                children=[
                    dcc.Tab(label="Overview Sentiment Distribution", value="option-1", className='vt-tab', selected_className='vt-tab-selected'),
                    dcc.Tab(label="Time-Based Analysis", value="option-2", className='vt-tab', selected_className='vt-tab-selected'),
                    dcc.Tab(label="Geographical Analysis", value="option-3", className='vt-tab', selected_className='vt-tab-selected'),
                    dcc.Tab(label="Word Analysis", value="option-4", className='vt-tab', selected_className='vt-tab-selected'),
                    dcc.Tab(label="Others", value="option-5", className='vt-tab', selected_className='vt-tab-selected')
                ],vertical=True
            )
        ], className="vt-tabs-container"),
        #content area
        html.Div([
            # Tab 1 container
            html.Div([
                html.H4("Overview Sentiment Distribution"),
                dcc.Dropdown(
                    id="option1-dropdown",
                    options=[
                        {"label": "Sentiment Distribution of Feedback", "value": "A"},
                        {"label": "Sentiment Distribution by Customer Category", "value": "B"},
                        {"label": "Sentiment Distribution by Feedback Category", "value": "C"},
                        {"label": "Sentiment Distribution by Delivery", "value": "D"},
                    ],
                    value="A"
                ),
                html.Div(id="option1-output", style={'color':"#FFFFFF", 'marginTop':'10px'})
            ], id="tab1-container", style={'display':'block'}),

            # Tab 2 container
            html.Div([
                html.H4("Time-Based Analysis"),
                dcc.Dropdown(
                    id="option2-dropdown",
                    options=[
                        {"label": "Sentiment Trend by Year", "value": "A"},
                        {"label": "Sentiment Trend by Month", "value": "B"},
                        {"label": "Sentiment Trend by Day", "value": "C"},
                        {"label": "Sentiment Trend by Order Hour", "value": "D"},
                    ],
                    value="A"
                ),
                html.Div(id="option2-output", style={'color':"#FFFFFF", 'marginTop':'10px'})
            ], id="tab2-container", style={'display':'none'}),

            # Tab 3 container
            html.Div([
                html.H4("Geographical Analysis"),
                dcc.Graph(figure=geo_analysis(df), style={'color': "#FFFFFF", 'marginTop': '10px'})
            ], id="tab3-container", style={'display':'none'}),

            # Tab 4 container
            html.Div([
                html.H4("Word Analysis"),
                dcc.Dropdown(
                    id="option4-dropdown",
                    options=[
                        {"label": "Wordcloud Analysis", "value": "A"},
                        {"label": "Most Common Overall Words", "value": "B"},
                        {"label": "Most Common Positive Words", "value": "C"},
                        {"label": "Most Common Negative Words", "value": "D"},
                        {"label": "Most Common Neutral Words", "value": "E"},
                    ],
                    value="A"
                ),
                html.Div(id="option4-output", style={'color':"#FFFFFF", 'marginTop':'10px'})
            ], id="tab4-container", style={'display':'none'}),

            # Tab 5 container
            html.Div([
                html.H4("Others"),
                dcc.Dropdown(
                    id="option5-dropdown",
                    options=[
                        {"label": "Correlation Table", "value": "A"},
                        {"label": "Used Model Classification Report", "value": "B"},
                        {"label": "Summary Analysis", "value": "C"},
                    ],
                    value="A"
                ),
                html.Div(id="option5-output", style={'color':"#FFFFFF", 'marginTop':'10px'})
            ], id="tab5-container", style={'display':'none'}),

        ], className="vt-content")
    ], className="vt-main")
], className="ovr-board")

# Callback to toggle which tab container is visible
@app.callback(
    Output("tab1-container","style"),
    Output("tab2-container","style"),
    Output("tab3-container","style"),
    Output("tab4-container","style"),
    Output("tab5-container","style"),
    Input("main_tab_option","value")
)
def show_tab(selected_tab):
    return (
        {'display':'block'} if selected_tab=="option-1" else {'display':'none'},
        {'display':'block'} if selected_tab=="option-2" else {'display':'none'},
        {'display':'block'} if selected_tab=="option-3" else {'display':'none'},
        {'display':'block'} if selected_tab=="option-4" else {'display':'none'},
        {'display':'block'} if selected_tab=="option-5" else {'display':'none'},
    )
# Callbacks for dropdowns
@app.callback(
    Output("option1-output", "children"),
    Input("option1-dropdown", "value")
)
def dropdown1(value):
    if value == "A":
        fig = count_analysis(df)
        return dcc.Graph(figure=fig)
    elif value == "B":
        fig = customer_analysis(df)
        return dcc.Graph(figure=fig)
    elif value == "C":
        fig = category_analysis(df)
        return dcc.Graph(figure=fig)
    else:
        fig = delivery_analysis(df)
        return dcc.Graph(figure=fig)

@app.callback(
    Output("option2-output", "children"),
    Input("option2-dropdown", "value")
)
def dropdown2(value):
    if value == "A":
        fig = year_analysis(df)
        return dcc.Graph(figure=fig)
    elif value == "B":
        fig = month_analysis(df)
        return dcc.Graph(figure=fig)
    elif value == "C":
        fig = day_analysis(df)
        return dcc.Graph(figure=fig)
    else:
        fig = hour_analysis(df)
        return dcc.Graph(figure=fig)
    

@app.callback(
    Output("option4-output", "children"),
    Input("option4-dropdown", "value")
)
def dropdown4(value):
    if value == "A":
        fig = wordcloud_analysis(df)
        return dcc.Graph(figure=fig)
    elif value == "B":
        fig = com_word_analysis(df)
        return dcc.Graph(figure=fig)
    elif value == "C":
        fig = pos_word_analysis(df)
        return dcc.Graph(figure=fig)
    elif value == "D":
        fig = neg_word_analysis(df)
        return dcc.Graph(figure=fig)
    else:
        fig = neu_word_analysis(df)
        return dcc.Graph(figure=fig)

@app.callback(
    Output("option5-output", "children"),
    Input("option5-dropdown", "value")
)
def dropdown5(value):
    if value == "A":
        fig = correlation_analysis(df)
        return dcc.Graph(figure=fig)
    elif value == "B":
        return html.Div([model_analysis(df)])
    else:
        return html.Div([summary_analysis(df)])


#run dashboard
if __name__ == "__main__":
    app.run(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
