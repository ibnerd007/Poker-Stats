# Poker-Stats
# Python script that keeps track of a variety of poker stats by player using a PokerNow log and ledger file
Designed and written by ibnerd007 for use with the logs and ledgers generated from a session on the online poker website www.pokernow.club

Run main script -> pokerStats.py

There are a few variables that must be set correctly before running program:

1. handTypeDesired = hand type you want to see stats for. This variable can be one of the following:
    'NL' - No Limit Texas Holdem
    'PLO' - Pot Limit Omaha Hi
    'combined' - hand type does not matter, all stats will be calculated for entire session regardless of poker type
  
2. Date = date of session. This date is used to find your PokerNow log and ledger files, which will be parsed.
    Log and ledger files should be named like this: 'log_MM DD', 'ledger_MM DD' and put in the same folder as pokerStats.py. 
    Use must use the same format to set date that you used to name the file, so that the file can be found.
    
3. Manually fill playerDictionary.txt
    Unfortunately, there isn't yet functionality to automatically fill a text file with player nicknames and IDs. Coming soon, however.
    So, you need to manually enter all player's IDs and nicknames into the dictionary file.

Once you set these variables, there are a few options for output:

1. Print stats for this session directly to command line (This is the only option currently that supports positional stats)
    At the bottom of the script, run the function 'printAllStatsForAllPlayers()'

2. Write stats for this session to an Excel spreadsheet
    At the bottom of the script, run the function 'writeCurrSessiontoExcel()'
    
    A template is included in the repository under /Outputs, called 'stats.xlsx'. It can show stats broken down by poker type,
    and organized into neat Excel charts for comparison.

3. Write stacks vs time data to a separate Excel workbook, called 'stacks over time.xlsx'.
    At the bottom of the script, run the function 'writeStacksOverTimetoExcel()' *NOTE: This function only runs if handTypeDesired = combined
    
    This function uses the module pandas to create a dataframe with all the stack values at the start of every hand for each player 
    over the course of the session. It then plots these data points in an Excel line chart for easy comparison.
    
4. Write bankroll data across multiple sessions to 'stats.xlsx'.
    At the bottom of the script, run the function 'writeBankrollsToExcel()'
    
    If you wish to keep track of players' bankroll progress over the course of multiple sessions, this function allows you to do that.
    For each session with a date that hasn't been recorded, it will plot bankroll data collected from the ledger to 'stats.xlsx'.
    This data includes the player's total net, their bankroll, their own money invested to the bankroll (only when necessary), and
    whether they played a session or not. This data is then graphed side by side for all players of interest.
    
    *NOTE: The players of which you want to keep track must be hard-coded into the function You just need their 10-digit ID and nickname.
