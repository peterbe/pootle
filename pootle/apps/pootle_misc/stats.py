#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Zuza Software Foundation
#
# This file is part of Pootle.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from django.utils.translation import ugettext_lazy as _, ungettext

from pootle_app.views.language import dispatch
from pootle_misc.util import add_percentages


def get_raw_stats(path_obj, include_suggestions=False):
    """Returns a dictionary of raw stats for `path_obj`.

    :param path_obj: A Directory/Store object.
    :param include_suggestions: Whether to include suggestion count in the
                                output or not.

    Example::

        {'translated': {'units': 0, 'percentage': 0, 'words': 0},
         'fuzzy': {'units': 0, 'percentage': 0, 'words': 0},
         'untranslated': {'units': 34, 'percentage': 100, 'words': 181},
         'total': {'units': 34, 'percentage': 100, 'words': 181}
         'suggestions': 4 }
    """
    quick_stats = add_percentages(path_obj.getquickstats())

    stats = {
        'total': {
            'words': quick_stats['totalsourcewords'],
            'percentage': 100,
            'units': quick_stats['total'],
            },
        'translated': {
            'words': quick_stats['translatedsourcewords'],
            'percentage': quick_stats['translatedpercentage'],
            'units': quick_stats['translated'],
            },
        'fuzzy': {
            'words': quick_stats['fuzzysourcewords'],
            'percentage': quick_stats['fuzzypercentage'],
            'units': quick_stats['fuzzy'],
            },
        'untranslated': {
            'words': quick_stats['untranslatedsourcewords'],
            'percentage': quick_stats['untranslatedpercentage'],
            'units': quick_stats['untranslated'],
            },
        'errors': quick_stats['errors'],
        'suggestions': -1,
    }

    if include_suggestions:
        stats['suggestions'] = path_obj.get_suggestion_count()

    return stats


def get_translation_stats(directory, dir_stats):
    """Returns a list of statistics ready to be displayed."""

    stats = []

    if dir_stats['total']['units'] > 0:
        stats.append({
            'title': _("Total"),
            'words': _('<a href="%(url)s">%(num)d words</a>') % \
                {'url': dispatch.translate(directory),
                 'num': dir_stats['total']['words']},
            'percentage': _("%(num)d%%") % \
                {'num': dir_stats['total']['percentage']},
            'units': _("(%(num)d units)") % \
                {'num': dir_stats['total']['units']}
        })

    if dir_stats['translated']['units'] > 0:
        stats.append({
            'title': _("Translated"),
            'words': _('<a href="%(url)s">%(num)d words</a>') % \
                {'url': dispatch.translate(directory, state='translated'),
                 'num': dir_stats['translated']['words']},
            'percentage': _("%(num)d%%") % \
                {'num': dir_stats['translated']['percentage']},
            'units': _("(%(num)d units)") % \
                {'num': dir_stats['translated']['units']}
        })

    if dir_stats['fuzzy']['units'] > 0:
        stats.append({
            'title': _("Fuzzy"),
            'words': _('<a href="%(url)s">%(num)d words</a>') % \
                {'url': dispatch.translate(directory, state='fuzzy'),
                 'num': dir_stats['fuzzy']['words']},
            'percentage': _("%(num)d%%") % \
                {'num': dir_stats['fuzzy']['percentage']},
            'units': _("(%(num)d units)") % \
                {'num': dir_stats['fuzzy']['units']}
        })

    if dir_stats['untranslated']['units'] > 0:
        stats.append({
            'title': _("Untranslated"),
            'words': _('<a href="%(url)s">%(num)d words</a>') % \
                {'url': dispatch.translate(directory, state='untranslated'),
                 'num': dir_stats['untranslated']['words']},
            'percentage': _("%(num)d%%") % \
                {'num': dir_stats['untranslated']['percentage']},
            'units': _("(%(num)d units)") % \
                {'num': dir_stats['untranslated']['units']}
        })

    return stats


def get_directory_summary(directory, dir_stats):
    """Returns a list of sentences to be displayed for each directory."""
    summary = [
        ungettext("This folder has %(num)d word, %(percentage)d%% of which is "
           "translated",
           "This folder has %(num)d words, %(percentage)d%% of which are "
           "translated",
           dir_stats['total']['words']) % {
               'num': dir_stats['total']['words'],
               'percentage': dir_stats['translated']['percentage']
           }
    ]

    if dir_stats['untranslated']['words'] > 0 or dir_stats['fuzzy']['words'] > 0:
        num_words = dir_stats['untranslated']['words'] + dir_stats['fuzzy']['words']
        summary.append(
            ungettext('<a class="directory-incomplete" href="%(url)s">%(num)d '
               'word needs translation</a>',
               '<a class="directory-incomplete" href="%(url)s">%(num)d words '
               'need translation</a>',
               num_words) % {
                   'num': num_words,
                   'url': dispatch.translate(directory, state='incomplete')
               }
        )

    if dir_stats['suggestions'] > 0:
        summary.append(
            ungettext('<a class="directory-incomplete" href="%(url)s">%(num)d '
               'suggestion</a> needs review',
               '<a class="directory-incomplete" href="%(url)s">%(num)d '
               'suggestions</a> need review',
               dir_stats['suggestions']) % {
                   'num': dir_stats['suggestions'],
                   'url': dispatch.translate(directory, state='suggestions')
               }
        )

    return summary
