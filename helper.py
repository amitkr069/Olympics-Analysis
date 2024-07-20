import numpy as np
import pandas as pd

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    # year ka
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    # country ka
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country


# now country and year select krne wala

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1  # kisi country ka year wise meadal chahiye
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': 'No_of_countries'}, inplace=True)
    return nations_over_time

def all_events_over_time(df):
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year')
    events_over_time.rename(columns={'Year': 'Edition', 'count': 'No_of_Events'}, inplace=True)
    return events_over_time

def all_athletes_over_time(df):
    athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('Year')
    athletes_over_time.rename(columns={'Year': 'Edition', 'count': 'No_of_Athletes'}, inplace=True)
    return athletes_over_time

def most_successful(df, sport):
  temp_df = df.dropna(subset=['Medal'])

  if sport != 'Overall':
    temp_df = temp_df[temp_df['Sport'] == sport] # wo particular port temp df me store hoga

  x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
  x.rename(columns={'count': 'Medals'}, inplace=True)
  return x

def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    new_df = df[df['region'] == country]
    new_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    # new_df.pivot_table(index = 'Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')
    return pt

#now for most successful atheletes

def most_successful_ath(df, country):
  temp_df = df.dropna(subset=['Medal'])

  temp_df = temp_df[temp_df['region'] == country]

  x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[['Name', 'count', 'Sport']].drop_duplicates('Name')
  x.rename(columns={'count': 'Medals'}, inplace=True)
  return x

def weight_v_height(df, sport):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    # now height and weight analysis
    athelete_df['Medal'].fillna("No Medal", inplace=True)
    if sport != 'Overall':
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        return temp_df
    else:
        return athelete_df

def men_vs_women(df):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    # now for men and women participation over the years

    men = athelete_df[athelete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athelete_df[athelete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final