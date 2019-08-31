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

TAG = 'Ecclesia'


class ReferendumFactory(object):
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


class Referendum(object):
    # ================================================
    #  DB Variables
    # ================================================
    _QUESTION = 'REFERENDUM_QUESTION'
    _ANSWERS = 'REFERENDUM_ANSWERS'
    _VOTES = 'REFERENDUM_VOTES'
    _END = 'REFERENDUM_END'
    _QUORUM = 'REFERENDUM_QUORUM'

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def _question(db: IconScoreDatabase, uid: int) -> VarDB:
        return VarDB(f'{Referendum._QUESTION}_{uid}', db, value_type=str)

    @staticmethod
    def _answers(db: IconScoreDatabase, uid: int) -> ArrayDB:
        return ArrayDB(f'{Referendum._ANSWERS}_{uid}', db, value_type=str)

    @staticmethod
    def _votes(db: IconScoreDatabase, uid: int) -> ArrayDB:
        return ArrayDB(f'{Referendum._VOTES}_{uid}', db, value_type=int)

    @staticmethod
    def _end(db: IconScoreDatabase, uid: int) -> VarDB:
        return VarDB(f'{Referendum._END}_{uid}', db, value_type=int)

    @staticmethod
    def _quorum(db: IconScoreDatabase, uid: int) -> VarDB:
        return VarDB(f'{Referendum._QUORUM}_{uid}', db, value_type=int)

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def insert(db: IconScoreDatabase,
               end: int,
               quorum: int,
               question: str,
               answers: list) -> int:
        uid = ReferendumFactory.get_uid(db)
        Referendum._end(db, uid).set(end)
        Referendum._quorum(db, uid).set(quorum)
        Referendum._question(db, uid).set(question)
        for answer in answers:
            Referendum._answers(db, uid).put(answer)
            Referendum._votes(db, uid).put(0)
        return uid

    @staticmethod
    def delete(db: IconScoreDatabase, uid: int) -> None:
        Referendum._end(db, uid).remove()
        Referendum._quorum(db, uid).remove()
        Referendum._question(db, uid).remove()
        Utils.array_db_clear(Referendum._answers(db, uid))
        Utils.array_db_clear(Referendum._votes(db, uid))

    @staticmethod
    def vote(db: IconScoreDatabase, voter: Address, uid: int, answer: int) -> None:
        Referendum._votes(db, uid)[answer] += 1

    @staticmethod
    def serialize(db: IconScoreDatabase, uid: int) -> dict:
        return {
            'end': Referendum._end(db, uid).get(),
            'quorum': Referendum._quorum(db, uid).get(),
            'question': Referendum._question(db, uid).get(),
            'answers': list(map(lambda answer: str(answer), Referendum._answers(db, uid))),
            'votes': list(map(lambda vote: vote, Referendum._votes(db, uid)))
        }
