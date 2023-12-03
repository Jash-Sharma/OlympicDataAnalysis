import numpy as np

def medal_tally(df):
    medals_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medals_df = medals_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medals_df['Total'] = medals_df['Gold']+ medals_df['Silver']+ medals_df['Bronze']
    return medals_df

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0,'All')
    return years , countries

def fetch(year,countries,medals_df):
    flag = 0
    if year == 'Overall' and countries == "All":
        temp =  medals_df
    if year == 'Overall' and countries != 'All':
        flag  = 1
        temp =  medals_df[medals_df['region'] == countries]
    if year != 'Overall' and countries == 'All':
        temp =  medals_df[medals_df['Year'] == year]
    if year != 'Overall' and countries != 'All':
        temp =  medals_df[(medals_df['region'] == countries) & (medals_df['Year'] == year)]

    if flag == 1:
        temp = temp.groupby('Year').sum()[['Gold','Silver','Bronze']].reset_index()
        temp = temp.sort_values('Year')
        flag = 0
    else:
        temp = temp.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    temp['Total'] = temp['Gold']+ temp['Silver']+ temp['Bronze']

    return temp

def most_success(df,sport):
    temp = df.dropna(subset=["Medal"])
    if sport != 'All':
        temp = temp[temp['Sport'] == sport]

    x = temp['Name'].value_counts().reset_index().merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','region']].drop_duplicates('Name').reset_index().drop('index',axis = 1)
    return x

def countrywise_medal(df,country):
    temp = df.dropna(subset=['Medal'])
    temp.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    if country != 'All':
        temp = temp[temp['region'] == country]
    final_df = temp.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    if country != 'All':
        temp_df = temp_df[temp_df['region'] == country]

    pt = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    if country != 'All':
        temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def weight_v_height(df,sport,sex):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall' and sex != 'All':
        temp_df = athlete_df[(athlete_df['Sport'] == sport) & (athlete_df['Sex'] == sex)]
        return temp_df
    if sport == 'Overall' and sex != 'All':
        temp_df = athlete_df[athlete_df['Sex'] == sex]
        return temp_df
    if sport != 'Overall' and sex == 'All':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final