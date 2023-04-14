# Lootius
 Entropia universe Loot tracker, with more features soonTM

after isntalli8ng wxpython with python 3.11.1
fix this manually https://github.com/wxWidgets/Phoenix/issues/2297 \
on windows venv set pypath http://chrisspearswebdev.blogspot.com/2014/08/setting-pythonpath-with-powershell.html

mvc layout
- Project Lootius (repo)\
|   - app(project)\
|   |   - Modules (modules used by other functions)\
|   |   - Views (frontend gui etc.)\
|   |   - Models (models used by controllers)\
|   |   - Database (database related functions/models)\
|   |   Lootius.py\
|   - data (raw data)\
|   - tests unit tests\
|   - docs\
| .gitignore\
| .gitattibutes\
| README.md\
| requirments.txt

---
https://newville.github.io/wxmplot/examples.html for graphs \
https://realpython.com/python-logging/ logging?

database stuffs:\
https://stackoverflow.com/a/70238438

---

dmg enhancer calc == base dmg +10% per tier enhancer

Dev Notes (tmp):\
manage seperate hunting runs (exel format?)\
long term stats, split by cat, hunting mining crafting?\
healer mode (pure tracking of healing costs/returns/clientmanagement) split heal points and done by self and others (if you heal self and others during run you can see how much you spent/amount/healed per person) \
stream overlays/ez-customize + none easy customize\
custom maps with easy copy paste wp for ingame use.\
mining tracker (manual use as no ocr, copy paste wp from claim and add size) (later select claim or extract directly to log precise tt value of ores) / map\
team tracker, loot split calc etc. screenshots.\
skill tracker / damage tracker.\
decay values in tuples/unmutable database, to counter eco tampering.\

keep in mind crit dmg +1% and +2% and ranger scope\
relaodd speed from rings etc to show dps on stream overlay later\
long term goals:\
web based service if enough ned for it, including accounts etc.\

py c:\Users\ndvds\Development\wxGlade-1.0.4\wxglade.py 