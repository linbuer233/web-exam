#
# 生成token
from bson import ObjectId
import jwt
from pymongo import MongoClient

# from pymongo.server_api import ServerApi
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import numpy as np
import random

url = "mongodb://localhost:27017/"
client = MongoClient(url)
database = client.get_database("webexam")
app = FastAPI()
# 允许所有来源的跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 你可以将 '*' 替换为特定的前端源，如 'http://localhost:3000'
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


def createtoken(username, id, role):
    payload = {
        "exp": datetime.now() + timedelta(hours=6),  # 令牌过期时间
        "username": username,  # 想要传递的信息,如用户名ID
        "id": id,
        "role": role,
    }
    key = "SECRET_KEY"
    encoded_jwt = jwt.encode(payload, key, algorithm="HS256")
    return encoded_jwt


def yanzrole(token):
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        if payload["role"] != "admin":
            return {"status": 500, "error": "Unauthorized"}
    except jwt.ExpiredSignatureError:
        return {"status": 500, "error": "Token expired"}


# 定义请求体模型
class LoginModel(BaseModel):
    id: str
    pwd: str


class login_yzModel(BaseModel):
    token: str


@app.post("/api/login")
async def login(login_data: LoginModel):
    print("Welcome")
    query = dict(login_data)
    user = database.get_collection("user")
    try:
        result = user.find_one(query)
        print(result)
        token = createtoken(result["user"], result["id"], result["role"])
        return {
            "user": result["user"],
            "token": token,
            "id": result["id"],
            "role": result["role"],
        }
    except:  # noqa: E722
        print("error")
        return 500


