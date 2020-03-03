# coding: utf-8
import pymysql
import db

USER_ID = 31
WITHDRAW_LIMIT = 50
WITHDRAW_TIMES = 1

conn = pymysql.connect(**db.config)
cursor = conn.cursor()


# 查看钱包
def my_wallet():
    # status: 10(未收货金额) 20(可提现金额)
    sql = "SELECT sum(tb_pay_income) FROM tb_order WHERE user_id = '%s' AND tb_status = 10" % USER_ID
    cursor.execute(sql)
    not_receive = cursor.fetchone()[0]
    if not_receive is None:
        not_receive = 0
    sql = "SELECT sum(tb_clear_income) FROM tb_order WHERE user_id = '%s' AND tb_status = 20" % USER_ID
    cursor.execute(sql)
    can_withdraw = cursor.fetchone()[0]
    if can_withdraw is None:
        can_withdraw = 0
    return {'not_receive': not_receive, 'can_withdraw': can_withdraw}


# 提现
def withdraw_cash_master():
    # 是否还有钱，没钱直接返回
    sql = "SELECT withdraw_amount FROM wx_user_info WHERE id = %s" % USER_ID
    cursor.execute(sql)
    withdraw_amount = cursor.fetchone()[0]
    if withdraw_amount <= 0:
        return {'code': 405, 'msg': '申请失败，可提现0元'}
    # 金额超过50元报警
    elif withdraw_amount >= 50:
        # todo 进行报警，检查
        print()
    amount_money = my_wallet()
    # 提醒人员进行人工转账


# 找出用户id
def find_user():
    print()


ret = withdraw_cash_master()
print(ret)
