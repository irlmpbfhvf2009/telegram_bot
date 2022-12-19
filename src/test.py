import _sql
import json

sql=_sql.DBHP("telegram-bot.db")

inviteId="a"
inviteAccount ="b"
beInvitedId = "e"
beInvitedAccoun ="f"

JSON_data = json.dumps({beInvitedId:beInvitedAccoun})
print(JSON_data)
data=[
    {"inviteId":inviteId,"inviteAccount":inviteAccount,"beInvited":JSON_data}
]
sql.insert_data("invitationLimit",data)