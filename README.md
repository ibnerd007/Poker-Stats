# Poker-Stats
# Python program that keeps track of a variety of poker stats by player using a PokerNow log and ledger file
Designed and written by ibnerd007 for use with the logs and ledgers generated from a session on the online poker website www.pokernow.club

Stats tracked:

- VPIP (Voluntarily Put in Pot) (%)
- Pre-flop Raise (%)
- 3-bet Pre-flop (%)
- Aggression Factor (# of bets + # of raises / # of calls)
- Aggression Frequency (%)
- C-bet percentage (# of c-bets / # of opportunities to c-bet) (%)
- Went to showdown (%)
- Won at showdown (absolute) (%)
- Won at showdown (relative to "Went to showdown") (%)
- Money won at showdown ($)
- Money won before showdown ($)
- Hands played during session

*Note: All stats are tracked positionally as well (except money won), and can be viewed in command line output.

Run main script -> `runPokerStats.py` (contains GUI)

Once the program is running, choose the desired date to see specific stats from the dropdown menu. The dropdown shows all available
dates in the `\Poker-Stats\Logs` directory.

Next, choose whether command line output is desired using the checkboxes. You can print stats from Texas Holdem, PLO, or combined.
The command line option will show positional statistics as well in table form. Positional Excel output will be released in a future update.

Click `Run`. The program will run, and display the session date, people that played, and the types of poker played (Holdem, PLO, or both).
Open any Excel spreadsheet to view the new data and corresponding charts.

The program will fill the following workbooks for the session specified:

- stats.xlsx                 (shows poker stats from current session)
- net_over_time_raw.xlsx     (shows raw (not averaged) net gain/loss for each player, for current session, overlaid on one chart)
- net_over_time_avg.xlsx     (shows 10-hand moving average of net gain/loss for each player, for current session, overlaid on one chart)
- stacks_over_time_raw.xlsx  (shows raw (not averaged) stack for each player, for current session, overlaid on one chart)
- stacks_over_time_avg.xlsx  (shows 10-hand moving average of each player's stack, for current session, overlaid on one chart)

stacks_over_time shows a player's stack size throughout the session, but cannot be less than zero. It shows when a player added on and their stack
at any point, but does not necessarily reflect net gain/loss.
net_over_time shows a player's net gain/loss throughout the session, but does not show when a player added on and what their actual stack is.

The program will also fill the following multi-session workbooks for the specified date, if data for said date has not already been entered during 
runtime of a previous instance of PokerStats:

- bankrolls.xlsx        (tracks certain players' net gain/loss over many sessions, regardless of poker type played)
- stat averages.xlsx    (tracks all-time averages of players' stats over many session, sorted by poker type)
- stats over time.xlsx  (tracks players' stats across multiple sessions, but instead of averaging, puts them side by side for trend comparison)

The program will fill the stats.xlsx workbook. It will also fill net over time and stacks over time, both average and raw, for the 
session specified. Average stats, bankroll information, and stats over time for the selected session date will be filled, if that date 
has not already been entered.

When viewing statistics from the current session in Excel, be sure to look at the date shown in the upper right corner. The Excel sheets
will not be touched by the program if no hands of that type were played on the session, so it may show old data from a different date.

*NOTE: The players of which you want to keep track for average stats, stats over time, and bankrolls must be hard-coded into the program.
You just need their 10-digit ID and nickname.
