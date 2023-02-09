import test

api ="v2_3yqBD_sf93zAjrAsCdTbmwaEa8Dcj"
dataBaseName="irlmpbfhvf2009/telegram-bot"


class Test2():
    def __init__(self):
        sql = test.DBHP(api,dataBaseName)
        sql.create_table("config",['key', 'value'])
        sql.create_table("invitationLimit",['groupId','groupTitle','inviteId','inviteAccount','beInvited','invitationStartDate','invitationEndDate','invitationDate'])
        sql.close()

Test2()