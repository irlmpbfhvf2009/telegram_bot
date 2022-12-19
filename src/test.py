import _sql
import json

sql=_sql.DBHP("telegram-bot.db")

inviteId="a"
inviteAccount ="b"
beInvitedId = "e"
beInvitedAccoun ="f"

JSON_data = json.dumps({beInvitedId:beInvitedAccoun})

data=[
    {"inviteId":inviteId,"inviteAccount":inviteAccount,"beInvited":JSON_data}
]
#sql.insert_data("invitationLimit",data)
print(sql.existInviteId(inviteId))
print(sql.existInviteId(inviteId))



sql.updateBeInvited("5036779522",data)