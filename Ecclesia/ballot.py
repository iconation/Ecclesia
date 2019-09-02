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

    @staticmethod
    def create(db: IconScoreDatabase, referendum: int, address: Address, answer: int, vote: int) -> int:
        uid = BallotFactory.get_uid(db)
        ballot = Ballot(db, uid)
        ballot._address.set(address)
        ballot._referendum.set(referendum)
        ballot._answer.set(answer)
        ballot._vote.set(vote)
        return uid


class Ballot(object):
    # ================================================
    #  DB Variables
    # ================================================
    _ADDRESS = 'BALLOT_ADDRESS'
    _REFERENDUM = 'BALLOT_REFERENDUM'
    _ANSWER = 'BALLOT_ANSWER'
    _VOTE = 'BALLOT_VOTE'

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase, uid: int) -> None:
        self._address = VarDB(f'{Ballot._ADDRESS}_{uid}', db, value_type=Address)
        self._referendum = VarDB(f'{Ballot._REFERENDUM}_{uid}', db, value_type=int)
        self._answer = VarDB(f'{Ballot._ANSWER}_{uid}', db, value_type=int)
        self._vote = VarDB(f'{Ballot._VOTE}_{uid}', db, value_type=int)

    # ================================================
    #  Public Methods
    # ================================================
    def serialize(self) -> dict:
        return {
            'address': self._address.get(),
            'referendum': self._referendum.get(),
            'answer': self._answer.get(),
            'vote': self._vote.get()
        }

    def delete(self) -> None:
        self._address.remove()
        self._referendum.remove()
        self._answer.remove()
        self._weight.remove()
