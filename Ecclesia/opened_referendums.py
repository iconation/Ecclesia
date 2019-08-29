# -*- coding: utf-8 -*-

# Copyright 2019 ICONation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from iconservice import *
from .utils import *
from .referendum import *

TAG = 'Ecclesia'


# ================================================
#  Exceptions
# ================================================
class AnswersArrayTooBig(Exception):
    pass


class ReferendumClosed(Exception):
    pass


class OpenedReferendums(object):
    # ================================================
    #  Constants
    # ================================================
    # Maximum limit of answers
    MAXIMUM_ANSWERS_COUNT = 100

    # ================================================
    #  DB Variables
    # ================================================
    # Array of opened referendums
    _OPENED_REFERENDUMS = 'OPENED_REFERENDUMS'

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self) -> None:
        pass

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def _opened_referendums(db: IconScoreDatabase) -> ArrayDB:
        return ArrayDB(OpenedReferendums._OPENED_REFERENDUMS, db, value_type=int)

    # ================================================
    #  Checks
    # ================================================
    @staticmethod
    def _check_answers_count(answers) -> None:
        if len(answers) > OpenedReferendums.MAXIMUM_ANSWERS_COUNT:
            raise AnswersArrayTooBig

    @staticmethod
    def _check_opened(db: IconScoreDatabase, uid: int) -> ArrayDB:
        if not Utils.array_db_exists(OpenedReferendums._opened_referendums(db), uid):
            raise ReferendumClosed

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def delete(db: IconScoreDatabase) -> None:
        referendums = OpenedReferendums._opened_referendums(db)
        while referendums:
            opened = referendums.pop()
            Referendum.delete(db, opened)

    @staticmethod
    def insert(db: IconScoreDatabase,
               uid: int,
               end: int,
               quorum: int,
               question: str,
               answers: list) -> Referendum:
        OpenedReferendums._check_answers_count(answers)

        OpenedReferendums._opened_referendums(db).put(uid)
        Referendum.insert(db, uid, end, quorum, question, answers)

    @staticmethod
    def vote(db: IconScoreDatabase, voter: Address, uid: int, answer: int) -> None:
        OpenedReferendums._check_opened(db, uid)

        Referendum.vote(db, voter, uid, answer)

    @staticmethod
    def serialize(db: IconScoreDatabase) -> list:
        return list(map(lambda uid: {
            'uid': uid,
            'referendum': Referendum.serialize(db, uid)
        }, OpenedReferendums._opened_referendums(db)))
