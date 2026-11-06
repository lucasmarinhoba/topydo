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
Unit tests for the StatsCommand and its calculation/formatting functions.
"""

import unittest
from datetime import date

from topydo.Commands import get_subcommand
from topydo.commands.StatsCommand import (StatsCommand, calculate_stats,
                                          format_stats)
from topydo.lib.TodoList import TodoList
from topydo.ui.CLIApplicationBase import CLIApplicationBase

from .command_testcase import CommandTest


class StatsCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        self.todolist = TodoList([])

    def test_stats_empty_list(self):
        """ Tests stats command execution on an empty todo list. """
        command = StatsCommand([], self.todolist, self.out, self.error)
        result = command.execute()

        self.assertTrue(result)
        self.assertIn("Total tasks: 0", self.output)
        self.assertIn("Completed:   0", self.output)
        self.assertIn("Pending:     0", self.output)
        self.assertIn("Overdue:     0", self.output)
        self.assertNotIn("Tasks by project:", self.output)
        self.assertEqual(self.errors, "")

    def test_calculate_stats_metrics(self):
        """ Tests calculation logic with mixed tasks and reference date. """
        tasks = [
            "(A) Task 1 +ProjectA due:2026-11-01",
            "(B) Task 2 +ProjectB due:2026-11-10",
            "x 2026-11-02 Completed past due +ProjectA due:2026-11-01",
            "Task without due date +ProjectA +ProjectB",
            "(C) Task due today due:2026-11-05",
        ]
        todolist = TodoList(tasks)
        ref_date = date(2026, 11, 5)

        stats = calculate_stats(todolist, p_reference_date=ref_date)

        self.assertEqual(stats['total'], 5)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['pending'], 4)
        self.assertEqual(stats['overdue'], 1)
        self.assertEqual(stats['projects'], {'ProjectA': 3, 'ProjectB': 2})

    def test_stats_invalid_due_dates(self):
        """ Tests tasks with malformed or invalid due dates. """
        tasks = [
            "(A) Invalid date string +Proj due:not-a-date",
            "(B) Invalid calendar date +Proj due:2026-99-99",
            "Task with empty due tag due:",
        ]
        todolist = TodoList(tasks)
        ref_date = date(2026, 11, 5)

        stats = calculate_stats(todolist, p_reference_date=ref_date)

        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['completed'], 0)
        self.assertEqual(stats['pending'], 3)
        self.assertEqual(stats['overdue'], 0)
        self.assertEqual(stats['projects'], {'Proj': 2})

    def test_stats_execution_with_tasks(self):
        """ Tests complete command execution with sample tasks. """
        tasks = [
            "(A) 2026-10-01 Item 1 +Faculdade @comp due:2026-10-15",
            "(B) 2026-11-01 Item 2 +Faculdade @estudos due:2026-11-10",
            "x 2026-10-20 Item 3 +Faculdade @leitura",
            "Item 4 +Pessoal @mercado",
            "(C) Item 5 +Pessoal @financas due:2026-10-25",
        ]
        self.todolist = TodoList(tasks)
        command = StatsCommand([], self.todolist, self.out, self.error)
        result = command.execute()

        self.assertTrue(result)
        self.assertIn("Total tasks: 5", self.output)
        self.assertIn("Completed:   1", self.output)
        self.assertIn("Pending:     4", self.output)
        self.assertIn("Tasks by project:", self.output)
        self.assertIn("+Faculdade: 3", self.output)
        self.assertIn("+Pessoal: 2", self.output)
        self.assertEqual(self.errors, "")

    def test_stats_help(self):
        """ Tests the help interceptor for stats command. """
        command = StatsCommand(["help"], self.todolist, self.out, self.error)
        result = command.execute()

        self.assertFalse(result)
        self.assertIn("Synopsis: stats", self.errors)
        self.assertIn("Displays summary statistics", self.errors)

    def test_format_stats_portuguese(self):
        """ Tests formatting with Portuguese language option. """
        sample_stats = {
            'total': 10,
            'completed': 4,
            'pending': 6,
            'overdue': 2,
            'projects': {'ProjetoX': 5},
        }
        lines = format_stats(sample_stats, p_lang='pt')
        joined = "\n".join(lines)

        self.assertIn("Estatísticas do TodoList:", joined)
        self.assertIn("Total de tarefas: 10", joined)
        self.assertIn("Concluídas:       4", joined)
        self.assertIn("Pendentes:        6", joined)
        self.assertIn("Atrasadas:        2", joined)
        self.assertIn("Tarefas por projeto:", joined)
        self.assertIn("+ProjetoX: 5", joined)

    def test_format_stats_invalid_language_fallback(self):
        """ Tests fallback to English when an unknown language is passed. """
        sample_stats = {
            'total': 2,
            'completed': 1,
            'pending': 1,
            'overdue': 0,
            'projects': {},
        }
        lines = format_stats(sample_stats, p_lang='invalid_lang')
        joined = "\n".join(lines)

        self.assertIn("Todo List Statistics:", joined)
        self.assertIn("Total tasks: 2", joined)

    def test_stats_subcommand_registration(self):
        """ Tests that stats is properly registered and read-only. """
        cmd_class, args = get_subcommand(["stats"])
        self.assertTrue(issubclass(cmd_class, StatsCommand))
        self.assertEqual(args, [])
        self.assertTrue(CLIApplicationBase.is_read_only(StatsCommand))


if __name__ == '__main__':
    unittest.main()
