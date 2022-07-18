import requests as r 
from psycopg2 import connect
from config import *
from time import strftime

def log(level, message):
    levels = ['INFO', 'WARN', 'ERROR']
    print(strftime('%Y-%m-%d %H:%M:%S ') + levels[level] + ': ' + message)

def getDataFromAPI(api_url):
    global err_cnt
    log(0, 'Requesting data from API: {}'.format(api_url))
    try:
        response = r.get(api_url)
        if response.status_code != 200:
            raise ValueError(response.text)
        data = response.json()
        log(0, 'Successfully got data from API')
        return data['stats']
    except Exception as e:
        log(2, 'Unable to get data from API: {}'.format(e))
        err_cnt += 1
        return None
    
def loadStatsSingleSeasonData(data, cursor):
    global err_cnt
    log(0, 'Loading statsSingleSeason...')
    try:
        gametype_values = [data['type']['gameType']['id'], 
                            data['type']['gameType']['description'], 
                            data['type']['gameType']['postseason']]

        for team in data['splits']:
            team_values = [team['team']['id'],
                            team['team']['name']]
            stat_values = list(team['stat'].values())
            insert_values = tuple(team_values + gametype_values + stat_values)

            cursor.execute('''insert into stg."statsSingleSeason" values %s''', (insert_values,))
        
        log(0, 'statsSingleSeason load complete')
    except Exception as e:
        log(2, 'Unable to load statsSingleSeason due to {}'.format(e))
        err_cnt += 1
        
def loadRegularSeasonStatRankingsData(data, cursor):
    global err_cnt
    log(0, 'Loading regularSeasonStatRankings...')
    try:
        for team in data['splits']:
            team_values = [team['team']['id'],
                            team['team']['name']]
            stat_values = list(team['stat'].values())
            insert_values = tuple(team_values + stat_values)

            cursor.execute('''insert into stg."regularSeasonStatRankings" values %s''', (insert_values,))
        
        log(0, 'regularSeasonStatRankings load complete')
    except Exception as e:
        log(2, 'Unable to load statsSingleSeason due to {}'.format(e))
        err_cnt += 1
        
def loadDataToDB(data):
    global err_cnt
    log(0, 'Connecting to DB {}:{}/{} as {}'.format(host, port, dbname, user))
    try:
        conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
        cur = conn.cursor()
        for stats_record in data:
            if stats_record['type']['displayName'] == 'statsSingleSeason':
                loadStatsSingleSeasonData(stats_record, cur)
            elif stats_record['type']['displayName'] == 'regularSeasonStatRankings':
                loadRegularSeasonStatRankingsData(stats_record, cur)
            else:
                log(1, 'Unknown stats type: {}. Skipping...'.format(stats_record['type']['displayName']))
        if err_cnt != 0:
            raise ValueError('Error while loading data, all transactions rolled back')
        conn.commit()
        conn.close()
    except Exception as e:
        log(2, 'Unable to load data to DB due to {}'.format(e))
        err_cnt += 1

if __name__ == '__main__':
    err_cnt = 0
    log(0, 'Pipeline started')
    data = getDataFromAPI(api_url)
    if err_cnt == 0:
        loadDataToDB(data)
    pipeline_status = 'successfully' if err_cnt == 0 else 'with errors'
    log(0, 'Pipeline finished ' + pipeline_status)