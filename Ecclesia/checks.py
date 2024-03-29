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


TAG = 'Ecclesia'


# ================================================
#  Exceptions
# ================================================
class SenderNotScoreOwnerError(Exception):
    pass


class SenderNotWalletOwnerError(Exception):
    pass


class NotAFunctionError(Exception):
    pass


def only_wallet(func):
    if not isfunction(func):
        raise NotAFunctionError

    @wraps(func)
    def __wrapper(self: object, *args, **kwargs):
        if self.msg.sender != self.address:
            raise SenderNotWalletOwnerError

        return func(self, *args, **kwargs)
    return __wrapper


def only_owner(func):
    if not isfunction(func):
        raise NotAFunctionError

    @wraps(func)
    def __wrapper(self: object, *args, **kwargs):
        if self.msg.sender != self.owner:
            raise SenderNotScoreOwnerError

        return func(self, *args, **kwargs)
    return __wrapper


def catch_error(func):
    if not isfunction(func):
        raise NotAFunctionError

    @wraps(func)
    def __wrapper(self: object, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            Logger.error(repr(e), TAG)
            revert(repr(e))

    return __wrapper
