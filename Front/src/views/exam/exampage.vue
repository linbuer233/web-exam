<template>
    <div class="exampage">
        <el-row :gutter="0" style="height:100%">
            <el-col :span="4">
                <el-card style="height:99%;box-shadow:0 0 0 0;margin: 2px;">
                    <div>
                        <p style="text-align: center; font-size: 25px;">答题卡</p>
                    </div>
                    <!-- 答题卡 -->
                    <div style="margin: 0px;">
                        <el-scrollbar height="80vh" style="margin: 0px;padding:0px">
                            <div>
                                <el-row>
                                    <el-text class="mx-1" size="large" type="info">一、选择题</el-text>
                                    <div style="width: 100%;padding:0px;margin: 10px;margin-right: 0px;">
                                        <el-button style="margin: 4px;" v-for="(question, index) in danquestions"
                                            :key="question.id" @click="scrollToQuestion(question.id)"
                                            :type="typeof (form.dananswerlist[index].value) == 'undefined' ? 'success' : 'null'"
                                            circle>
                                            {{ index + 1 }}
                                        </el-button>
                                    </div>
                                </el-row>
                                <br />
                                <el-row>
                                    <el-text class="mx-1" size="large" type="info">二、多选题</el-text>
                                    <div style="width: 100%;padding:0px;margin: 10px;margin-right: 0px;">
                                        <el-button style="margin: 4px;" v-for="(question, index) in duoquestions"
                                            :key="question.id" @click="scrollToQuestion(question.id)"
                                            :type="(form.duoanswerlist[index] == null || form.duoanswerlist[index].length == 0) ? null : 'success'"
                                            circle>
                                            {{ index + 1 }}
                                        </el-button>
                                    </div>
                                </el-row>
                                <br />
                                <el-row>
                                    <el-text class="mx-1" size="large" type="info">三、判断题</el-text>
                                    <div style="width: 100%;padding:0px;margin: 10px;margin-right: 0px;">
                                        <el-button style="margin: 4px;" v-for="(question, index) in panquestions"
                                            :key="question.id" @click="scrollToQuestion(question.id)"
                                            :type="form.pananswerlist[index] == null ? null : 'success'" circle>
                                            {{ index + 1 }}
                                        </el-button>
                                    </div>
                                </el-row>
                            </div>
                        </el-scrollbar>
                    </div>
                </el-card>
            </el-col>
            <!-- 答题区 -->
            <el-col :span="16">
                <el-card style="height:99%;box-shadow:0 0 0 0;margin: 2px;">
                    <el-scrollbar height="92vh">
                        <div class="question-content">
                            <el-form :model="form">
                                <h2>一、选择题</h2>
                                <div v-for="(question, index) in danquestions" :key="question.id" :id="question.id"
                                    class="question">
                                    <el-text tag="b" style="font-size: x-large;">{{ index + 1
                                        }}、{{
                                            question.question
                                        }} </el-text>
                                    <br />
                                    <br />
                                    <div v-for="(qu, idx) in question.options" :key="idx">
                                        <el-radio v-model="form.dananswerlist[index]" :value="idx" :key="idx">
                                            <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                            <el-text style="font-size: large;">{{ qu }}</el-text>
                                        </el-radio>
                                    </div>
                                </div>
                                <h2>二、多选题</h2>
                                <div v-for="(question, index) in duoquestions" :key="question.id" :id="question.id"
                                    @click="scrollToQuestion(question.id)" class="question">
                                    <el-text tag="b" style="font-size: x-large;">{{ index + 1
                                        }}、{{
                                            question.question
                                        }} </el-text>
                                    <br />
                                    <br />
                                    <div v-for="(qu, idx) in question.options" :key="idx">
                                        <el-checkbox-group v-model="form.duoanswerlist[index]">
                                            <el-checkbox :label="idx" size="large" :key="idx">
                                                <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                                <el-text style="font-size: large;">{{ qu }}</el-text>
                                            </el-checkbox>
                                        </el-checkbox-group>
                                    </div>
                                </div>
                                <h2>三、判断题</h2>
                                <div v-for="(question, index) in panquestions" :key="question.id" :id="question.id"
                                    @click="scrollToQuestion(question.id)" class="question">
                                    <el-text tag="b" style="font-size: x-large;">{{ index + 1
                                        }}、{{
                                            question.question
                                        }} </el-text>
                                    <br />
                                    <br />
                                    <el-radio v-for="(qu, idx) in question.options" v-model="form.pananswerlist[index]"
                                        :value="idx" :key="idx">
                                        <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                        <el-text style="font-size: large;">{{ qu }}</el-text>
                                    </el-radio>
                                </div>
                            </el-form>
                        </div>
                    </el-scrollbar>
                </el-card>
            </el-col>
            <!-- 考试信息 -->
            <el-col :span="4">
                <el-card style="height:99%;box-shadow:0 0 0 0;margin: 2px;">
                    <template #header>
                        <div>
                            <p style="text-align: center; font-size: 25px;">考试信息</p>
                        </div>
                    </template>
                    <span>考试名称：</span>
                    <el-text type="primary">{{ examname }}</el-text>
                    <br />
                    <br />
                    <span>题量：</span>
                    <el-text class="mx-1" type="primary">{{ dannum + duonum + pannum
                        }}</el-text>
                    <br />
                    <br />
                    <span>总分：</span>
                    <el-text class="mx-1" type="primary">{{
                        dannum * danfen +
                        duonum * duofen +
                        pannum * panfen
                        }}</el-text>
                    <br />
                    <br />
                    <span>及格分：</span>
                    <el-text class="mx-1" type="primary">{{
                        (dannum * danfen + duonum * duofen + pannum * panfen) * 0.6
                        }}</el-text>
                    <br />
                    <br />
                    <span>剩余时间：</span>
                    <br />
                    <el-text style="font-size: xx-large;" type="primary">{{ timere }}</el-text>
                    <br />
                    <br />
                    <el-button type="primary" size='large' @click="submitForm">提交试卷</el-button>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script lang="js" setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import router from '@/router';

