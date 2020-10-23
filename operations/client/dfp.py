"""
Module to access DFP reports
"""
import time
import base64
import tempfile
import binascii
import json
from suds import WebFault
from django.conf import settings
from googleads import (ad_manager as dfp, oauth2)
from oauth2client.client import (AccessTokenRefreshError)
from googleads.oauth2 import (GoogleServiceAccountClient, )
from account.models import DisplayAd, Account, AccountProduct, Activity


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


def deactivate_accounts(sf_accounts=None, code=20842576):
    dfp = Client(code=code)
    accounts = Account.objects.filter(
        ac_number__in=sf_accounts, status='active').update(status='inactive', account_status='f')


def get_or_create_adunit(self, name='TBN.beinggenevieve', parent=None):
    return self.__create_if_missing_item(
        self.inventory_service.getAdUnitsByStatement,
        'WHERE name = :name',
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


def archieve_line_item(sf_accounts=None, code=20842576):
    dfp = Client(code=code)
    accounts = list(
        Account.objects.filter(
            ac_number__in=sf_accounts,
            status='active').values_list('ac_number', flat=True)
    )
    account_to_update = []
    for account in accounts:
        if archieve_lineitem_for_account(
                account, dfp):
            account_to_update.append(account)
    Account.objects.filter(ac_number__in=account_to_update).update(
        status='inactive', account_status='f')


def archieve_lineitem_for_account(account, dfp):
    line_items_for_account = dfp.get_lineitems(account + '%', True)
    if not line_items_for_account:
        print("LineItems not fount for account %s" % account)
        return True
    li_to_archive = []
    for li in line_items_for_account:
        if not li.isArchived and str(account) == li.name.split('_')[0]:
            li_to_archive.append(str(li.id))
    filter_query = 'WHERE id in %s' % (tuple(li_to_archive),) if len(
        li_to_archive) > 1 else 'WHERE id = %s' % li_to_archive[0]
    result = dfp.archive_li(
        filter_query
    )
    return True if result else False


def get_or_create_adunit(self, name='TBN.beinggenevieve', parent=None):
    return self.__create_if_missing_item(
        self.inventory_service.getAdUnitsByStatement,
        'WHERE name = :name',
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


def search_and_update_lineitem_for_account(account, dfp, new_ipin_from_dfp):
    # account = 'test_ad_ex'
    line_items_for_account = dfp.get_lineitems(account + '%')
    if not line_items_for_account:
        print("LineItems not found for account %s" % account)
        return
    updated_li = []
    for li in line_items_for_account:
        if li.isArchived:
            continue
        for nip in new_ipin_from_dfp:
            li['targeting']['inventoryTargeting']['targetedAdUnits'].append({
                'xsi_type': 'AdUnitTargeting',
                'adUnitId': nip.id,
                'includeDescendants': True
            })
        updated_li.append(li)
    dfp.update_lineitem(updated_li)

# def update_ad_unit(account, dfp):
#     ad_unit = Account.objects.filter(ac_number=account).values('ad_unit', 'pin')
#     if not ad_unit:
#         return

#     pin = ad_unit[0].get('pin')
#     ad_unit = ad_unit[0].get('ad_unit')

#     parent_ad_unit = dfp.get_or_create_adunit(name=ad_unit)
#     #print(parent_ad_unit)
#     #print(parent_ad_unit)
#     i_pins = dfp.get_all_ad_unit(pin+'%')
#     for ipin in i_pins:
#         if ipin.status == "ARCHIVED":
#             continue

#         ipin['parentId'] = parent_ad_unit.id
#         ipin['parentPath'].append({
#             'xsi_type': 'AdUnitParent',
#             'name': parent_ad_unit.name,
#             'id': str(parent_ad_unit.id),
#             'adUnitCode': parent_ad_unit.adUnitCode
#         })
#         print(ipin['parentPath'])
#         dfp.update_ad_unit([ipin])
#         return


def create_ipin_in_dfp_for_account(account, pin, dfp, parent):
    ipins = DisplayAd.objects.filter(account_id__ac_number=account, deleted=0).values(
        'ipin_mobile', 'ipin_tablet', 'ipin_desktop')
    parent_ad_unit = dfp.get_or_create_adunit(name=pin, parent=parent)
    parent = parent_ad_unit.id  # '19842696'  # '107073892'  # TO-DO
    dfp_ipins = []
    devices = ['desktop', 'mobile', 'tablet']
    for ipin in ipins:
        display_ad = DisplayAd.objects.filter(ipin_desktop=ipin.get('ipin_desktop'),
                                              ipin_tablet=ipin.get(
                                                  'ipin_tablet'),
                                              ipin_mobile=ipin.get('ipin_mobile'))
        for device in devices:
            time.sleep(0.5)
            ipin_to_create = ipin.get('ipin_%s' % device, None).get('ipin')
            if ipin_to_create:
                pin = dfp.get_or_create_adunit(ipin_to_create, parent)

                if display_ad:
                    if display_ad[0].sticky and device in display_ad[0].stick_for:
                        add_ipin_to_sticky_placement(
                            pin, display_ad[0].sticky, dfp)

                if pin:
                    dfp_ipins.append(pin)
                    if ipin.get('ipin_%s' % device, None).get('edit') == 'False':
                        continue
                    ipin['ipin_%s' % device]['edit'] = False
                data = {'ipin_%s' % device: ipin['ipin_%s' % device]}
                if device == 'mobile':
                    DisplayAd.objects.filter(account_id__ac_number=account, deleted=0,
                                             ipin_mobile__icontains=ipin_to_create).update(**data)
                elif device == 'desktop':
                    DisplayAd.objects.filter(account_id__ac_number=account, deleted=0,
                                             ipin_desktop__icontains=ipin_to_create).update(**data)
                elif device == 'tablet':
                    DisplayAd.objects.filter(account_id__ac_number=account, deleted=0,
                                             ipin_tablet__icontains=ipin_to_create).update(**data)
    return [parent_ad_unit]


def add_ipin_to_sticky_placement(ipin, sticky, client):
    sticky_placements = get_placement_by_sticky_type(sticky, client)

    if sticky_placements:
        valid_placements = [placement.name for placement in sticky_placements
                            if ipin.id not in placement.targetedAdUnitIds]
        sticky_placement_names = [
            placement.name for placement in sticky_placements]
        if valid_placements == sticky_placement_names:
            for placement in sticky_placements:
                current_ad_units = placement.targetedAdUnitIds
                if len(current_ad_units) < 1000:
                    placement.targetedAdUnitIds.append(ipin.id)
                    client.placement_service.updatePlacements([placement])
                    break


def get_placement_by_sticky_type(sticky, client):
    if sticky == 'bottom':
        statement = dfp.FilterStatement("WHERE name LIKE '%Sticky Bottom%'")
    elif sticky == 'header':
        statement = dfp.FilterStatement("WHERE name LIKE '%Sticky Header%'")
    elif sticky == 'sidebar':
        statement = dfp.FilterStatement("WHERE name LIKE '%Sticky Sidebar%'")
    elif sticky == 'pillar':
        statement = dfp.FilterStatement("WHERE name LIKE '%Sticky Pillar%'")
    elif sticky == 'flight':
        statement = dfp.FilterStatement("WHERE name LIKE '%Sticky Flight%'")
    else:
        return None

    placement_results = client.placement_service.getPlacementsByStatement(
        statement.ToStatement())
    return placement_results.results


def flight_ipin(account, pin, dfp, flight_config, parent):
    parent_ad_unit = dfp.get_or_create_adunit(name=pin, parent=parent)
    parent = parent_ad_unit.id  # '19842696'  # '107073892'  # TO-DO
    devices = ['M', 'D', 'T']
    ipin = []
    stick_devices = json.loads(flight_config.get('stick_for', '[]'))
    sticky_declarations = [d[0].upper() for d in stick_devices]
    for index in range(10):
        for device in devices:
            i_pin = "%s-D%sL.%s" % (pin, device, chr(ord('A') + index))
            new_ipin = dfp.get_or_create_adunit(i_pin, parent)
            ipin.append(new_ipin)
            if device in sticky_declarations:
                add_ipin_to_sticky_placement(new_ipin, 'flight', dfp)
    return [parent_ad_unit]


def repeatable_ipin(account, pin, dfp, parent):
    """Generates ipins for repeatable tags for the given account in the given dfp

    Arguments:
        account {str} -- ac_number
        pin {str} -- pin
        dfp {Client} -- dfp Client

    Returns:
        list -- list of the parent ad unit
    """
    ipins = DisplayAd.objects.filter(account_id__ac_number=account,
                                     deleted=0,
                                     is_repeatable=True)\
        .values('ipin_mobile', 'ipin_tablet', 'ipin_desktop')
    parent_ad_unit = dfp.get_or_create_adunit(name=pin, parent=parent)
    parent = parent_ad_unit.id  # '19842696'  # '107073892'  # TO-DO
    devices = ['desktop', 'mobile', 'tablet']
    ipin_list = []
    for ipin in ipins:
        for device in devices:
            i_pin = ipin.get('ipin_%s' % device, None).get('ipin')
            if not i_pin:
                continue
            dot_index = i_pin.find('.')
            repeatable_ipin = '%sI%s' % (
                i_pin[:dot_index-1], i_pin[dot_index:])
            ipin_list.append(dfp.get_or_create_adunit(repeatable_ipin, parent))
    return [parent_ad_unit]


def run(accounts=None, code=None):
    accounts = list(
        Account.objects.filter(
            ac_number__in=accounts,
            status='active').values('ac_number', 'pin', 'dfp_account')
    )
    for account in accounts:
        account_dfp_network = code if code else str(account.get('dfp_account'))
        dfp = Client(code=account_dfp_network)
        parent = settings.DFP_PARENT_AD_UNITS.get(account_dfp_network)
        if not parent:
            print("Please provide parent ad unit for given network %s" % account_dfp_network)
            continue
        if not account.get('pin'):
            continue
        print("createing/getting Ad Unit(I-PIN) for account: %s, on network %s" %
              (account, account_dfp_network))
        new_ipin_from_dfp = create_ipin_in_dfp_for_account(
            account.get('ac_number'), account.get('pin'), dfp, parent)
        flight_status = AccountProduct.objects.filter(
            account_id__ac_number=account.get('ac_number'), product='flight', status='active').values('status', 'configuration')
        if flight_status and flight_status[0].get('status') == 'active':
            print("creating flight ad units")
            new_ipin_from_dfp += flight_ipin(
                account.get('ac_number'), account.get('pin'), dfp, flight_status[0]['configuration'], parent)
        # if DisplayAd.objects.filter(account_id__ac_number=account.get('ac_number'), is_repeatable=True).count():
        #     print("creating repeatable ad units")
        #     new_ipin_from_dfp += repeatable_ipin(
        #         account.get('ac_number'), account.get('pin'), dfp, parent)
        if not new_ipin_from_dfp:
            print("New I-PIN not created for account %s", account)
            return
        print("Updateting Ad Unit(I-PIN) for account: %s" % account)
        search_and_update_lineitem_for_account(
            account.get('ac_number'), dfp, new_ipin_from_dfp)


def get_ad_unit_ids(i_pins, client):
    """
    Calls a function to get a list of ipins, gets the corresponding ad unit ID from GAM using
    the GAM API.
    Returns a list of ad unit IDs
    """
    ipins = tuple(i_pins)
    print('REMOVE FROM GAM STICKY: getting ad unit IDs')
    statement = dfp.StatementBuilder(
        version='v202002').Where(f"status = 'ACTIVE' and name IN {ipins}")
    au_ids = []
    while True:
        response = client.inventory_service.getAdUnitsByStatement(statement.ToStatement())
        if 'results' in response and len(response['results']):
            for ad_unit in response['results']:
                if ad_unit['adUnitCode'] in ipins:
                    au_ids.append(ad_unit['id'])
            statement.offset += statement.limit
        else:
            break
    return au_ids


def remove_auid_from_placement(ipins, gam_account='20842576'):
    """
    Get ad unit IDs and remove them from GAM sticky placements
    """
    print('REMOVE FROM GAM STICKY: Removing ad unit IDs from sticky placements')
    client = Client(code=gam_account)
    au_ids = get_ad_unit_ids(i_pins=ipins, client=client)
    statement = dfp.FilterStatement("WHERE name LIKE 'Sticky%'")
    while True:
        response = client.placement_service.getPlacementsByStatement(
            statement.ToStatement())
        if 'results' in response and len(response['results']):
            for placement in response['results']:
                if placement['targetedAdUnitIds']:
                    for auid in au_ids:
                        if auid in placement['targetedAdUnitIds']:
                            placement['targetedAdUnitIds'].remove(auid)
                            print(f'removing {auid} from {placement["name"]}')
                            client.placement_service.updatePlacements([placement])
            statement.offset += statement.limit
        else:
            break
    print('Removing ad units from sticky placements complete')


def toggle_df_safeframes(active=True, code='21664718071'):
    client = Client(code=code)
    statement = (dfp.StatementBuilder(version='v202008').Where("name like 'Demand_Fusion%'"))
    statement.limit = 1000
    
    res = client.creative_service.getCreativesByStatement(statement.ToStatement())
    while res['results']:
        print(f"Requesting {statement.offset} -> {statement.offset + statement.limit}.")
        creative_list = res['results']
        for creative in creative_list:
            creative['isSafeFrameCompatible'] = active
        client.creative_service.updateCreatives(creative_list)
        statement.offset += statement.limit
        res = client.creative_service.getCreativesByStatement(statement.ToStatement())

    print("All creatives updated.")
