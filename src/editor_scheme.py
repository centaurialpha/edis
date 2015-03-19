# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Edis Scheme
EDIS_SCHEME = {
    'BackgroundEditor': '#0E0F12',
    'Color': '#E2E2E5',
    'Keyword': '#7E8AA2',
    'Comment': '#3F3F3F',
    'CommentLine': '#3F3F3F',
    'Number': '#FF9900',
    'DoubleQuotedString': '#606060',
    'SingleQuotedString': '#606060',
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
    'SidebarFore': '#B3B3B3',
    'FoldMarginBack': '#262626',
    'FoldMarginFore': '#262626',
    'error': '#DF3E3E'
    }

# Based on Code::Blocks
CB_SCHEME = {
    'BackgroundEditor': '#FFFFFF',
    'Color': '#000000',
    'Keyword': '#0000A0',
    'Comment': '#A0A0A0',
    'CommentLine': '#BEBEE6',
    'Number': '#F000F0',
    'DoubleQuotedString': '#0000FF',
    'SingleQuotedString': '#E0A000',
    'PreProcessor': '#00A000',
    'Operator': '#FF0000',
    'MatchedBraceFore': '#000000',
    'MatchedBraceBack': '#80FFFF',
    'UnmatchedBraceFore': '#FFFFFF',
    'UnmatchedBraceBack': '#FF0000',
    'Margin': '#808080',
    'CaretLineBack': '#DEDEDE',
    'CaretLineFore': '#000000',
    'CaretLineAlpha': 20,
    'SidebarBack': '#D2D2D2',
    'SidebarFore': '#000000',
    'FoldMarginBack': '#D2D2D2',
    'FoldMarginFore': '#FFFFFF',
    'error': '#DF3E3E'
    }

SCHEME = {'edis': EDIS_SCHEME, 'codeblocks': CB_SCHEME}


def get_scheme(key):
    return SCHEME.get(key, None)