const form = reactive({
    dananswerlist: ref([]),
    duoanswerlist: ref([]),
    pananswerlist: ref([]),
})
// 从sessionStorage提取信息
const id = sessionStorage.getItem("id")
const role = sessionStorage.getItem("role")
const user = sessionStorage.getItem("user")
const examBT_isexists = sessionStorage.getItem("examnameBT")
const examname_isexists = sessionStorage.getItem("examname")
// do not use same name with ref
const timere = ref("")
const times = ref(0)
const examname = ref('')
const danquestions = ref([]);
const duoquestions = ref([]);
const panquestions = ref([]);
const examtimelong = ref(null);
// 实现掉线继续答题
// 先检验题库是否存在：
const examresult_isexits = async () => {
    const result = await axios.get(`http://localhost:8000/api/exam/get_exam_useranswer?examname=${examname_isexists}&id=${id}&examBT=${examBT_isexists}`);
    if (result.data['status'] == 201) {
        console.log(result.data)
    }
    // 查看缓存题库有没有试题 // 存在则加载
    if (result.data['status'] == 200) {
        const data = result.data['data']
        const dantemplist = []
        for (let index = 0; index < data[0].length; index++) {
            const element = data[0][index];
            if (element == '') {
                dantemplist.push(ref(null))
                continue
            }
            dantemplist.push(element)
        }
        const duotemplist = []
        for (let index = 0; index < data[1].length; index++) {
            const element = data[1][index];
            if (element.length == 0) {
                duotemplist.push([])
                continue
            }
            duotemplist.push(element)
        }
        const pantemplist = []
        for (let index = 0; index < data[2].length; index++) {
            const element = data[2][index];
            if (element == '') {
                pantemplist.push(null)
                continue
            }
            pantemplist.push(element)
        }
        form.dananswerlist = dantemplist
        form.duoanswerlist = duotemplist
        form.pananswerlist = pantemplist
    }
}
examresult_isexits()

// 获取考试信息
var examdata = []
const dannum = ref(0);
const duonum = ref(0);
const pannum = ref(0);
const danfen = ref(0);
const duofen = ref(0);
const panfen = ref(0);

