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


class VoterNotEnoughWeightError(Exception):
    pass


class VoterWeightValueError(Exception):
    pass


class VoterFactory(object):
    @staticmethod
    def create(db: IconScoreDatabase,
               referendum: int,
               address: Address,
               weight: int) -> None:

        voter = Voter(db, referendum, address)
        # Logger.warning(f'Voter {address} has weight {weight}')
        voter._weight.set(weight)


class Voter(object):
    # ================================================
    #  DB Variables
    # ================================================
    _WEIGHT = 'VOTER_WEIGHT'
    _BALLOTS = 'VOTER_BALLOTS'

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase, referendum: int, address: Address) -> None:
        self._referendum = referendum
        self._address = address
        self._weight = VarDB(f'{Voter._WEIGHT}_{referendum}_{address}', db, value_type=int)
        self._ballots = ArrayDB(f'{Voter._BALLOTS}_{referendum}_{address}', db, value_type=int)

    # ================================================
    #  Checks
    # ================================================
    def _check_weight(self, target_weight: int) -> None:
        if target_weight <= 0:
            raise VoterWeightValueError(f'{self._address} : {target_weight} <= 0')
        if target_weight > self._weight.get():
            raise VoterNotEnoughWeightError(f'{self._address} : {target_weight} > {self._weight.get()}')

    # ================================================
    #  Public Methods
    # ================================================
    def vote(self,
             db: IconScoreDatabase,
             answer: int,
             weight: int) -> int:
        self._check_weight(weight)

        # Set the voting weight to the ballot
        ballot = BallotFactory.create(db, self._referendum, self._address, answer, weight)
        self._ballots.put(ballot)

        # Update the voting weight of the voter
        self._weight.set(self._weight.get() - weight)

        return ballot

    def serialize(self) -> dict:
        return {
            'weight': self._weight.get(),
            'ballots': list(map(lambda ballot: ballot, self._ballots))
        }

    def delete(self) -> None:
        self._weight.remove()
        Utils.array_db_clear(self._ballots)
