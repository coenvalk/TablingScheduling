# TablingScheduling
A simple tabling scheduling program that takes multiple people's available
times, and outputs a fair schedule of members at the table, within the
constraints given by each member's available times.

Makes use of dynamic programming to get as close to the optimal fairness
solution as possible.

Partial Credit is the best!
# Usage
``` python3 schedule.py ```

Requires a file named `times.csv` with all the names of the members and all
the times they are available in the working directory. Future developments will crawl scheduling websites
like whenisgiood.net to get the data automatically from the website.