const get_exam_question = async () => {
    examname.value = sessionStorage.getItem("examname")
    const result = await axios.get(`http://localhost:8000/api/exam/get_exam_questions?examname=${examname.value}`)
    examdata = result.data.data
    dannum.value = examdata.dannum
    duonum.value = examdata.duonum
    pannum.value = examdata.pannum
    danfen.value = examdata.danfen
    duofen.value = examdata.duofen
    panfen.value = examdata.panfen
    danquestions.value = examdata.danquestions
    duoquestions.value = examdata.duoquestions
    panquestions.value = examdata.panquestions
    for (let index = 0; index < danquestions.value.length; index++) {
        form.dananswerlist.push(ref(''))
    }
    examtimelong.value = examdata.examtimelong

    // 
    const examBT1 = new Date(examdata.valuecreatetime)
    const inputTime = examBT1.setMinutes(examBT1.getMinutes() + examtimelong.value)
    // const inputTime = new Date("2024-10-16T00:00:00")
    countDown();
    // 定时器 每隔一秒变化一次
    const tid = setInterval(countDown, 1000);
    function clearI() {
        // 考试退出
        var a = sessionStorage.getItem("examEnd")
        if (a == 1) {
            clearInterval(tid);
            sessionStorage.removeItem("examEnd")
        }
    }
    function countDown() {
        // 获取当前时间的时间戳（单位毫秒）
        var nowTime = new Date();
        // 把剩余时间毫秒数转化为秒
        times.value = (inputTime - nowTime) / 1000;
        if (times.value <= 0) {
            timere.value = "00" + ":" + "00" + ":" + "00";
            sessionStorage.setItem("examEnd", 1)
            setTimeout(clearI, 100)
            return
        }
        // 计算小时数 转化为整数
        var h = parseInt(times.value / 60 / 60);
        // 如果小时数小于10，要变成0 + 数字的形式 赋值给盒子
        h = h < 10 ? "0" + h : h;
        // 计算分钟数 转化为整数
        var m = parseInt((times.value - parseInt(h) * 3600) / 60);
        // 如果分钟数小于10，要变成0 + 数字的形式 赋值给盒子
        m = m < 10 ? "0" + m : m;
        // 计算秒数 转化为整数
        var s = parseInt(times.value % 60);
        // 如果秒钟数小于10，要变成0 + 数字的形式 赋值给盒子
        s = s < 10 ? "0" + s : s;
        // 赋值给 refs
        timere.value = h + ":" + m + ":" + s;
        // 如果剩余时间小于0，结束计时
    }
}
get_exam_question()


const get_user_now_answer = async () => {
    // console.log(form)
    // console.log(examdata)
    // console.log(form.dananswerlist)
    // console.log(form.duoanswerlist)
    // console.log(form.pananswerlist)
    // 提取答案
    var dancurrectanswerList = []
    var duocurrectanswerList = []
    var pancurrectanswerList = []
    // user answer
    var danuseranswer = []
    var duouseranswer = []
    var panuseranswer = []
    // Wrong/Right answer
    var danWRanswer = []
    var duoWRanswer = []
    var panWRanswer = []
    //dan
    for (let index = 0; index < examdata.danquestions.length; index++) {
        dancurrectanswerList.push(examdata.danquestions[index].correctanswer)
        if (form.dananswerlist[index] == examdata.danquestions[index].correctanswer) {
            danuseranswer.push(form.dananswerlist[index])
            danWRanswer.push("Right")
        } else {
            danuseranswer.push(form.dananswerlist[index])
            danWRanswer.push("Wrong")
        }
    }
    // duo
    for (let index = 0; index < examdata.duoquestions.length; index++) {
        duocurrectanswerList.push(examdata.duoquestions[index].correctanswer)
        var duotemp = 0
        for (let index1 = 0; index1 < examdata.duoquestions[index].correctanswer.length; index1++) {
            if (typeof (form.duoanswerlist[index]) == 'undefined') {
                duotemp = 1
                continue
            }
            var CASW = examdata.duoquestions[index].correctanswer[index1]
            if (form.duoanswerlist[index].indexOf(CASW) == -1) {
                duotemp = 1
            }
        }
        if (duotemp == 0) {
            duouseranswer.push(form.duoanswerlist[index])
            duoWRanswer.push("Right")
        } else {
            duouseranswer.push(form.duoanswerlist[index])
            duoWRanswer.push("Wrong")
        }
    }
    // pan
    for (let index = 0; index < examdata.panquestions.length; index++) {
        pancurrectanswerList.push(examdata.panquestions[index].correctanswer)
        if (form.pananswerlist[index] == examdata.panquestions[index].correctanswer) {
            panuseranswer.push(form.pananswerlist[index])
            panWRanswer.push("Right")
        } else {
            panuseranswer.push(form.pananswerlist[index])
            panWRanswer.push("Wrong")
        }
    }
    // console.log(dancurrectanswerList, danuseranswer, danWRanswer)
    // console.log(duocurrectanswerList, duouseranswer, duoWRanswer)
    // console.log(pancurrectanswerList, panuseranswer, panWRanswer)
    return [[dancurrectanswerList, danuseranswer, danWRanswer],
    [duocurrectanswerList, duouseranswer, duoWRanswer],
    [pancurrectanswerList, panuseranswer, panWRanswer]]
}

