# coding: utf-8
import json, sys, getopt
from datetime import date
from pyquery import PyQuery as pq

seasons = []
teams = {
  'diamondbacks' : 'ARI',
  'braves'       : 'ATL',
  'orioles'      : 'BAL',
  'red-sox'      : 'BOS',
  'redsox'       : 'BOS',
  'cubs'         : 'CHC',
  'white-sox'    : 'CHW',
  'whitesox'     : 'CHW',
  'reds'         : 'CIN',
  'indians'      : 'CLE',
  'rockies'      : 'COL',
  'tigers'       : 'DET',
  'astros'       : 'HOU',
  'royals'       : 'KCR',
  'angels'       : 'LAA',
  'dodgers'      : 'LAD',
  'marlins'      : 'MIA',
  'brewers'      : 'MIL',
  'twins'        : 'MIN',
  'mets'         : 'NYM',
  'yankees'      : 'NYY',
  'athletics'    : 'OAK',
  'phillies'     : 'PHI',
  'pirates'      : 'PIT',
  'padres'       : 'SDP',
  'giants'       : 'SFG',
  'mariners'     : 'SEA',
  'cardinals'    : 'STL',
  'rays'         : 'TBR',
  'rangers'      : 'TEX',
  'blue-jays'    : 'TOR',
  'bluejays'     : 'TOR',
  'nationals'    : 'WSN'
}

def main():
  team = False
  firstyear = lastyear = date.today().year # Default to current year

  try:
    opts, args = getopt.getopt(sys.argv[1:],"ht:f:l:",["team=","firstyear=","lastyear="])
  except getopt.GetoptError as error:
    print error
    print 'scrape.py -t <team> -f <first year> -l <last year>'
    sys.exit()
  for opt, arg in opts:
    if opt == '-h':
       print 'scrape.py -t <team> -f <first year> -l <last year>'
       sys.exit()
    elif opt in ("-t", "--team"):
       team = arg
    elif opt in ("-f", "--firstyear"):
       firstyear = int(arg)
    elif opt in ("-l", "--lastyear"):
       lastyear = int(arg)
  if not team:
    print 'A team is required.'
    print 'scrape.py -t <team> -f <first year> -l <last year>'
    sys.exit()

  team = team.lower()
  if not team in teams:
    print 'That team wasn’t found.'
    print 'Use a hyphen for two-word names, such as “White-Sox” for the White Sox.'
    print 'Use “Athletics” for the A’s.'
    print 'scrape.py -t <team> -f <first year> -l <last year>'
    sys.exit()

  team = teams[team]
  if lastyear < firstyear:
    lastyear = firstyear

  for year in xrange(firstyear,lastyear + 1):
    year            = str(year)
    url             = 'http://www.baseball-reference.com/teams/' + team + '/' + year + '-schedule-scores.shtml'
    d               = pq(url=url)
    rows            = d('#team_schedule tbody tr')
    season          = []
    runDifferential = 0

    for r in rows:
      cells      = d(r).children('td')
      ourScore   = 0
      oppScore   = 0
      gameNumber = 0
      row        = []
      for c in cells:
        row.append(d(c).text())
      try:
        gameNumber = row[1]
        ourScore   = int(row[8])
        oppScore   = int(row[9])
        result     = row[7]

        runDifferential = runDifferential + ourScore - oppScore

        if int(gameNumber) > 0 and 'T' not in result:
          day = [gameNumber,ourScore,oppScore,runDifferential]
          season.append(day)
      except:
        pass
    print 'Run differential in ' + year + ': ' + str(runDifferential)

    seasonLog = [0]

    for day in season:
      seasonLog.append(day[3])
    seasonJson = {'year':year, "runDiff": runDifferential, "log": seasonLog}
    seasons.append(seasonJson)

  jsonFile = open('runlog-' + team + '-' + str(firstyear) + '-' + str(lastyear) + '.js','w')
  jsonFile.write(json.dumps(seasons))

if __name__ == "__main__":
   main()

