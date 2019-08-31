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

import os
import json

from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction

from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS
from Ecclesia.tests.utils import *

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


class TestEcclesia(IconIntegrateTestBase):
    TEST_HTTP_ENDPOINT_URI_V3 = "http://127.0.0.1:9000/api/v3"
    SCORE_PROJECT = os.path.abspath(os.path.join(DIR_PATH, '..'))

    _PARTICIPATION_COST = 1 * 10**18

    def setUp(self):
        super().setUp()

        self.icon_service = None
        # if you want to send request to network, uncomment next line and set self.TEST_HTTP_ENDPOINT_URI_V3
        # self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))

        # install SCORE
        self._score_address = self._deploy_score()['scoreAddress']
        self._operator = self._test1

        for wallet in self._wallet_array:
            icx_transfer_call(super(), self._test1, wallet.get_address(), 100 * 10**18, self.icon_service)

    def _deploy_score(self, to: str = SCORE_INSTALL_ADDRESS) -> dict:
        # Generates an instance of transaction for deploying SCORE.
        transaction = DeployTransactionBuilder() \
            .from_(self._test1.get_address()) \
            .to(to) \
            .step_limit(100_000_000_000) \
            .nid(3) \
            .nonce(100) \
            .content_type("application/zip") \
            .content(gen_deploy_data_content(self.SCORE_PROJECT)) \
            .build()

        # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._test1)

        # process the transaction in local
        result = self.process_transaction(signed_transaction, self.icon_service)

        self.assertTrue('status' in result)
        self.assertEqual(1, result['status'])
        self.assertTrue('scoreAddress' in result)

        return result

    # ===============================================================
    def create_referendum(self):
        result = transaction_call_success(
            super(),
            from_=self._operator,
            to_=self._score_address,
            method="create_referendum",
            params={
                'end': 2567281501517606,
                'quorum': 100,
                'question': 'Yes or No ?',
                'answers': '["Yes", "No", "Maybe"]',
                'voters': '[ \
                    {"address" : "' + self._wallet_array[0].get_address() + '", "weight": 100},   \
                    {"address" : "' + self._wallet_array[1].get_address() + '", "weight": 100},    \
                    {"address" : "' + self._wallet_array[2].get_address() + '", "weight": 100}    \
                ]'
            },
            icon_service=self.icon_service
        )

        indexed = result['eventLogs'][0]['indexed']
        self.assertEqual(indexed[0], 'ReferendumCreatedEvent(int)')
        return int(indexed[1], 16)

    def get_referendums(self) -> list:
        # OK
        result = icx_call(
            super(),
            from_=self._operator.get_address(),
            to_=self._score_address,
            method="referendums",
            icon_service=self.icon_service,
        )
        return result

    # ===============================================================
    def test_vote_ok(self):
        referendum_id = self.create_referendum()
        # OK
        result = transaction_call_success(
            super(),
            from_=self._wallet_array[0],
            to_=self._score_address,
            method="vote",
            params={
                'referendum_id': referendum_id,
                'answer': 0,
                'weight': 100
            },
            icon_service=self.icon_service
        )

    def test_vote_invalid_answer(self):
        referendum_id = self.create_referendum()
        # OK
        result = transaction_call_error(
            super(),
            from_=self._wallet_array[0],
            to_=self._score_address,
            method="vote",
            params={
                'referendum_id': referendum_id,
                'answer': 10000,
                'weight': 100
            },
            icon_service=self.icon_service
        )
        self.assertTrue('ArrayDB out of index' in result['failure']['message'])

    def test_vote_invalid_weight(self):
        referendum_id = self.create_referendum()
        # OK
        result = transaction_call_error(
            super(),
            from_=self._wallet_array[0],
            to_=self._score_address,
            method="vote",
            params={
                'referendum_id': referendum_id,
                'answer': 0,
                'weight': 100000
            },
            icon_service=self.icon_service
        )
        self.assertTrue('VoterNotEnoughWeightError' in result['failure']['message'])

    def test_vote_invalid_refereum(self):
        referendum_id = self.create_referendum()
        # OK
        result = transaction_call_error(
            super(),
            from_=self._wallet_array[0],
            to_=self._score_address,
            method="vote",
            params={
                'referendum_id': referendum_id,
                'answer': 0,
                'weight': 0
            },
            icon_service=self.icon_service
        )
        self.assertTrue('VoterWeightValueError' in result['failure']['message'])
