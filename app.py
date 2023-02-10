import os
import sys
from flask import Flask, render_template, jsonify, request
from gevent.pywsgi import WSGIServer
from src.common import utils
from src import _sql
from src import bot
import multiprocessing as mp

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys.executable, '..', 'templates')
    static_folder = os.path.join(sys.executable, '..', 'static')
    app = Flask(__name__, template_folder=template_folder,
                static_folder=static_folder)
else:
    app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template(r'index.html')


@app.route("/getLogList", methods=['get'])
def getLogList():
    return jsonify({'log': utils.Common().log['log_list']})


@app.route("/getConfig", methods=['get'])
def getConfig():
    sql = _sql.DBHP("telegram-bot")
    return jsonify({'botusername': sql.botusername,
                    'password': sql.password,
                    'inviteFriendsAutoClearTime': sql.inviteFriendsAutoClearTime,
                    'inviteFriendsSet': sql.inviteFriendsSet,
                    'followChannelSet': sql.followChannelSet,
                    'inviteFriendsQuantity': sql.inviteFriendsQuantity,
                    'deleteSeconds': sql.deleteSeconds,
                    'invitationBonusSet': sql.invitationBonusSet,
                    'inviteMembers': sql.inviteMembers,
                    'inviteEarnedOutstand': sql.inviteEarnedOutstand,
                    'inviteSettlementBonus': sql.inviteSettlementBonus,
                    'contactPerson': sql.contactPerson})


@app.route("/editInviteFriends", methods=['post'])
def editInviteFriends():
    sql = _sql.DBHP("telegram-bot")
    sql.editInviteFriends(
        "False") if sql.inviteFriendsSet == "True" else sql.editInviteFriends("True")
    string = "關閉[邀請好友限制發言]" if sql.inviteFriendsSet == "True" else "開啟[邀請好友限制發言]"
    code = 0 if sql.inviteFriendsSet == "True" else 1
    return jsonify({'code': code, 'msg': string})


@app.route("/editFollowChannel", methods=['post'])
def editFollowChannel():
    sql = _sql.DBHP("telegram-bot")
    sql.editFollowChannel(
        "False") if sql.followChannelSet == "True" else sql.editFollowChannel("True")
    string = "關閉[關注頻道限制發言]" if sql.followChannelSet == "True" else "開啟[關注頻道限制發言]"
    code = 0 if sql.followChannelSet == "True" else 1
    return jsonify({'code': code, 'msg': string})


@app.route("/editPassword", methods=['post'])
def editPassword():
    sql = _sql.DBHP("telegram-bot")
    try:
        sql.editPassword(request.get_json()['password'])
        return jsonify({'code': 1,'msg':'修改成功'})
    except Exception as e:
        return jsonify({'code': 0,'msg':str(e)})

@app.route("/editContactPerson", methods=['post'])
def editContactPerson():
    sql = _sql.DBHP("telegram-bot")
    try:
        sql.editContactPerson(request.get_json()['contactPerson'])
        return jsonify({'code': 1,'msg':'修改成功'})
    except Exception as e:
        return jsonify({'code': 0,'msg':str(e)})

@app.route("/editInviteFriendsQuantity", methods=['post'])
def editInviteFriendsQuantity():
    sql = _sql.DBHP("telegram-bot")
    try:
        sql.editInviteFriendsQuantity(request.get_json()['inviteFriendsQuantity'])
        return jsonify({'code': 1,'msg':'修改成功'})
    except Exception as e:
        return jsonify({'code': 0,'msg':str(e)})

@app.route("/editInviteFriendsAutoClearTime", methods=['post'])
def editInviteFriendsAutoClearTime():
    sql = _sql.DBHP("telegram-bot")
    try:
        sql.editInviteFriendsAutoClearTime(request.get_json()['inviteFriendsAutoClearTime'])
        return jsonify({'code': 1,'msg':'修改成功'})
    except Exception as e:
        return jsonify({'code': 0,'msg':str(e)})

@app.route("/editDeleteSeconds", methods=['post'])
def editDeleteSeconds():
    sql = _sql.DBHP("telegram-bot")
    try:
        sql.editDeleteSeconds(request.get_json()['deleteSeconds'])
        return jsonify({'code': 1,'msg':'修改成功'})
    except Exception as e:
        return jsonify({'code': 0,'msg':str(e)})

def flask():
    http_server = WSGIServer(('127.0.0.1', 5555), app)
    print(f"* Running on http://{http_server.address[0]}:{http_server.address[1]}")
    http_server.serve_forever()