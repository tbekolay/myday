from __future__ import absolute_import

from datetime import datetime
from time import mktime

import parsedatetime
import recurrent
from dateutil.rrule import rrulestr


def matches_today(repeat):
    """Determine if today is included in a natural language recurrence.

    A natural language recurrence is something like "daily", "every monday",
    "the first Tue of the month", and so on.
    """
    cal = parsedatetime.Calendar()

    # Parses to an RRULE string, which is then dealt with by dateutil;
    # see http://www.kanzaki.com/docs/ical/rrule.html for RRULE info.
    rrule = rrulestr(recurrent.parse(repeat))
    daystart = datetime.fromtimestamp(mktime(cal.parse("today at 00:00")[0]))
    dayend = datetime.fromtimestamp(mktime(cal.parse("today at 23:59")[0]))
    matches = rrule.between(after=daystart, before=dayend)
    return len(matches) > 0
