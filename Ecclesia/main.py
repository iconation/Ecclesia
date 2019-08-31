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
from .checks import *
from .referendum_composite import *
from .version import *

TAG = 'Ecclesia'
ECCLESIA_VERSION = '0.0.1'


class Ecclesia(IconScoreBase):
    """ Ecclesia SCORE Base implementation """

    # ================================================
    #  Event Logs
    # ================================================
    @eventlog(indexed=1)
    def ReferendumCreatedEvent(self, uid: int) -> None:
        pass

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

    def on_install(self) -> None:
        super().on_install()
        Version.set(self.db, ECCLESIA_VERSION)

    def on_update(self) -> None:
        super().on_update()
        Version.set(self.db, ECCLESIA_VERSION)

    # ================================================
    #  External methods
    # ================================================
    @only_owner
    @external
    @catch_error
    def create_referendum(self,
                          end: int,
                          quorum: int,
                          question: str,
                          answers: str,
                          voters: str) -> None:
        # Create a newly opened referendum
        uid = ReferendumComposite.create(
            self.db,
            end,
            quorum,
            question,
            json_loads(answers),
            json_loads(voters))
        self.ReferendumCreatedEvent(uid)

    @external
    @catch_error
    def vote(self,
             referendum_id: int,
             answer: int,
             weight: int) -> None:
        referendum = Referendum(self.db, referendum_id)
        voter = Voter(self.db, referendum_id, self.msg.sender)
        referendum.vote(self.db, voter, answer, weight, self.now())

    @only_owner
    @external
    @catch_error
    def clear_referendums(self) -> None:
        ReferendumComposite.delete(self.db)

    @external(readonly=True)
    @catch_error
    def referendums(self) -> list:
        """ Return a list of all referendums """
        return ReferendumComposite.serialize(self.db)
