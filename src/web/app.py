import os,sys,mimetypes,json
from flask import Flask, render_template, jsonify, request
from gevent.pywsgi import WSGIServer
from src.sql._sql import DBHP
from src.common.utils import Log
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys.executable, '../resources', 'templates')
    static_folder = os.path.join(sys.executable, '../resources', 'static')
    print("template_folder")
    print(template_folder)
    app = Flask(__name__, template_folder=template_folder,
                static_folder=static_folder)
else:
    app = Flask(__name__, template_folder='../../resources/templates',static_folder='../../resources/static')

sql = DBHP()

@app.route("/")
async def index():
    return render_template(r'index.html')

@app.route("/getLogList", methods=['get'])
def getLogList():
    return jsonify({'log': Log()._log['log_list']})
    
@app.route("/dev/getConfig", methods=['get'])
def getConfig():
    sql = DBHP()
    list = [{'key':'机器人名称','value':sql.botusername},
            {'key':'密码','value':sql.password},
            {'key':'邀请好友限制发言','value':sql.inviteFriendsSet},
            {'key':'关注频道限制发言','value':sql.followChannelSet},
            {'key':'邀请指定人数','value':sql.inviteFriendsQuantity},
            {'key':'自动删除系统消息(秒)','value':sql.inviteFriendsAutoClearTime},
            {'key':'重置天数(n天为一个周期)','value':sql.deleteSeconds},
            {'key':'邀请奖金功能','value':sql.invitationBonusSet},
            {'key':'每邀请(n人)获取奖金','value':sql.inviteMembers},
            {'key':'邀请达标赚取(n元)奖金','value':sql.inviteEarnedOutstand},
            {'key':'满(n元)结算奖金','value':sql.inviteSettlementBonus},
            {'key':'设定联系人','value':sql.contactPerson},
        ]
    return jsonify({'code':200,'data':{'list':list}})

@app.route("/dev/updateConfig", methods=['post'])
def updateConfig():
    data = request.get_json()
    data['value'] = 'False' if data['value'] == '关闭' else 'True'
    match data['key']:
        case "密码":
            key='password'
        case "自动删除系统消息(秒)":
            key='inviteFriendsAutoClearTime'
        case "邀请好友限制发言":
            key = 'inviteFriendsSet'
        case "关注频道限制发言":
            key = 'followChannelSet'
        case "邀请指定人数":
            key='inviteFriendsQuantity'
        case "重置天数(n天为一个周期)":
            key='deleteSeconds'
        case "邀请奖金功能":
            key='invitationBonusSet'
        case "每邀请(n人)获取奖金":
            key='inviteMembers'
        case "邀请达标赚取(n元)奖金":
            key='inviteEarnedOutstand'
        case "满(n元)结算奖金":
            key='inviteSettlementBonus'
        case "设定联系人":
            key='contactPerson'
    sql.editConfig(key,data['value'])
    return jsonify({'code':200,'data':{}})

@app.route("/dev/groupCategory", methods=['post'])
def groupCategory():
    sql = DBHP()
    list = []
    results=sql.getAllJoinGroupIdAndTitle()
    for result in results:
        list.append({"groupId":result[0],"groupTitle":result[1]})
    return jsonify({'code':200,'data':{'list':list}})

@app.route("/dev/getAdvertiseData", methods=['post'])
def getAdvertiseData():
    req = request.data.decode("utf8")
    sql = DBHP()
    list = []
    groupId = json.loads(req)['category']
    results=sql.getAdvertise(groupId)
    for result in results:
        list.append({"groupId":result[1],"groupTitle":result[2],"advertiseContent":result[3],"advertiseTime":result[4]})
    return jsonify({'code':200,'data':{'list':list}})


@app.route("/dev/updateAdvertiseData", methods=['post'])
def updateAdvertiseData():
    #{'advertiseContent': 'asd', 'advertiseTime': '55', 'groupId': '-1001700543954', 'groupTitle': 'CCP1121Group'}
    data = request.get_json() 
    sql=DBHP()
    sql.updateAdvertise(data['groupId'],data['advertiseContent'],data['advertiseTime'])
    return jsonify({'code':200,'data':{}})

def flask(port):
    http_server = WSGIServer(('0.0.0.0', port), app)
    #print(f"* Running on http://{http_server.address[0]}:{http_server.address[1]}")
    http_server.serve_forever()