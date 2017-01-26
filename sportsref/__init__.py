# flake8: noqa

SITE_ABBREV = {
    'http://www.pro-football-reference.com': 'pfr',
    'http://www.basketball-reference.com': 'bkref',
    'http://www.sports-reference.com/cfb': 'ncaaf',
    'http://www.sports-reference.com/cbb': 'ncaab',
}

import decorators
import utils
import nfl
import nba
import ncaaf

__all__ = ['decorators', 'utils', 'nfl', 'nba', 'ncaaf', 'SITE_ABBREV']
