# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <bram@topydo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Command to display summary statistics of the todo list.
"""

from collections import Counter
from datetime import date

from topydo.lib.Command import Command

DEFAULT_LANG = 'en'

LABELS = {
    'en': {
        'title': "Todo List Statistics:",
        'total': "  Total tasks: {}",
        'completed': "  Completed:   {}",
        'pending': "  Pending:     {}",
        'overdue': "  Overdue:     {}",
        'projects_header': "Tasks by project:",
        'project_item': "  +{}: {}",
        'synopsis': "Synopsis: stats",
        'help': "Displays summary statistics of the todo list.",
    },
    'pt': {
        'title': "Estatísticas do TodoList:",
        'total': "  Total de tarefas: {}",
        'completed': "  Concluídas:       {}",
        'pending': "  Pendentes:        {}",
        'overdue': "  Atrasadas:        {}",
        'projects_header': "Tarefas por projeto:",
        'project_item': "  +{}: {}",
        'synopsis': "Sinopse: stats",
        'help': "Exibe um resumo estatístico da lista de tarefas.",
    },
}


def _is_overdue(p_todo, p_reference_date):
    """ Returns True when a pending task has a valid due date in the past. """
    if p_todo.is_completed():
        return False

    due = p_todo.due_date()
    return bool(due and due < p_reference_date)


def _count_projects(p_todos):
    """ Returns a case-insensitively sorted dictionary of project counts. """
    counts = Counter()
    for todo in p_todos:
        for project in todo.projects():
            counts[project] += 1

    return dict(sorted(counts.items(), key=lambda item: item[0].lower()))


def calculate_stats(p_todolist, p_reference_date=None):
    """
    Computes statistical metrics for the given todo list.

    Returns a dictionary containing counts of total, completed, pending,
    overdue tasks, and a breakdown of tasks by project.
    """
    reference_date = p_reference_date or date.today()
    todos = p_todolist.todos()

    total = len(todos)
    completed = sum(1 for todo in todos if todo.is_completed())
    overdue = sum(1 for todo in todos if _is_overdue(todo, reference_date))

    return {
        'total': total,
        'completed': completed,
        'pending': total - completed,
        'overdue': overdue,
        'projects': _count_projects(todos),
    }


def format_stats(p_stats, p_lang=DEFAULT_LANG):
    """
    Formats the statistical dictionary into a list of human-readable strings.
    """
    labels = LABELS.get(p_lang, LABELS['en'])

    lines = [
        labels['title'],
        labels['total'].format(p_stats['total']),
        labels['completed'].format(p_stats['completed']),
        labels['pending'].format(p_stats['pending']),
        labels['overdue'].format(p_stats['overdue']),
    ]

    projects = p_stats.get('projects', {})
    if projects:
        lines.append("")
        lines.append(labels['projects_header'])
        for project, count in projects.items():
            lines.append(labels['project_item'].format(project, count))

    return lines


class StatsCommand(Command):
    """
    Represents the 'stats' subcommand in topydo.
    """

    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        if not super().execute():
            return False

        stats = calculate_stats(self.todolist)
        for line in format_stats(stats, DEFAULT_LANG):
            self.out(line)
        return True

    def usage(self):
        labels = LABELS.get(DEFAULT_LANG, LABELS['en'])
        return labels['synopsis']

    def help(self):
        labels = LABELS.get(DEFAULT_LANG, LABELS['en'])
        return labels['help']
