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
from .opened_referendums import *
from .version import *

TAG = 'Ecclesia'
ECCLESIA_VERSION = '0.0.1'


class Ecclesia(IconScoreBase):
    """ Ecclesia SCORE Base implementation """

    # ================================================
    #  DB Variables
    # ================================================
    # Referendum Unique ID
    _REFERENDUM_LAST_UID = 'REFERENDUM_LAST_UID'

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._referendum_last_uid = VarDB(self._REFERENDUM_LAST_UID, db, value_type=int)

    def on_install(self) -> None:
        super().on_install()
        self._referendum_last_uid.set(0)
        Version.set(self.db, ECCLESIA_VERSION)

    def on_update(self) -> None:
        super().on_update()
        Logger.warning(dir(self))
        Version.set(self.db, ECCLESIA_VERSION)

    # ================================================
    #  External methods
    # ================================================
    @only_owner
    @external
    def create_referendum(self,
                          end: int,
                          quorum: int,
                          question: str,
                          answers: str) -> None:
        try:
            # Create a new opened referendum
            uid = self._referendum_last_uid.get()
            OpenedReferendums.insert(self.db, uid, end, quorum, question, json_loads(answers))

            # Update the UID
            self._referendum_last_uid.set(uid + 1)
        except Exception as e:
            Logger.error(repr(e), TAG)
            revert(repr(e))

    @external
    def vote(self, uid: int, answer: int) -> None:
        try:
            OpenedReferendums.vote(self.db, self.msg.sender, uid, answer)
        except Exception as e:
            Logger.error(repr(e), TAG)
            revert(repr(e))

    @only_owner
    @external
    def clear_referendums(self) -> None:
        try:
            OpenedReferendums.delete(self.db)
            self._referendum_last_uid.set(0)
        except Exception as e:
            Logger.error(repr(e), TAG)
            revert(repr(e))

    # ==== ReadOnly methods =============================================
    @external(readonly=True)
    def uid(self) -> int:
        """ Return the current UID generator """
        return self._referendum_last_uid.get()

    @external(readonly=True)
    def opened_referendums(self) -> list:
        """ Return a list of opened referendums """
        return OpenedReferendums.serialize(self.db)

    # ================================================
    #  Private methods
    # ================================================
