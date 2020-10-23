"""
Module to access DFP reports
"""
import time
import base64
import tempfile
import binascii
import json
from django.conf import settings
from googleads import (ad_manager as dfp, oauth2)
from oauth2client.client import (AccessTokenRefreshError)
from googleads.oauth2 import (GoogleServiceAccountClient, )


class Client():
    """
    DFP Client
    """

    def _create_tmp_file(cls, content, suffix=None, mode='w+b', return_path=False):
        """
        Given report text, create a tmp file and return it
        """
        content_file = tempfile.NamedTemporaryFile(
            suffix=suffix, delete=False, mode=mode)
        content_file.write(content)
        content_file.flush()
        return content_file.name if return_path else content_file

    def __init__(self, dfp_version='v202002', code=None):
        # login
        content_file = tempfile.NamedTemporaryFile(
            suffix='.json', delete=False, mode='w')
        json.dump(settings.DFP,content_file)
        content_file.flush()

        oauth2_client = GoogleServiceAccountClient(content_file.name, oauth2.GetAPIScope('ad_manager'))
        code = code or '108073772'
        self.dfp_client = dfp.AdManagerClient(oauth2_client,
                                        settings.DFP['name'],
                                        code)
        v = dfp_version
        self.inventory_service = self.dfp_client.GetService(
            'InventoryService', version=v)
        self.li_service = self.dfp_client.GetService(
            'LineItemService', version=v)
        self.placement_service = self.dfp_client.GetService(
            'PlacementService', version=v)
        self.creative_service = self.dfp_client.GetService(
            'CreativeService', version=v)

    def __get_default_adunit_sizes(self,):
        return [
            {
                'size': {
                    'width': '300',
                    'height': '250'
                },
                'environmentType': 'BROWSER'
            }, {
                'size': {
                    'width': '160',
                    'height': '600'
                },
                'environmentType': 'BROWSER'
            }, {
                'size': {
                    'width': '300',
                    'height': '600'
                },
                'environmentType': 'BROWSER'
            }, {
                'size': {
                    'width': '728',
                    'height': '90'
                },
                'environmentType': 'BROWSER'
            }, {
                'size': {
                    'width': '320',
                    'height': '100'
                },
                'environmentType': 'BROWSER'
            }, {
                'size': {
                    'width': '320',
                    'height': '50'
                },
                'environmentType': 'BROWSER'
            }, {
                'size': {
                    'width': '1',
                    'height': '1'
                },
                'environmentType': 'VIDEO_PLAYER'
            }, {
                'size': {
                    'width': '400',
                    'height': '300'
                },
                'environmentType': 'VIDEO_PLAYER'
            }, {
                'size': {
                    'width': '640',
                    'height': '480'
                },
                'environmentType': 'VIDEO_PLAYER'
            }
        ]
    # def get_all_ad_unit(self, name='TBN.beinggenevieve'):
    #     return self.__filter_item(
    #         self.inventory_service.getAdUnitsByStatement,
    #         'WHERE name LIKE :name',
    #         [{
    #             'key': 'name',
    #             'value': {
    #                 'xsi_type': 'TextValue',
    #                 'value': name
    #             },
    #         }]
    #     )

    def __create_item(self, create_fn, data):
        try:
            return True, create_fn(data)
        except WebFault as ex:
            # print(ex)
            return False, None

    def __filter_item(self, filter_fn, filter_query, filter_values):
        statement = dfp.FilterStatement(filter_query, filter_values)
        # print(statement.ToStatement())
        response = filter_fn(statement.ToStatement())
        if response.totalResultSetSize > 0:
            return response.results
        else:
            return None

    def __create_if_missing_item(self, filter_fn, filter_query, filter_values, create_fn, create_data):
        result = self.__filter_item(filter_fn, filter_query, filter_values)
        if result:
            return result[0]
        success, item = self.__create_item(create_fn, create_data)
        if success:
            return item[0]

    def get_or_create_adunit(self, name='TBN.beinggenevieve', parent=None):
        return self.__create_if_missing_item(
            self.inventory_service.getAdUnitsByStatement,
            "WHERE name = :name ORDER BY status",  # AND status = 'active'",
            [{
                'key': 'name',
                'value': {
                    'xsi_type': 'TextValue',
                    'value': name
                },
            }],
            self.inventory_service.createAdUnits,
            [{
                'name': name,
                'adUnitCode': name,
                'parentId': parent,
                'adSenseSettings': {'adSenseEnabled': False},
                'adUnitSizes': self.__get_default_adunit_sizes()
            }]
        )

    def archive_li(self, filter_query, ):
        statement = dfp.FilterStatement(filter_query, )
        return self.li_service.performLineItemAction({'xsi_type': 'ArchiveLineItems'}, statement.ToStatement())

    def get_lineitems(self, name, filter_archived=False):
        condition = "WHERE name LIKE :name and isArchived = False" if filter_archived else "WHERE name LIKE :name"
        return self.__filter_item(
            self.li_service.getLineItemsByStatement,
            condition,
            [{
                'key': 'name',
                'value': {
                    'xsi_type': 'TextValue',
                    'value': name
                },
            }],
        )

    def update_lineitem(self, data):
        try:
            self.li_service.updateLineItems(data)
        except WebFault as e:
            pass
    # def update_ad_unit(self, data):
    #     self.inventory_service.updateAdUnits(data)