// 定期保存考生的考试情况
const save_user_answer = async () => {
    var user_now_answer = await get_user_now_answer();
    console.log(user_now_answer)
    var dan_now_answer = []                           //#user_now_answer[0][1]
    var duo_now_answer = []
    var pan_now_answer = []
    for (let index = 0; index < user_now_answer[0][1].length; index++) {
        if (typeof (user_now_answer[0][1][index]) == 'string') {
            dan_now_answer.push(user_now_answer[0][1][index])
            continue
        }
        dan_now_answer.push("")
    }
    for (let index = 0; index < user_now_answer[1][1].length; index++) {
        const element = user_now_answer[1][1][index];
        if (typeof (element) == "undefined") {
            duo_now_answer.push([])
            continue
        }
        var duotemp = []
        for (let index = 0; index < element.length; index++) {
            const el = element[index];
            duotemp.push(el)
        }
        duo_now_answer.push(duotemp)
    }
    for (let index = 0; index < user_now_answer[2][1].length; index++) {
        const element = user_now_answer[2][1][index];
        if (typeof (element) == "undefined") {
            pan_now_answer.push("")
            continue
        }
        pan_now_answer.push(element)
    }
    await axios.post("http://localhost:8000/api/exam/store_exam_useranswer", {
        id: id,
        examname: examname_isexists,
        data: [dan_now_answer, duo_now_answer, pan_now_answer]
    });
}
setTimeout(setInterval(save_user_answer, 900000), 10000)

const submitForm = async () => {
    var user_now_answer = await get_user_now_answer();
    console.log(user_now_answer)
    var user_nowdan_answer = []
    for (let index = 0; index < user_now_answer[0][1].length; index++) {
        const element = user_now_answer[0][1][index];
        if (typeof (element) == 'string') {
            user_nowdan_answer.push(element);
            continue
        }
        user_nowdan_answer.push("");
    }
    var user_nowduo_answer = []
    for (let index = 0; index < user_now_answer[1][1].length; index++) {
        const element = user_now_answer[1][1][index];
        if (typeof (element) == "undefined") {
            user_nowduo_answer.push([]);
            continue
        }
        if (element.length == 0) {
            user_nowduo_answer.push([]);
            continue
        }
        user_nowduo_answer.push(element);
    }
    // var user_nowpan_answer = []
    // for (let index = 0; index < user_now_answer[2][1].length; index++) {
    //     const element = user_now_answer[2][1][index];
    //     if (element==null) {

    //     }
    // }
    // 考试提交
    console.log(examdata)
    const dannum = user_now_answer[0][2].filter(item => item === 'Right').length
    const duonum = user_now_answer[1][2].filter(item => item === 'Right').length
    const pannum = user_now_answer[2][2].filter(item => item === 'Right').length
    const fenshu = dannum * examdata['danfen'] + examdata['duofen'] * duonum + pannum * examdata['panfen']
    await axios.post("http://localhost:8000/api/exam/store_final_exam_result", {
        id: id,
        user: user,
        roleofexamcreater: examdata['role'],
        idofcreater: examdata['id'],
        examBT: examBT_isexists,
        examname: examdata['examname'],
        examtimelong: examdata['examtimelong'],
        createtime: examdata['createtime'],
        qustore: examdata['qustore'],
        tags: examdata['tags'],
        danquestions: examdata['danquestions'],
        duoquestions: examdata['duoquestions'],
        panquestions: examdata['panquestions'],
        danfen: examdata['danfen'],
        duofen: examdata['duofen'],
        panfen: examdata['panfen'],
        dannum: examdata['dannum'],
        duonum: examdata['duonum'],
        pannum: examdata['pannum'],
        dancorrectanswerlist: user_now_answer[0][0],
        duocorrectanswerlist: user_now_answer[1][0],
        pancorrectanswerlist: user_now_answer[1][0],
        dananswerlist: user_nowdan_answer,
        duoanswerlist: user_nowduo_answer,
        pananswerlist: user_now_answer[2][1],
        danWRanswerlist: user_now_answer[0][2],
        duoWRanswerlist: user_now_answer[1][2],
        panWRanswerlist: user_now_answer[2][2],
        fenshu: fenshu,
    })
    router.push({ path: "/exam/examresult" })
}

function scrollToQuestion(questionId) {
    const questionElement = document.getElementById(questionId);
    if (questionElement) {
        questionElement.scrollIntoView({ behavior: 'smooth' });
    }
}
</script>

<style lang="css">
.exampage {
    width: 100vw;
    height: 100vh;
    background-color: white;
    color: #000;
}

.exam-container {
    display: flex;
}

.question-buttons {
    margin-right: 20px;
}

.question-content {
    flex-grow: 1;
}

.question {
    margin-bottom: 20px;
    cursor: pointer;
}
</style>