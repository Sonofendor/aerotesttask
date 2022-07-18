import requests as r 
from psycopg2 import connect
from config import *
from time import strftime

def log(level, message):
    levels = ['INFO', 'WARN', 'ERROR']
    print(strftime('%Y-%m-%d %H:%M:%S ') + levels[level] + ': ' + message)

def getDataFromAPI(api_url):
    log(0, 'Requesting data from API: {}'.format(api_url))
    response = r.get(api_url)
    data = response.json()
    log(0, 'Successfully got data from API')
    return data 
    
def loadStatsSingleSeasonData(data, cursor):
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
        
        log(0, 'statsSingleSeason loaded successfully')
    except Exception as e:
        log(2, 'Unable to load statsSingleSeason due to {}'.format(e))
        err_cnt += 1
        
def loadRegularSeasonStatRankingsData(data, cursor):
    log(0, 'Loading regularSeasonStatRankings...')
    try:
        for team in data['splits']:
            team_values = [team['team']['id'],
                            team['team']['name']]
            stat_values = list(team['stat'].values())
            insert_values = tuple(team_values + stat_values)

            cursor.execute('''insert into stg."regularSeasonStatRankings" values %s''', (insert_values,))
        
        log(0, 'regularSeasonStatRankings loaded successfully')
    except Exception as e:
        log(2, 'Unable to load statsSingleSeason due to {}'.format(e))
        err_cnt += 1
        
def loadDataToDB(data):
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
        conn.commit()
        conn.close()
    except Exception as e:
        log(2, 'Unable to connect to DB due to {}'.format(e))
        err_cnt += 1

if __name__ == '__main__':
    err_cnt = 0
    log(0, 'Pipeline started')
    data = getDataFromAPI(api_url)['stats']
    loadDataToDB(data)
    pipeline_status = 'successfully' if err_cnt == 0 else 'with errors'
    log(0, 'Pipeline finished ' + pipeline_status)