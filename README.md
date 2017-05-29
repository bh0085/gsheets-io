# gsheets-io



default share email (used by ben):

# api key username
<pre><code>untappd-python-reporting@polished-bounty-162720.iam.gserviceaccount.com</pre></code>


# sample commands

### occupancy reports
./get-google-sheet.py --sqlite --sheet="1EOzXwcts0nBFjQIMMfK6i6D4jk_AIbtNHCFvjmUfCF0" --name="DATABASE" --header-rows=4 --types-row=2 --index-row=3 --table=linedata --output=occupancy.db

### shows output
./get-google-sheet.py --sqlite --sheet="1WWOD92D7SvCVh2Hlu-0dyyuIOctn7UMVMSOPoFBbGgI" --name="DATABASE" --header-rows=4 --types-row=2 --index-row=3 --table=bands --output=bands.db
