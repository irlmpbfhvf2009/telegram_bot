import _sql
import json

sql=_sql.DBHP("telegram-bot.db")

message_id="5036779522"
print(sql.messageLimitToInviteFriends(message_id))
#print(sql.getInviteFriendsQuantity())