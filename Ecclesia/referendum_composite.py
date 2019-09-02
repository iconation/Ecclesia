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
from .voter import *

TAG = 'Ecclesia'


class ReferendumComposite(object):

    # ================================================
    #  DB Variables
    # ================================================
    # Referendums are indexed by their UID
    _INDEX = 'REFERENDUM_COMPOSITE_INDEX'

    # ================================================
    #  Private Methods
    # ================================================
    @staticmethod
    def _referendums(db: IconScoreDatabase) -> ArrayDB:
        return ArrayDB(ReferendumComposite._INDEX, db, value_type=int)

    # ================================================
    #  Public Methods
    # ================================================
    @staticmethod
    def create(db: IconScoreDatabase,
               end: int,
               quorum: int,
               question: str,
               answers: list,
               voters: list) -> int:
        # Create referendum object
        uid = ReferendumFactory.create(db, end, quorum, question, answers)
        ReferendumComposite._referendums(db).put(uid)

        # Initialize the voters for that referendum
        for voter in voters:
            address = Address.from_string(voter['address'])
            weight = voter['weight']
            VoterFactory.create(db, uid, address, weight)

        return uid

    @staticmethod
    def serialize(db: IconScoreDatabase) -> list:
        return list(map(lambda uid: {
            'uid': uid,
            'referendum': Referendum(db, uid).serialize()
        }, ReferendumComposite._referendums(db)))

    @staticmethod
    def delete(db: IconScoreDatabase) -> None:
        referendums = ReferendumComposite._referendums(db)
        while referendums:
            uid = referendums.pop()
            Referendum(db, uid).delete()
