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


class BallotFactory(object):
    # ================================================
    #  DB Variables
    # ================================================
    _UID = 'BALLOT_FACTORY_UID'

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def _uid(db: IconScoreDatabase) -> VarDB:
        return VarDB(f'{BallotFactory._UID}', db, value_type=int)

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def get_uid(db: IconScoreDatabase) -> int:
        uid = BallotFactory._uid(db)
        uid.set(uid.get() + 1)
        return uid.get()


class Ballot(object):
    # ================================================
    #  DB Variables
    # ================================================
    _ADDRESS = 'BALLOT_ADDRESS'
    _REFERENDUM = 'BALLOT_REFERENDUM'
    _ANSWER = 'BALLOT_VOTE'
    _VOTE = 'BALLOT_VOTE'

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def _address(db: IconScoreDatabase, uid: int) -> VarDB:
        return VarDB(f'{Ballot._ADDRESS}_{uid}', db, value_type=Address)

    @staticmethod
    def _referendum(db: IconScoreDatabase, uid: int) -> VarDB:
        return VarDB(f'{Ballot._REFERENDUM}_{uid}', db, value_type=int)

    @staticmethod
    def _answer(db: IconScoreDatabase, uid: int) -> VarDB:
        return VarDB(f'{Ballot._ANSWER}_{uid}', db, value_type=int)

    @staticmethod
    def _vote(db: IconScoreDatabase, uid: int) -> VarDB:
        return VarDB(f'{Ballot._VOTE}_{uid}', db, value_type=int)

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def delete(db: IconScoreDatabase, uid: int) -> None:
        Ballot._weight(db, uid).remove()

    @staticmethod
    def insert(db: IconScoreDatabase, address: Address, referendum: int, answer: int, vote: int) -> int:
        uid = BallotFactory.get_uid(db)
        Ballot._address(db, uid).set(address)
        Ballot._referendum(db, uid).set(referendum)
        Ballot._answer(db, uid).set(answer)
        Ballot._vote(db, uid).set(vote)
        return uid

    @staticmethod
    def serialize(db: IconScoreDatabase, address: Address, uid: int, answer: int) -> dict:
        return {
            'vote': Ballot._vote(db, address, uid, answer).get()
        }
