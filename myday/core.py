import io
import os
from collections import OrderedDict

import orgmode
from orgmode.compat import is_string

from myday.datetime import matches_today
from myday.exceptions import ProjectNotFound


class OrgDB(object):
    def __init__(self, *orgpaths):
        self.agenda = orgmode.OrgAgenda(*orgpaths)

    @property
    def projects(self):
        """Projects is a mapping between project names and paths."""
        projects = OrderedDict()
        for orgpath in self.agenda.files:
            projects[os.path.splitext(os.path.basename(orgpath))[0]] = orgpath
        return projects


def reset_dailies(db):
    """Reset the done state of all dailies for today."""
    for el in all_dailies(db):
        for child in el.contents:
            if isinstance(child, orgmode.OrgDrawer):
                to_del = []
                for i, prop in enumerate(child.contents):
                    if is_string(prop):
                        continue
                    if prop.name == "DONETODAY":
                        to_del.append(i)
                for i in reversed(to_del):
                    del child.contents[i]

    db.agenda.sync()


def all_dailies(db):
    """Get a list of all dailies for today."""
    tasks = []
    if 'dailies' not in db.projects:
        return dailies

    for el in db.agenda.documents[db.projects['dailies']].contents:
        if isinstance(el, orgmode.OrgSection):
            for child in el.contents:
                if isinstance(child, orgmode.OrgDrawer):
                    for prop in child.contents:
                        if prop.name == "REPEAT" and matches_today(prop.value):
                            tasks.append(el)

    return tasks


def dailies(db):
    todo, done = [], []

    for el in all_dailies(db):
        for child in el.contents:
            if (isinstance(child, orgmode.OrgDrawer)
                    and child.name == "PROPERTIES"):
                for prop in child.contents:
                    if is_string(prop):
                        continue
                    if prop.name == "DONETODAY" and prop.value == "t":
                        done.append(el)
                        break
                else:
                    todo.append(el)

    return todo, done


def mark_daily_done(db, task_ix):
    todo, _ = dailies(db)

    for child in todo[task_ix].contents:
        if isinstance(child, orgmode.OrgDrawer) and child.name == "PROPERTIES":
            # If a DONETODAY property exists, change it to t
            for prop in child.contents:
                if not is_string(prop) and prop.name == "DONETODAY":
                    prop.value = "t"
            # Otherwise add a new DONETODAY property
            else:
                child.add(orgmode.OrgProperty(
                    name="DONETODAY", value="t", indent=child.indent))
            break


def mark_done(db, task):
    try:
        # Integers correspond to dailies
        mark_daily_done(db, int(task))
    except ValueError:
        # Not an integer, so another task. Deal with this later.
        pass
    db.agenda.sync()


def task(db, project):
    """Choose a random task in a project."""
    if project not in db.projects:
        raise ProjectNotFound(project)
