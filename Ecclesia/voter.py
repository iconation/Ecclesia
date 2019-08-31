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
from .ballot import *

TAG = 'Ecclesia'


class VoterNotEnoughWeight(Exception):
    pass


class Voter(object):
    # ================================================
    #  DB Variables
    # ================================================
    _WEIGHT = 'VOTER_WEIGHT'

    # ================================================
    #  Checks
    # ================================================
    def _check_enough_weight(db: IconScoreDatabase, address: Address, uid: int, target_weight: int) -> None:
        current_weight = Voter.weight(db, address, uid)
        if target_weight > current_weight:
            raise VoterNotEnoughWeight

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def _weight(db: IconScoreDatabase, address: Address, uid: int) -> VarDB:
        return VarDB(f'{Voter._WEIGHT}_{address}_{uid}', db, value_type=int)

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def insert(db: IconScoreDatabase, address: Address, uid: int, weight: int) -> None:
        Voter._weight(db, address, uid).set(weight)

    @staticmethod
    def delete(db: IconScoreDatabase, address: Address, uid: int) -> None:
        Voter._weight(db, address, uid).remove()

    @staticmethod
    def vote(db: IconScoreDatabase, address: Address, uid: int, answer: int, weight: int) -> None:
        Voter._check_enough_weight(weight)

        # Set the voting weight to the ballot
        Ballot.insert(db, address, uid, answer, weight)

        # Update the voting weight of the voter
        current_weight = Voter._weight(db, address, uid)
        current_weight.set(current_weight.get() - weight)

    @staticmethod
    def serialize(db: IconScoreDatabase, address: Address, uid: int) -> dict:
        return {
            'weight': Voter._weight(db, address, uid).get()
        }