@app.post("/api/login_yz")
async def login_yz(token: login_yzModel):
    try:
        payload = jwt.decode(token.token, "SECRET_KEY", algorithms=["HS256"])
        return {
            "status": 200,
            "user": payload["username"],
            "role": payload["role"],
            "id": payload["id"],
        }
    except jwt.ExpiredSignatureError:
        return {"status": 500, "error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"status": 500, "error": "Invalid token"}


@app.post("/api/change_password")
async def change_password(res: dict):
    user = database.get_collection("user")
    try:
        user.update_one({"id": res["id"]}, {"$set": {"pwd": res["pwd"]}})
        return {"status": 200, "message": "change_success"}
    except:  # noqa: E722
        print("error")
        return {"status": 500, "error": "change_error"}


@app.get("/api/get_users")
async def get_users():
    users = database.get_collection("user")
    result = [
        {
            "id": user["id"],
            "user": user["user"],
            "role": user["role"],
        }
        for user in users.find()
    ]
    # 使用sorted函数排序
    sorted_data = sorted(result, key=lambda x: x["id"])
    return sorted_data


@app.get("/api/userisexists")
async def userisexists(id: str):
    user = database.get_collection("user")
    return user.count_documents({"id": id}) > 0


@app.post("/api/add_user")
async def add_user(usermsg: dict):
    user = database.get_collection("user")
    try:
        user.insert_one(usermsg)
        return {"status": 200, "message": "add_success"}
    except:  # noqa: E722
        print("error")
        return {"status": 500, "error": "add_error"}


@app.post("/api/delete_user")
async def delete_user(id: dict):
    id = id["id"]
    token = id["token"]
    yanzrole(token)
    user = database.get_collection("user")
    try:
        user.delete_one({"id": id})
        return {"status": 200, "message": "delete_success"}
    except:  # noqa: E722
        print("error")
        return {"status": 500, "error": "delete_error"}


@app.post("/api/change_userinfo")
async def change_userinfo(res: dict):
    user = database.get_collection("user")
    token = res["token"]
    yanzrole(token)
    try:
        user.update_one(
            {"id": res["id"]}, {"$set": {"user": res["user"], "role": res["role"]}}
        )
        return {"status": 200, "message": "change_success"}
    except:  # noqa: E722
        print("error")
        return {"status": 500, "error": "change_error"}


################################################################
# QUESTIONS
################################################################


# 批量导入
@app.post("/api/createquestion/pidao")
def pidao_create_question(res: dict):
    questionstore = database.get_collection("questionstore")
    try:
        for i in range(len(res["data"])):
            questionstore.insert_one(res["data"][i])
        return {"status": 200, "message": "create_success"}
    except Exception as e:  # 捕获所有异常，并将其赋值给变量e
        print(f"error: {e}")  # 打印错误信息
        return {"status": 500, "error": "create_error"}


# 单题导入
@app.post("/api/createquestion/singledao")
def singledao_create_question(res: dict):
    questionstore = database.get_collection("questionstore")
    try:
        questionstore.insert_one(res)
        return {"status": 200, "message": "create_success"}
    except Exception as e:  # 捕获所有异常，并将其赋值给变量e
        print(f"error: {e}")  # 打印错误信息
        return {"status": 500, "error": "create_error"}


# 更新题目
@app.post("/api/createquestion/update_singledao")
def update_singledao_create_question(res: dict):
    questionstore = database.get_collection("questionstore")
    print(res)
    try:
        questionstore.update_one({"_id": ObjectId(res["uid"])}, {"$set": res["data"]})
        return {"status": 200, "message": "update_success"}
    except Exception as e:  # 捕获所有异常，并将其赋值给变量e
        print(f"error: {e}")  # 打印错误信息
        return {"status": 500, "error": "create_error"}


# 获取标签和题库信息
@app.get("/api/question/get_questionstore_info")
def get_questionstore_info():
    questionstore = database.get_collection("questionstore")
    unique_tags = questionstore.distinct("tag")
    unique_qustore = questionstore.distinct("qustore")
    allnumlist = []
    dannumlist = []
    duonumlist = []
    pannumlist = []
    for i in unique_qustore:
        allnum = questionstore.count_documents({"qustore": i})
        dannum = questionstore.count_documents({"qustore": i, "qutype": "0"})
        duonum = questionstore.count_documents({"qustore": i, "qutype": "1"})
        pannum = questionstore.count_documents({"qustore": i, "qutype": "2"})
        allnumlist.append(allnum)
        dannumlist.append(dannum)
        duonumlist.append(duonum)
        pannumlist.append(pannum)
    # 打印去重后的tag值
    print(unique_tags, unique_qustore)
    return {
        "status": 200,
        "tag": unique_tags,
        "qustore": unique_qustore,
        "allnum": allnumlist,
        "duonum": duonumlist,
        "pannum": pannumlist,
        "dannum": dannumlist,
    }


# 获取试题
@app.get("/api/question/get_questions")
async def get_questions(qustore: str, qutag: str, tix: str, start: int):
    print(qustore, qutag, tix, start)
    questionstore = database.get_collection("questionstore")
    # questionstore = database.get_collection("questionstore")
    tixlist = {"选择题": "0", "多选题": "1", "判断题": "2"}
    qulen = 10
    if qustore == "全部题库":
        if qutag == "全部标签":
            if tix == "全部题型":
                # 查询所有问题
                qulength = questionstore.count_documents({})
                questionslist = questionstore.find({}).skip(start).limit(qulen)
            else:
                # 查询特定题型的问题
                print(
                    "=====", {"qustore": qustore, "tag": qutag, "qutype": tixlist[tix]}
                )
                questionslist = (
                    questionstore.find({"qutype": tixlist[tix]})
                    .skip(start)
                    .limit(qulen)
                )
                qulength = questionstore.count_documents({"qutype": tixlist[tix]})
        else:
            if tix == "全部题型":
                # 查询特定标签的问题
                questionslist = (
                    questionstore.find({"tag": qutag}).skip(start).limit(qulen)
                )
                qulength = questionstore.count_documents({"tag": qutag})
            else:
                # 查询特定标签和特定题型的问题
                questionslist = (
                    questionstore.find({"tag": qutag, "qutype": tixlist[tix]})
                    .skip(start)
                    .limit(qulen)
                )
                qulength = questionstore.count_documents(
                    {"tag": qutag, "qutype": tixlist[tix]}
                )
    else:
        if qutag == "全部标签":
            if tix == "全部题型":
                # 查询所有问题
                questionslist = (
                    questionstore.find({"qustore": qustore}).skip(start).limit(qulen)
                )
                qulength = questionstore.count_documents({"qustore": qustore})
            else:
                # 查询特定题型的问题
                questionslist = (
                    questionstore.find({"qustore": qustore, "qutype": tixlist[tix]})
                    .skip(start)
                    .limit(qulen)
                )
                qulength = questionstore.count_documents(
                    {"qustore": qustore, "qutype": tixlist[tix]}
                )
        else:
            if tix == "全部题型":
                # 查询特定标签的问题
                questionslist = (
                    questionstore.find({"qustore": qustore, "tag": qutag})
                    .skip(start)
                    .limit(qulen)
                )
                qulength = questionstore.count_documents(
                    {"qustore": qustore, "tag": qutag}
                )
            else:
                # 查询特定标签和特定题型的问题
                questionslist = (
                    questionstore.find(
                        {"qustore": qustore, "tag": qutag, "qutype": tixlist[tix]}
                    )
                    .skip(start)
                    .limit(qulen)
                )
                qulength = questionstore.count_documents(
                    {"qustore": qustore, "tag": qutag, "qutype": tixlist[tix]}
                )
    # 将查询结果转换为列表或其他格式
    questions = []
    for question in questionslist:
        question["id"] = str(question["_id"])
        del question["_id"]
        questions.append(question)
    return {"status": 200, "data": questions, "qulength": qulength}


# 删除试题
@app.post("/api/question/delete_question")
async def delete_question(id: dict):
    uid = id["id"]
    token = id["token"]
    yanzrole(token)
    questionstore = database.get_collection("questionstore")
    examstore = database.get_collection("examlist")
    qustorePra = database.get_collection("qustorepractice")
    try:
        questionstore.delete_one({"_id": ObjectId(uid)})
        # 删除考试中的题目
        exams = examstore.find()
        for exam in exams:
            exam_dan = exam["danidlist"]
            exam_duo = exam["duoidlist"]
            exam_pan = exam["panidlist"]
            exam_name = exam["examname"]
            if uid in list(exam_dan):
                exam_dan.remove(uid)
                examstore.update_one(
                    {"examname": exam_name},
                    {"$set": {"danidlist": exam_dan}},
                )
            if uid in list(exam_duo):
                exam_duo.remove(uid)
                examstore.update_one(
                    {"examname": exam_name},
                    {"$set": {"duoidlist": exam_duo}},
                )
            if uid in list(exam_pan):
                exam_pan.remove(uid)
                examstore.update_one(
                    {"examname": exam_name},
                    {"$set": {"panidlist": exam_pan}},
                )
        # 删除考生练习数据库 qustorepratice
        qustorePra_subs = qustorePra.find()
        for i in qustorePra_subs:
            qustore_name = i["qustorename"]
            qustorePra_subs_user_an_status = i["user_answers_status"]
            qustorePra_subs_user_an = i["user_answers"]
            if uid in qustorePra_subs_user_an_status.keys():
                qustorePra_subs_user_an_status.pop(uid)
            if uid in qustorePra_subs_user_an.keys():
                qustorePra_subs_user_an.pop(uid)
            qustorePra.update_one(
                {"qustorename": qustore_name},
                {
                    "$set": {
                        "user_answers_status": qustorePra_subs_user_an_status,
                        "user_answers": qustorePra_subs_user_an,
                    }
                },
            )
        return {"status": 200, "message": "delete_success"}
    except:  # noqa: E722
        print("error")
        return {"status": 500, "error": "delete_error"}


################################################################
# EXAMS
################################################################


# 创建考试
@app.post("/api/exam/create_exam")
def create_exams(resdata: dict):
    token = resdata["token"]
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        role = payload["role"]
        id = payload["id"]
        if role == "admin":
            examtype = "管理员创建"
        else:
            examtype = "学生创建"
    except jwt.ExpiredSignatureError:
        role = "admin"
        examtype = "管理员创建"
    res = resdata["data"]
    print(res)
    qustores = res["qustores"]
    tags = res["tags"]
    examstore = database.get_collection("examlist")
    questionstore = database.get_collection("questionstore")
    if len(tags) == 0:
        questions = questionstore.find({"qustore": {"$in": qustores}})
        questiondanlist = []
        questionduolist = []
        questionpanlist = []
        for i in questions:
            if i["qutype"] == "0":
                questiondanlist.append(str(i["_id"]))
            if i["qutype"] == "1":
                questionduolist.append(str(i["_id"]))
            if i["qutype"] == "2":
                questionpanlist.append(str(i["_id"]))
        try:
            fannaldanlist = np.array(questiondanlist)[
                random.sample(range(len(questiondanlist)), int(res["dannum"]))
            ]
            fannalduolist = np.array(questionduolist)[
                random.sample(range(len(questionduolist)), int(res["duonum"]))
            ]
            fannalpanlist = np.array(questionpanlist)[
                random.sample(range(len(questionpanlist)), int(res["pannum"]))
            ]
            # {'examname': '新建题库1728748452416', 'qustores': ['默认题库'], 'tags': '',
            # 'dannum': 96, 'danfen': 0.5, 'duonum': 50, 'duofen': 0.8, 'pannum': 40, 'panfen': 0.3,
            # 'valuecreatetime': '2024-10-12T15:54:19.000Z'}
            examdict = {
                "userid": id,
                "role": role,
                "examtype": examtype,
                "examname": res["examname"],
                "qustore": qustores,
                "tags": tags,
                "dannum": res["dannum"],
                "duonum": res["duonum"],
                "pannum": res["pannum"],
                "danidlist": list(fannaldanlist),
                "duoidlist": list(fannalduolist),
                "panidlist": list(fannalpanlist),
                "danfen": res["danfen"],
                "duofen": res["duofen"],
                "panfen": res["panfen"],
                "createtime": datetime.now(),
                "valuecreatetime": res["valuecreatetime"],
                "examtimelong": res["examtimelong"],
                "examCiShu": res["examCiShu"],
            }
            # 插入考试
            examstore.insert_one(examdict)
        except Exception as e:  # 捕获所有异常，并将其赋值给变量e
            print(f"error: {e}")  # 打印错误信息
            return {"status": 500, "error": "题目数量大于总题数"}
    if len(qustores) == 0:
        questions = questionstore.find({"tag": {"$in": tags}})
        questiondanlist = []
        questionduolist = []
        questionpanlist = []
        for i in questions:
            if i["qutype"] == "0":
                questiondanlist.append(str(i["_id"]))
            if i["qutype"] == "1":
                questionduolist.append(str(i["_id"]))
            if i["qutype"] == "2":
                questionpanlist.append(str(i["_id"]))
        try:
            fannaldanlist = np.array(questiondanlist)[
                random.sample(range(len(questiondanlist)), int(res["dannum"]))
            ]
            fannalduolist = np.array(questionduolist)[
                random.sample(range(len(questionduolist)), int(res["duonum"]))
            ]
            fannalpanlist = np.array(questionpanlist)[
                random.sample(range(len(questionpanlist)), int(res["pannum"]))
            ]
            examdict = {
                "userid": id,
                "role": role,
                "examtype": examtype,
                "examname": res["examname"],
                "qustore": qustores,
                "tags": tags,
                "dannum": res["dannum"],
                "duonum": res["duonum"],
                "pannum": res["pannum"],
                "danidlist": list(fannaldanlist),
                "duoidlist": list(fannalduolist),
                "panidlist": list(fannalpanlist),
                "danfen": res["danfen"],
                "duofen": res["duofen"],
                "panfen": res["panfen"],
                "createtime": datetime.now(),
                "valuecreatetime": res["valuecreatetime"],
                "examtimelong": res["examtimelong"],
                "examCiShu": res["examCiShu"],
            }
            # 插入考试
            examstore.insert_one(examdict)
        except Exception as e:  # 捕获所有异常，并将其赋值给变量e
            print(f"error: {e}")  # 打印错误信息
            return {"status": 500, "error": "题目数量大于总题数"}
    if len(tags) != 0 and len(qustores) != 0:
        questions = questionstore.find(
            {"tag": {"$in": tags}, "qustore": {"$in": qustores}}
        )
        questiondanlist = []
        questionduolist = []
        questionpanlist = []
        for i in questions:
            if i["qutype"] == "0":
                questiondanlist.append(str(i["_id"]))
            if i["qutype"] == "1":
                questionduolist.append(str(i["_id"]))
            if i["qutype"] == "2":
                questionpanlist.append(str(i["_id"]))
        try:
            fannaldanlist = np.array(questiondanlist)[
                random.sample(range(len(questiondanlist)), int(res["dannum"]))
            ]
            fannalduolist = np.array(questionduolist)[
                random.sample(range(len(questionduolist)), int(res["duonum"]))
            ]
            fannalpanlist = np.array(questionpanlist)[
                random.sample(range(len(questionpanlist)), int(res["pannum"]))
            ]
            examdict = {
                "userid": id,
                "role": role,
                "examtype": examtype,
                "examname": res["examname"],
                "qustore": qustores,
                "tags": tags,
                "dannum": res["dannum"],
                "duonum": res["duonum"],
                "pannum": res["pannum"],
                "danidlist": list(fannaldanlist),
                "duoidlist": list(fannalduolist),
                "panidlist": list(fannalpanlist),
                "danfen": res["danfen"],
                "duofen": res["duofen"],
                "panfen": res["panfen"],
                "createtime": datetime.now(),
                "valuecreatetime": res["valuecreatetime"],
                "examtimelong": res["examtimelong"],
                "examCiShu": res["examCiShu"],
            }
            # 插入考试
            examstore.insert_one(examdict)
        except Exception as e:  # 捕获所有异常，并将其赋值给变量e
            print(f"error: {e}")  # 打印错误信息
            return {"status": 500, "error": "题目数量大于总题数"}
    # 添加单选题题目
    return {"status": 200}


# 查询全部考试
@app.get("/api/exam/get_all_exams")
def get_all_exams(user: str, userid: str, role: str):
    print(user, userid, role)
    examstore = database.get_collection("examlist")
    if role == "admin":
        exams = examstore.find({"role": "admin"})
        exams_list = []
        for exam in exams:
            del exam["_id"]
            exams_list.append(exam)
    else:
        exams = examstore.find({"$or": [{"userid": userid}, {"role": "admin"}]})
        exams_list = []
        for exam in exams:
            del exam["_id"]
            exams_list.append(exam)
    return {"status": 200, "data": exams_list}


# 查询单个考试
@app.get("/api/exam/get_one_exams")
def get_one_exams(examname: str):
    examstore = database.get_collection("examlist")
    exam = examstore.find_one({"examname": examname})
    del exam["_id"]
    return {"status": 200, "data": exam}


# 删除考试
@app.post("/api/exam/delete_exam")
def delete_exam(res: dict):
    token = res["token"]
    examname = res["examname"]
    yanzrole(token)
    examstore = database.get_collection("examlist")
    examstore.delete_one({"examname": examname})
    return {"status": 200, "message": "delete_success"}


# 修改考试
@app.post("/api/exam/update_exam")
def update_exam(res: dict):
    token = res["token"]
    Yuanexamname = res["data"]["Yuanexamname"]
    yanzrole(token)
    examstore = database.get_collection("examlist")
    examstore.update_one({"examname": Yuanexamname}, {"$set": res["data"]})
    return {"status": 200, "message": "update_success"}


# 获取考试的题目信息
@app.get("/api/exam/get_exam_questions")
def get_exam_questions(examname: str):
    examstore = database.get_collection("examlist")
    exam = examstore.find_one({"examname": examname})
    questionstore = database.get_collection("questionstore")
    danqulist = []
    duoqulist = []
    panqulist = []
    for danid in exam["danidlist"]:
        danquestion = questionstore.find_one({"_id": ObjectId(danid)})
        danquestion["id"] = str(danquestion["_id"])
        del danquestion["_id"]
        danqulist.append(danquestion)
    for duoid in exam["duoidlist"]:
        duoquestion = questionstore.find_one({"_id": ObjectId(duoid)})
        duoquestion["id"] = str(duoquestion["_id"])
        del duoquestion["_id"]
        duoqulist.append(duoquestion)
    for panid in exam["panidlist"]:
        panquestion = questionstore.find_one({"_id": ObjectId(panid)})
        panquestion["id"] = str(panquestion["_id"])
        del panquestion["_id"]
        panqulist.append(panquestion)
    exam_questions = {
        "examname": exam["examname"],
        "id": exam["userid"],
        "role": exam["role"],
        "danquestions": danqulist,
        "duoquestions": duoqulist,
        "panquestions": panqulist,
        "danlist": exam["danidlist"],
        "duolist": exam["duoidlist"],
        "panlist": exam["panidlist"],
        "dannum": exam["dannum"],
        "duonum": exam["duonum"],
        "pannum": exam["pannum"],
        "danfen": exam["danfen"],
        "duofen": exam["duofen"],
        "panfen": exam["panfen"],
        "examtype": exam["examtype"],
        "qustore": exam["qustore"],
        "tags": exam["tags"],
        "createtime": exam["createtime"],
        "valuecreatetime": exam["valuecreatetime"],
        "examtimelong": exam["examtimelong"],
    }

    return {"status": 200, "data": exam_questions}


# 获取考试结果
@app.get("/api/exam/get_exam_useranswer")
def get_exam_useranswer(examname: str, id: str, examBT: str):
    examresult = database.get_collection("examresult")
    useranswer = examresult.find_one({"examname": examname})
    if useranswer is None:
        return {"status": 201, "message": "exam not found"}
    temp = useranswer["temp"]
    data = temp[id]
    return {"status": 200, "data": data}


# 存储考生考试中途情况
@app.post("/api/exam/store_exam_useranswer")
def store_exam_useranswer(res: dict):
    id = res["id"]
    examname = res["examname"]
    exam_re_data = res["data"]
    examresult = database.get_collection("examresult")
    useranswertemp = examresult.find_one({"examname": examname})
    if useranswertemp is None:
        useranswer = {"examname": examname, "temp": {}, "result": {}}
        examresult.insert_one(useranswer)
    useranswertemp = examresult.find_one({"examname": examname})
    temp = useranswertemp["temp"]
    temp[id] = exam_re_data
    examresult.update_one({"examname": examname}, {"$set": {"temp": temp}})
    return {"status": 200}


# 存储考生最终考试结果
@app.post("/api/exam/store_final_exam_result")
def store_final_exam_result(res: dict):
    id = res["id"]
    examname = res["examname"]
    examresult = database.get_collection("examresult")
    useranswertemp = examresult.find_one({"examname": examname})
    if useranswertemp is None:
        useranswer = {"examname": examname, "temp": {}, "result": {}}
        examresult.insert_one(useranswer)
    useranswertemp = examresult.find_one({"examname": examname})
    temp = useranswertemp["temp"]
    if id in temp.keys():
        del temp[id]
    result = useranswertemp["result"]
    if id not in result.keys():
        result[id] = {"user": res["user"], "examresultdata": []}
    result[id]["examresultdata"].append(
        {
            "fenshu": res["fenshu"],
            "dananswerlist": res["dananswerlist"],
            "duoanswerlist": res["duoanswerlist"],
            "pananswerlist": res["pananswerlist"],
            "danWRanswerlist": res["danWRanswerlist"],
            "duoWRanswerlist": res["duoWRanswerlist"],
            "panWRanswerlist": res["panWRanswerlist"],
        }
    )
    # 存入考生的错题
    store_Wrongquestions(
        id,
        res["examname"],
        res["roleofexamcreater"],
        res["danquestions"],
        res["duoquestions"],
        res["panquestions"],
        res["dananswerlist"],
        res["duoanswerlist"],
        res["pananswerlist"],
        res["danWRanswerlist"],
        res["duoWRanswerlist"],
        res["panWRanswerlist"],
    )
    examresult.update_one(
        {"examname": examname},
        {
            "$set": {
                "temp": temp,
                "examBT": res["examBT"],
                "roleofexamcreater": res["roleofexamcreater"],
                "idofcreater": res["idofcreater"],
                "createtime": res["createtime"],
                "examtimelong": res["examtimelong"],
                "qustore": res["qustore"],
                "tags": res["tags"],
                "danquestions": res["danquestions"],
                "duoquestions": res["duoquestions"],
                "panquestions": res["panquestions"],
                "dannum": res["dannum"],
                "duonum": res["duonum"],
                "pannum": res["pannum"],
                "danfen": res["danfen"],
                "duofen": res["duofen"],
                "panfen": res["panfen"],
                "dancorrectanswerlist": res["dancorrectanswerlist"],
                "duocorrectanswerlist": res["duocorrectanswerlist"],
                "pancorrectanswerlist": res["pancorrectanswerlist"],
                "result": result,
            }
        },
    )
    return {"status": 200}


# 存入考生的错题
def store_Wrongquestions(
    id,
    examname,
    roleofexamcreater,
    danquestions,
    duoquestions,
    panquestions,
    dananswerlist,
    duoanswerlist,
    pananswerlist,
    danWRanswerlist,
    duoWRanswerlist,
    panWRanswerlist,
):
    userWrongqustore = database.get_collection("userWrongqustore")
    for i in range(len(danWRanswerlist)):
        if danWRanswerlist[i] == "Right":
            continue
        quid = danquestions[i]["id"]
        if userWrongqustore.find_one({"quid": quid}) is not None:
            continue
        wrong_question = {
            "id": id,
            "quid": danquestions[i]["id"],
            "examname": examname,
            "roleofexamcreater": roleofexamcreater,
            "question": danquestions[i],
            "useranswer": dananswerlist[i],
        }
        userWrongqustore.insert_one(wrong_question)
    for i in range(len(duoWRanswerlist)):
        if duoWRanswerlist[i] == "Right":
            continue
        quid = duoquestions[i]["id"]
        if userWrongqustore.find_one({"quid": quid}) is not None:
            continue
        wrong_question = {
            "id": id,
            "quid": duoquestions[i]["id"],
            "examname": examname,
            "roleofexamcreater": roleofexamcreater,
            "question": duoquestions[i],
            "useranswer": duoanswerlist[i],
        }
        userWrongqustore.insert_one(wrong_question)
    for i in range(len(panWRanswerlist)):
        if panWRanswerlist[i] == "Right":
            continue
        quid = panquestions[i]["id"]
        if userWrongqustore.find_one({"quid": quid}) is not None:
            continue
        wrong_question = {
            "id": id,
            "quid": panquestions[i]["id"],
            "examname": examname,
            "roleofexamcreater": roleofexamcreater,
            "question": panquestions[i],
            "useranswer": pananswerlist[i],
        }
        userWrongqustore.insert_one(wrong_question)


# 考试结果页面获取考试结果
@app.get("/api/exam/get_examresult_page_data")
def get_examresult_page_data(examname: str, id: str):
    examresult = database.get_collection("examresult")
    useranswertemp = examresult.find_one({"examname": examname})
    user_result = useranswertemp["result"][id]["examresultdata"]
    data = user_result[len(user_result) - 1]
    data["danquestions"] = useranswertemp["danquestions"]
    data["duoquestions"] = useranswertemp["duoquestions"]
    data["panquestions"] = useranswertemp["panquestions"]
    data["dancorrectanswerlist"] = useranswertemp["dancorrectanswerlist"]
    data["duocorrectanswerlist"] = useranswertemp["duocorrectanswerlist"]
    data["pancorrectanswerlist"] = useranswertemp["pancorrectanswerlist"]
    data["danfen"] = useranswertemp["danfen"]
    data["duofen"] = useranswertemp["duofen"]
    data["panfen"] = useranswertemp["panfen"]
    return {"status": 200, "data": data}


# 获取考生的考试次数
@app.get("/api/exam/get_user_examCishu")
def get_user_examCishu(examname: str, id: str, examCishu: str):
    examresult = database.get_collection("examresult")
    useranswertemp = examresult.find_one({"examname": examname})
    if useranswertemp is None:
        return {"status": 200, "message": "exam not found go head"}
    try:
        user_result = useranswertemp["result"][id]["examresultdata"]
        if int(examCishu) > len(user_result):
            return {"status": 200, "message": "exam not enough go head"}
        else:
            return {"status": 500, "message": "can't exam"}
    except:  # noqa: E722
        return {"status": 200, "message": "user not found"}


# 获取考生的考试结果
@app.get("/api/exam/get_user_examresult")
def get_user_examresult():
    examresult = database.get_collection("examresult")
    useranswertemp = examresult.find()
    if useranswertemp is None:
        return {"status": 201, "message": "exam not found go head"}
    temp = []
    for i in useranswertemp:
        if i["roleofexamcreater"] == "student":
            continue
        examname = i["examname"]
        user_result_all = i["result"]
        user_one_exam_result = []
        user_id_all = user_result_all.keys()
        for ii in user_id_all:
            user_result_temp = user_result_all[ii]
            bestrrecord = 0
            for urt_i in user_result_temp["examresultdata"]:
                tempp = urt_i["fenshu"]
                if tempp > bestrrecord:
                    bestrrecord = tempp
            user_one_exam_result.append(
                {
                    "id": ii,
                    "user": user_result_temp["user"],
                    "fenshu": bestrrecord,
                    "user_exam_cishu": len(user_result_temp["examresultdata"]),
                }
            )
        temp.insert(
            0,
            {
                "uid": i["idofcreater"],
                "roleofexamcreater": i["roleofexamcreater"],
                "examname": examname,
                "examtimelong": i["examtimelong"],
                "examBT": i["examBT"],
                "allfen": i["dannum"] * i["danfen"]
                + i["duonum"] * i["duofen"]
                + i["pannum"] * i["panfen"],
                "examcompeletenum": len(user_id_all),
                "uoer": user_one_exam_result,
            },
        )
    return {"status": 200, "data": temp}


# 获取考生自己创建和管理创建的考试
@app.get("/api/exam/get_userown_examresult")
def get_userown_examresult(id: str):
    examresult = database.get_collection("examresult")
    useranswertemp = examresult.find()
    if useranswertemp is None:
        return {"status": 201, "message": "exam not found go head"}
    temp = []
    for i in useranswertemp:
        if i["roleofexamcreater"] == "student":
            if i["idofcreater"] != id:
                continue
        examname = i["examname"]
        user_result_all = i["result"]
        user_one_exam_result = []
        user_result_temp = user_result_all[id]
        bestrrecord = 0
        for urt_i in user_result_temp["examresultdata"]:
            tempp = urt_i["fenshu"]
            if tempp > bestrrecord:
                bestrrecord = tempp
            user_one_exam_result.append(
                {
                    "id": id,
                    "user": user_result_temp["user"],
                    "onefenshu": urt_i["fenshu"],
                }
            )
        temp.insert(
            0,
            {
                "uid": i["idofcreater"],
                "roleofexamcreater": i["roleofexamcreater"],
                "examname": examname,
                "fenshu": bestrrecord,
                "examtimelong": i["examtimelong"],
                "examBT": i["examBT"],
                "allfen": i["dannum"] * i["danfen"]
                + i["duonum"] * i["duofen"]
                + i["pannum"] * i["panfen"],
                "uoer": user_one_exam_result,
            },
        )
    return {"status": 200, "data": temp}
    pass


# 删除考生的结果
@app.post("/api/exam/delete_user_examresult")
def delete_user_examresult(res: dict):
    examname = res["examname"]
    examresult = database.get_collection("examresult")
    try:
        examresult.delete_one({"examname": examname})
        return {"status": 200, "message": "delete success"}
    except:  # noqa: E722
        return {"status": 500, "message": "delete fail"}


################################################################
# WrongQuestion
################################################################
# 获取错题
@app.get("/api/get_user_wrongquestions")
def get_user_wrongquestions(id: str, start: int, limit: str):
    userWrongqustore = database.get_collection("userWrongqustore")
    length = userWrongqustore.count_documents({"id": id})
    if limit == "True":
        Wrongquestions = userWrongqustore.find({"id": id}).skip(start).limit(10)
    else:
        Wrongquestions = userWrongqustore.find({"id": id}).skip(start).limit(1)
    Wqulist = []
    for i in Wrongquestions:
        Wqulist.insert(
            0,
            {
                "id": i["id"],
                "quid": i["quid"],
                "qutype": i["question"]["qutype"],
                "question": i["question"],
                "useranswer": i["useranswer"],
            },
        )
    return {"status": 200, "data": Wqulist, "length": length}


# 删除用户的错题
@app.post("/api/delete_user_wrongquestions")
def delete_user_wrongquestions(id: str, quid: str):
    userWrongqustore = database.get_collection("userWrongqustore")
    userWrongqustore.delete_one({"id": id, "quid": quid})
    return {"status": 200, "message": "delete success"}


# 清空用户的错题库
@app.post("/api/delete_alluser_wrong_question")
def delete_alluser_wrong_question(id: str):
    userWrongqustore = database.get_collection("userWrongqustore")
    userWrongqustore.delete_many({"id": id})
    return {"status": 200, "message": "delete success"}


################################################################
# Qustore practice
################################################################
@app.get("/api/qustore/get_SunXunpractice_data")
def get_SunXunpractice_data(qustorename: str, id: str):
    qustorePra = database.get_collection("qustorepractice")
    questionstore = database.get_collection("questionstore")
    questions = questionstore.find({"qustore": qustorename})
    SunXunpractice_data = qustorePra.find_one({"qustorename": qustorename})
    if SunXunpractice_data is None:
        # 没有就初始化
        qustorePra.insert_one(
            {
                "qustorename": qustorename,
                "user_answer_status": {},  # 用户是否答题
                "user_answer": {},  # 用户的的选择
            }
        )
    danquidlist = []
    duoquidlist = []
    panquidlist = []
    danuserstatus = {}
    duouserstatus = {}
    panuserstatus = {}
    danusersel = {}
    duousersel = {}
    panusersel = {}
    #
    SunXunpractice_data = qustorePra.find_one({"qustorename": qustorename})
    #
    if id not in SunXunpractice_data["user_answer_status"].keys():
        SunXunpractice_data["user_answer_status"][id] = {}
        SunXunpractice_data["user_answer"][id] = {}
        SunXunpractice_data["user_answer_status"][id]["nowPosition"] = 0
        for question_i in questions:
            SunXunpractice_data["user_answer_status"][id][str(question_i["_id"])] = 0
            SunXunpractice_data["user_answer"][id][str(question_i["_id"])] = ""
        #
        questions = questionstore.find({"qustore": qustorename})
        #
        for qu_i in questions:
            if (
                str(qu_i["_id"])
                not in SunXunpractice_data["user_answer_status"][id].keys()
            ):
                SunXunpractice_data["user_answer_status"][id][str(qu_i["_id"])] = 0
                SunXunpractice_data["user_answer"][id][str(question_i["_id"])] = ""
            print(str(qu_i["_id"]))
            if qu_i["qutype"] == "0":
                danquidlist.append(str(qu_i["_id"]))
                danuserstatus[str(qu_i["_id"])] = SunXunpractice_data[
                    "user_answer_status"
                ][id][str(qu_i["_id"])]
                danusersel[str(qu_i["_id"])] = SunXunpractice_data["user_answer"][id][
                    str(qu_i["_id"])
                ]
            if qu_i["qutype"] == "1":
                duoquidlist.append(str(qu_i["_id"]))
                duouserstatus[str(qu_i["_id"])] = SunXunpractice_data[
                    "user_answer_status"
                ][id][str(qu_i["_id"])]
                duousersel[str(qu_i["_id"])] = SunXunpractice_data["user_answer"][id][
                    str(qu_i["_id"])
                ]
            if qu_i["qutype"] == "2":
                panquidlist.append(str(qu_i["_id"]))
                panuserstatus[str(qu_i["_id"])] = SunXunpractice_data[
                    "user_answer_status"
                ][id][str(qu_i["_id"])]
                panusersel[str(qu_i["_id"])] = SunXunpractice_data["user_answer"][id][
                    str(qu_i["_id"])
                ]
        qustorePra.update_one(
            {"qustorename": qustorename}, {"$set": SunXunpractice_data}
        )
    else:
        for qu_i in questions:
            if str(qu_i["_id"]) not in SunXunpractice_data["user_answer_status"][id]:
                SunXunpractice_data["user_answer_status"][id][str(qu_i["_id"])] = 0
            if qu_i["qutype"] == "0":
                danquidlist.append(str(qu_i["_id"]))
                danuserstatus[str(qu_i["_id"])] = SunXunpractice_data[
                    "user_answer_status"
                ][id][str(qu_i["_id"])]
                danusersel[str(qu_i["_id"])] = SunXunpractice_data["user_answer"][id][
                    str(qu_i["_id"])
                ]
            if qu_i["qutype"] == "1":
                duoquidlist.append(str(qu_i["_id"]))
                duouserstatus[str(qu_i["_id"])] = SunXunpractice_data[
                    "user_answer_status"
                ][id][str(qu_i["_id"])]
                duousersel[str(qu_i["_id"])] = SunXunpractice_data["user_answer"][id][
                    str(qu_i["_id"])
                ]
            if qu_i["qutype"] == "2":
                panquidlist.append(str(qu_i["_id"]))
                panuserstatus[str(qu_i["_id"])] = SunXunpractice_data[
                    "user_answer_status"
                ][id][str(qu_i["_id"])]
                panusersel[str(qu_i["_id"])] = SunXunpractice_data["user_answer"][id][
                    str(qu_i["_id"])
                ]
            qustorePra.update_one(
                {"qustorename": qustorename}, {"$set": SunXunpractice_data}
            )
    return {
        "status": 200,
        "nowPosition": SunXunpractice_data["user_answer_status"][id]["nowPosition"],
        "danquidlist": danquidlist,
        "duoquidlist": duoquidlist,
        "panquidlist": panquidlist,
        "danuserstatus": danuserstatus,
        "duouserstatus": duouserstatus,
        "panuserstatus": panuserstatus,
        "danusersel": danusersel,
        "duousersel": duousersel,
        "panusersel": panusersel,
    }


# 获取一个题库中的题
@app.get("/api/qustore/get_onequ_data")
def get_onequ_data(quid: str):
    questionstore = database.get_collection("questionstore")
    question = questionstore.find_one({"_id": ObjectId(quid)})
    del question["_id"]
    return {"status": 200, "data": question}


# 获取这题的状态
@app.get("/api/qustore/get_user_answer_status")
def get_user_answer_status(qustorename: str, id: str, nowquid: str):
    qustorePra = database.get_collection("qustorepractice")
    SunXunpractice_data = qustorePra.find_one({"qustorename": qustorename})
    user_sel = SunXunpractice_data["user_answer"][id][nowquid]
    user_answer_status = SunXunpractice_data["user_answer_status"][id][nowquid]
    return {
        "status": 200,
        "user_answer_status": user_answer_status,
        "user_sel": user_sel,
    }


# 存储这题的状态
@app.post("/api/qustore/store_user_answer_status")
def store_user_answer_status(
    qustorename: str,
    id: str,
    nowquid: str,
    user_answer_status: int,
    user_sel: str,
    nowPosition: int,
):
    qustorePra = database.get_collection("qustorepractice")
    questionstore = database.get_collection("questionstore")
    userWrongqustore = database.get_collection("userWrongqustore")
    SunXunpractice_data = qustorePra.find_one({"qustorename": qustorename})
    SunXunpractice_data["user_answer_status"][id][nowquid] = user_answer_status
    SunXunpractice_data["user_answer_status"][id]["nowPosition"] = nowPosition
    SunXunpractice_data["user_answer"][id][nowquid] = user_sel
    qustorePra.update_one({"qustorename": qustorename}, {"$set": SunXunpractice_data})
    # 如果题目是错的
    if user_answer_status == 2:
        Wrongqu = userWrongqustore.find_one({"id": id, "quid": nowquid})
        if Wrongqu is None:
            question = questionstore.find_one({"_id": ObjectId(nowquid)})
            question["id"] = str(question["_id"])
            del question["_id"]
            userWrongqustore.insert_one(
                {
                    "id": id,
                    "quid": nowquid,
                    "question": question,
                    "useranswer": user_sel,
                    "qustorename": qustorename,
                }
            )
    return {"status": 200, "message": "success"}
