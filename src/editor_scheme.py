# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Edis Scheme
EDIS_DARK_SCHEME = {
    'BackgroundEditor': '#0E0F12',
    'Color': '#E2E2E5',
    'Keyword': '#7E8AA2',
    'Comment': '#3F3F3F',
    'CommentLine': '#3F3F3F',
    'Number': '#FF9900',
    'DoubleQuotedString': '#606060',
    'SingleQuotedString': '#96FF00',
    'PreProcessor': '#FAF4C6',
    'Operator': '#E2E2E5',
    'MatchedBraceFore': '#FFFFFF',
    'MatchedBraceBack': '#044888',
    'UnmatchedBraceFore': '#FFFFFF',
    'UnmatchedBraceBack': '#FF0000',
    'Margin': '#808080',
    'CaretLineBack': '#DEDEDE',
    'CaretLineFore': '#FFFFFF',
    'CaretLineAlpha': 20,
    'SidebarBack': '#262626',
    'SidebarFore': '#8C8C8C',
    'FoldMarginBack': '#262626',
    'FoldMarginFore': '#262626',
    'FoldMarkerFore': '#FFFFFF',
    'FoldMarkerBack': '#000000',
    'error': '#DF3E3E'
    }

# Based on Komodo
EDIS_WHITE_SCHEME = {
    'BackgroundEditor': '#FFFFFF',
    'Color': '#000000',
    'Keyword': '#333399',
    'Comment': '#666666',
    'CommentLine': '#BEBEE6',
    'Number': '#8B0000',
    'DoubleQuotedString': '#996633',
    'SingleQuotedString': '#E0A000',
    'PreProcessor': '#696969',
    'Operator': '#781F87',
    'MatchedBraceFore': '#FFFFFF',
    'MatchedBraceBack': '#333399',
    'UnmatchedBraceFore': '#FFFFFF',
    'UnmatchedBraceBack': '#FF0000',
    'Margin': '#C2C2C2',
    'CaretLineBack': '#DEDEDE',
    'CaretLineFore': '#000000',
    'CaretLineAlpha': 50,
    'SidebarBack': '#F5F5F5',
    'SidebarFore': '#C2C2C2',
    'FoldMarginBack': '#F7F7F7',
    'FoldMarginFore': '#F7F7F7',
    'FoldMarkerFore': '#F7F7F7',
    'FoldMarkerBack': '#C2C2C2',
    'error': '#DF3E3E'
    }

SCHEME = {'dark': EDIS_DARK_SCHEME, 'white': EDIS_WHITE_SCHEME}


def get_scheme(key):
    return SCHEME.get(key, None)
