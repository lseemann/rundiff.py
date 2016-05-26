# rundiff.py
Get a year-by-year, game-by-game record of a baseball team’s run differential. This is useful for historical comparisons or just to see hot and cold streaks within a season.

The program scrapes pages at [Baseball Reference](http://www.baseball-reference.com). Avoid abusing this great resource by running using only when necessary.
## Usage
From the command line:
```
python rundiff.py -t <name of team> -f <first year> -l <last year>
```

For example, `python rundiff.py -t Cubs -f 2000 -l 2014` will retrieve stats for the Chicago Cubs between 2000 and 2014, inclusive.

Data is saved in a JSON in the working directory. For each year, the daily cumulative run differential is stored, up to 163 values (for a 162-game season plus a tiebreaker). This JSON can then be used for other nifty things, such as [these D3JS charts](http://www.chicagomag.com/city-life/May-2016/Cubs-run-differential/) showing the Cubs’ hot start to the 2016 season.

First year and last years are optional. If omitted, stats for the current year will be retrieved.

## Credits
Luke Seemann, 2016