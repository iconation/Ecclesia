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
from .voter import *

TAG = 'Ecclesia'


class ReferendumTooManyAnswersError(Exception):
    pass


class ReferendumClosedError(Exception):
    pass


class ReferendumFactory(object):
    # ================================================
    #  Constants
    # ================================================
    # Maximum limit of answers
    MAXIMUM_ANSWERS_COUNT = 100

    # ================================================
    #  DB Variables
    # ================================================
    _UID = 'REFERENDUM_FACTORY_UID'

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def _uid(db: IconScoreDatabase) -> VarDB:
        return VarDB(f'{ReferendumFactory._UID}', db, value_type=int)

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def get_uid(db: IconScoreDatabase) -> int:
        uid = ReferendumFactory._uid(db)
        uid.set(uid.get() + 1)
        return uid.get()

    # ================================================
    #  Checks
    # ================================================
    @staticmethod
    def _check_answers_count(answers: list) -> None:
        if len(answers) > ReferendumFactory.MAXIMUM_ANSWERS_COUNT:
            raise ReferendumTooManyAnswersError

    @staticmethod
    def create(db: IconScoreDatabase,
               end: int,
               quorum: int,
               question: str,
               answers: list) -> int:

        ReferendumFactory._check_answers_count(answers)

        uid = ReferendumFactory.get_uid(db)
        referendum = Referendum(db, uid)

        referendum._end.set(end)
        referendum._quorum.set(quorum)
        referendum._question.set(question)
        for answer in answers:
            referendum._answers.put(answer)
            referendum._votes.put(0)

        return uid


class Referendum(object):
    # ================================================
    #  DB Variables
    # ================================================
    _QUESTION = 'REFERENDUM_QUESTION'
    _ANSWERS = 'REFERENDUM_ANSWERS'
    _VOTES = 'REFERENDUM_VOTES'
    _END = 'REFERENDUM_END'
    _QUORUM = 'REFERENDUM_QUORUM'
    _BALLOTS = 'REFERENDUM_BALLOTS'

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase, uid: int) -> None:
        self._question = VarDB(f'{Referendum._QUESTION}_{uid}', db, value_type=str)
        self._answers = ArrayDB(f'{Referendum._ANSWERS}_{uid}', db, value_type=str)
        self._votes = ArrayDB(f'{Referendum._VOTES}_{uid}', db, value_type=int)
        self._end = VarDB(f'{Referendum._END}_{uid}', db, value_type=int)
        self._quorum = VarDB(f'{Referendum._QUORUM}_{uid}', db, value_type=int)
        self._ballots = ArrayDB(f'{Referendum._BALLOTS}_{uid}', db, value_type=int)

    # ================================================
    #  Private Methods
    # ================================================
    def _is_opened(self, now: int) -> bool:
        return self._end.get() > now

    # ================================================
    #  Checks
    # ================================================
    def _check_is_opened(self, now: int) -> ArrayDB:
        if not self._is_opened(now):
            raise ReferendumClosedError(f'now: {now}, end: {self._end.get()}')

    # ================================================
    #  Public Methods
    # ================================================
    def vote(self,
             db: IconScoreDatabase,
             voter: Voter,
             answer: int,
             weight: int,
             now: int) -> None:
        self._check_is_opened(now)

        # The voter creates a ballot when voting
        ballot = voter.vote(db, answer, weight)
        self._ballots.put(ballot)

        # Update the referendum results
        self._votes[answer] += weight

    def serialize(self) -> dict:
        return {
            'end': self._end.get(),
            'quorum': self._quorum.get(),
            'question': self._question.get(),
            'answers': list(map(lambda answer: str(answer), self._answers)),
            'votes': list(map(lambda vote: vote, self._votes)),
            'ballots': list(map(lambda ballot: ballot, self._ballots))
        }

    def delete(self) -> None:
        self._end.remove()
        self._quorum.remove()
        self._question.remove()
        Utils.array_db_clear(self._answers)
        Utils.array_db_clear(self._votes)
        Utils.array_db_clear(self._ballots)
