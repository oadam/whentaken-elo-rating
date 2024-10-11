# elo rating system for whentaken

    echo '<all your recent chat logs>' | ./convert.py | tee new-lines.csv
    # add all converted lines to online backup and pull the whole lines.csv
    ./elo.py < lines.csv |tee result.csv
