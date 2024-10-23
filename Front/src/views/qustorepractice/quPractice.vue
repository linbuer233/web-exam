<template>
    <div class="qupractice">
        <div>
            <el-row>
                <el-col :span="3">
                </el-col>
                <el-col :span="1">
                    <el-button type="primary" style="position: absolute;top:8px" @click="backhome">返回主页</el-button>
                </el-col>
                <el-col :span="16">
                    <center><el-text type="primary" style="font-size:30px">{{ nowPositon + 1 }}/{{ allquestionnum
                            }}</el-text>
                    </center>
                </el-col>
                <el-col :span="1">
                    <el-button type="primary" style="position: absolute;top:8px" @click="showDTcard">答题卡</el-button>
                </el-col>
                <el-col :span="3">
                </el-col>
            </el-row>
        </div>
        <div class="questiondiv">
            <el-card class="question">
                <el-text tag="b" style="font-size: x-large;">{{ tigan }} </el-text>
                <br />
                <br />
                <!-- 单选 -->
                <div v-if="qutype == '0'">
                    <div v-if="typeof (quradio) == 'object'">
                        <div v-for="(qu, idx) in options" :key="idx">
                            <el-radio v-model="quradio" :value="idx" :key="idx">
                                <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                <el-text style="font-size: large;">{{ qu }}</el-text>
                            </el-radio>
                        </div>
                    </div>
                    <div v-else>
                        <div v-for="(qu, idx) in options" :key="idx">
                            <el-radio v-model="quradio" :value="idx" :key="idx" disabled>
                                <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                <el-text style="font-size: large;">{{ qu }}</el-text>
                            </el-radio>
                        </div>
                        <br />
                        <el-text style="font-size:20px">你的选项： <el-text style="font-size:20px"
                                :type="quradio == correctanswer ? 'primary' : 'danger'">{{ quradio }}</el-text>
                        </el-text>
                        <br />
                        <el-text style="font-size:20px">正确选项： <el-text style="font-size:20px" type="primary">{{
                            correctanswer
                                }}</el-text>
                        </el-text>
                        <br />
                        <el-text style="font-size:20px">解析： <el-text style="font-size:20px" type="warning">{{ analysis
                                }}</el-text>
                        </el-text>
                    </div>
                </div>
                <!-- 多选 -->
                <div v-else-if="qutype == '1'">
                    <div v-if="quduostatus == 0">
                        <div v-for="(qu, idx) in options" :key="idx">
                            <el-checkbox-group v-model="quduo">
                                <el-checkbox :label="idx" size="large" :key="idx">
                                    <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                    <el-text style="font-size: large;">{{ qu }}</el-text>
                                </el-checkbox>
                            </el-checkbox-group>
                        </div>
                        <el-button type="primary" @click="completeduo">提交</el-button>
                    </div>
                    <div v-else>
                        <div v-for="(qu, idx) in options" :key="idx">
                            <el-checkbox-group v-model="quduo" disabled>
                                <el-checkbox :label="idx" size="large" :key="idx">
                                    <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                    <el-text style="font-size: large;">{{ qu }}</el-text>
                                </el-checkbox>
                            </el-checkbox-group>
                        </div>
                        <br />
                        <el-text style="font-size:20px">你的选项： <el-text style="font-size:20px"
                                :type="quduoWR == 0 ? 'primary' : 'danger'">{{ quduofinalsel }}</el-text>
                        </el-text>
                        <br />
                        <el-text style="font-size:20px">正确选项： <el-text style="font-size:20px" type="primary">{{
                            correctanswer
                                }}</el-text>
                        </el-text>
                        <br />
                        <el-text style="font-size:20px">解析： <el-text style="font-size:20px" type="warning">{{ analysis
                                }}</el-text>
                        </el-text>
                    </div>
                </div>
                <!-- 判断 -->
                <div v-else-if="qutype == '2'">
                    <div v-if="typeof (qupan) == 'object'">
                        <div v-for="(qu, idx) in options" :key="idx">
                            <el-radio v-model="qupan" :value="idx" :key="idx">
                                <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                <el-text style="font-size: large;">{{ qu }}</el-text>
                            </el-radio>
                        </div>
                    </div>
                    <div v-else>
                        <div v-for="(qu, idx) in options" :key="idx">
                            <el-radio v-model="qupan" :value="idx" :key="idx" disabled>
                                <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                <el-text style="font-size: large;">{{ qu }}</el-text>
                            </el-radio>
                        </div>
                        <br />
                        <el-text style="font-size:20px">你的选项： <el-text style="font-size:20px"
                                :type="qupan == correctanswer ? 'primary' : 'danger'">{{ qupan }}</el-text>
                        </el-text>
                        <br />
                        <el-text style="font-size:20px">正确选项： <el-text style="font-size:20px" type="primary">{{
                            correctanswer
                                }}</el-text>
                        </el-text>
                        <br />
                        <el-text style="font-size:20px">解析： <el-text style="font-size:20px" type="warning">{{ analysis
                                }}</el-text>
                        </el-text>
                    </div>
                </div>
                <!-- footer 按钮 -->
                <el-row>
                    <el-col :span="10"> </el-col>
                    <el-col :span="8">
                        <el-button-group>
                            <el-button type="primary" :icon="ArrowLeft" @click="prequ">上一题</el-button>
                            <el-button type="primary" @click="nextqu">
                                下一题
                                <el-icon class="el-icon--right">
                                    <ArrowRight />
                                </el-icon>
                            </el-button>
                        </el-button-group>
                    </el-col>
                    <el-col :span="6"> </el-col>
                </el-row>
            </el-card>
        </div>
        <el-drawer v-model="drawer_visible" :show-close="false">
            <template #header="{ close, titleId, titleClass }">
                <h4 :id="titleId" :class="titleClass">答题卡</h4>
                <el-button type="danger" @click="close">
                    <el-icon class="el-icon--left">
                        <CircleCloseFilled />
                    </el-icon>
                    关闭
                </el-button>
            </template>
            <el-scrollbar height="80vh" style="margin: 0px;padding:0px">
                <div>
                    <el-row>
                        <el-text class="mx-1" size="large" type="info">一、选择题</el-text>
                        <div style="width: 100%;padding:0px;margin: 10px;margin-right: 0px;">
                            <el-button style="margin: 4px;" v-for="(i, quid, index) in danuserstatus" :key="quid"
                                :type="quseltype[i]" @click="scrollToQuestion(quid)" circle>
                                {{ index + 1 }}
                            </el-button>
                        </div>
                    </el-row>
                    <br />
                    <el-row>
                        <el-text class="mx-1" size="large" type="info">二、多选题</el-text>
                        <div style="width: 100%;padding:0px;margin: 10px;margin-right: 0px;">
                            <el-button style="margin: 4px;" v-for="(i, quid, index) in duouserstatus" :key="quid"
                                :type="quseltype[i]" @click="scrollToQuestion(quid)" circle>
                                {{ dannum + index + 1 }}
                            </el-button>
                        </div>
                    </el-row>
                    <br />
                    <el-row>
                        <el-text class="mx-1" size="large" type="info">三、判断题</el-text>
                        <div style="width: 100%;padding:0px;margin: 10px;margin-right: 0px;">
                            <el-button style="margin: 4px;" v-for="(i, quid, index) in panuserstatus" :key="quid"
                                :type="quseltype[i]" @click="scrollToQuestion(quid)" circle>
                                {{ dannum + duonum + index + 1 }}
                            </el-button>
                        </div>
                    </el-row>
                </div>
            </el-scrollbar>
        </el-drawer>
    </div>
</template>
<script lang="js" setup>
import {
    ArrowLeft,
    ArrowRight,
} from '@element-plus/icons-vue'
import { ref } from 'vue';
import axios from 'axios';
import { ElButton, ElDrawer } from 'element-plus'
import { CircleCloseFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
const router = useRouter();

var nowPositon = ref(0)
var allquestionnum = ref(1)
var allquesidlist = ref([])

var danuserstatus = ref({})
var duouserstatus = ref({})
var panuserstatus = ref({})

var danusersel = ref({})
var duousersel = ref({})
var panusersel = ref({})

// 题目信息
var qutype = ref(null)
var tigan = ref(null)
var options = ref(null)
var analysis = ref(null)
var correctanswer = ref(null)
var dannum = ref(0)
var duonum = ref(0)

// quseltype
const quseltype = ref({ 0: 'null', 1: 'primary', 2: 'danger' })
// qutype选项
var quradio = ref(null)
var qupan = ref(null)
// duo
var quduo = ref([])
var quduofinalsel = ref('')
var quduoWR = ref(1)
var quduostatus = ref(0)
// TODO: pic 

// 获取题库试题id
const get_SunXunpractice_data = async () => {
    const quPraId = sessionStorage.getItem("qupracticeid");
    const quPraQustorename = sessionStorage.getItem("qupracticequstorename");
    const result = await axios.get(`http://localhost:8000/api/qustore/get_SunXunpractice_data?qustorename=${quPraQustorename}&id=${quPraId}`);
    const data = result.data;
    //
    allquesidlist.value = data['danquidlist'].concat(data['duoquidlist']).concat(data['panquidlist'])
    danuserstatus.value = data['danuserstatus']
    duouserstatus.value = data['duouserstatus']
    panuserstatus.value = data['panuserstatus']
    danusersel.value = data['danusersel'];
    duousersel.value = data['duousersel'];
    panusersel.value = data['panusersel'];
    dannum.value = data['danquidlist'].length;
    duonum.value = data['duoquidlist'].length;
    // 获取题库长度
    allquestionnum.value = allquesidlist.value.length
    // 获取当前做到哪里
    const pratype = sessionStorage.getItem("qupracticeType")
    nowPositon.value = data['nowPosition']
    if (pratype == "Random") {
        nowPositon.value = Math.floor((Math.random() * allquesidlist.value.length));
    }
    // nowPositon.value = 96
    const nowquid = allquesidlist.value[nowPositon.value]
    get_one_question(nowquid)
}
get_SunXunpractice_data()

const get_one_question = async (quid) => {
    const result = await axios.get(`http://localhost:8000/api/qustore/get_onequ_data?quid=${quid}`)
    // 获取题目信息
    // quradio.value = null // 重置 radio 值
    qutype.value = result.data.data.qutype
    tigan.value = result.data.data.question
    options.value = result.data.data.options
    correctanswer.value = result.data.data.correctanswer
    analysis.value = result.data.data.analysis
    // 获取考生的做这道题的状态
    const quPraId = sessionStorage.getItem("qupracticeid");
    const quPraQustorename = sessionStorage.getItem("qupracticequstorename");
    const result1 = await axios.get(`http://localhost:8000/api/qustore/get_user_answer_status?qustorename=${quPraQustorename}&id=${quPraId}&nowquid=${quid}`)
    const user_status = result1.data['user_answer_status']
    const user_sel = result1.data['user_sel']
    if (qutype.value == '0') {
        if (user_status == '0') {
            quradio.value = null
        }
        else {
            quradio.value = user_sel
        }
    }
    if (qutype.value == '1') {
        if (user_status == 0) {
            console.log(user_status)
        } else {
            quduo.value = user_sel.split(',')
        }
        quduostatus.value = user_status
        quduofinalsel.value = user_sel
        var count = 0
        for (let index = 0; index < quduo.value.length; index++) {
            const element = correctanswer.value[index];
            if (quduo.value.indexOf(element) != -1) {
                count += 1
            }
        }
        if (count == quduo.value.length) {
            quduoWR.value = 0
        }
        if (quduo.value.length == 0) {
            quduoWR.value = 1
        }
    }
    if (qutype.value == '2') {
        if (user_status == '0') {
            qupan.value = null
        }
        else {
            qupan.value = user_sel
        }
    }
}

const prequ = () => {
    if (nowPositon.value <= 0) {
        return
    }
    // 试题选项清空 根据做题情况
    var nowquid = allquesidlist.value[nowPositon.value]
    store_user_answer_status(nowquid, nowPositon.value)
    nowPositon.value -= 1
    nowquid = allquesidlist.value[nowPositon.value]
    get_one_question(nowquid)
}
const nextqu = async () => {
    if (nowPositon.value >= allquesidlist.value.length - 1) {
        return
    }
    var nowquid = allquesidlist.value[nowPositon.value]
    store_user_answer_status(nowquid, nowPositon.value)
    nowPositon.value += 1
    nowquid = allquesidlist.value[nowPositon.value]
    get_one_question(nowquid)
}
// TODO: 实现题目做错之后往错题本存题
const store_user_answer_status = async (nowquid, nowPosition) => {
    const quPraId = sessionStorage.getItem("qupracticeid");
    const quPraQustorename = sessionStorage.getItem("qupracticequstorename");
    var qustatus = 0
    var postanswer = 'dsa'
    if (qutype.value == '0') {
        danusersel.value[nowquid] = quradio.value
        postanswer = quradio.value
        if (postanswer != null && postanswer != "dsa" && typeof (postanswer[0]) != 'undefined') {
            if (quradio.value == correctanswer.value) {
                danuserstatus.value[nowquid] = 1
            } else {
                danuserstatus.value[nowquid] = 2
            }
            qustatus = danuserstatus.value[nowquid]
        }
    }
    if (qutype.value == '1') {
        duousersel.value[nowquid] = quduofinalsel.value
        postanswer = quduofinalsel.value
        if (postanswer != null && postanswer != "dsa" && typeof (postanswer[0]) != 'undefined') {
            var count = 0
            for (let index = 0; index < quduo.value.length; index++) {
                const element = correctanswer.value[index];
                if (quduo.value.indexOf(element) != -1) {
                    count += 1
                }
            }
            if (count == quduo.value.length) {
                duouserstatus.value[nowquid] = 1
            }
            if (count != quduo.value.length) {
                duouserstatus.value[nowquid] = 2
            }
            if (quduo.value.length == 0) {
                duouserstatus.value[nowquid] = 2
            }
            console.log('count: ', count)
            console.log(duouserstatus.value[nowquid])
            qustatus = duouserstatus.value[nowquid]
        }
        quduo.value = []
        quduofinalsel.value = ''
    }
    if (qutype.value == '2') {
        panusersel.value[nowquid] = qupan.value
        postanswer = qupan.value
        if (postanswer != null && postanswer != "dsa" && typeof (postanswer[0]) != 'undefined') {
            if (quradio.value == correctanswer.value) {
                panuserstatus.value[nowquid] = 1
            } else {
                panuserstatus.value[nowquid] = 2
            }
            qustatus = panuserstatus.value[nowquid]
        }
    }
    if (postanswer != 'dsa' && postanswer != null && typeof (postanswer[0]) != 'undefined') {
        await axios.post(`http://localhost:8000/api/qustore/store_user_answer_status?qustorename=${quPraQustorename}&id=${quPraId}&nowquid=${nowquid}&user_answer_status=${qustatus}&user_sel=${postanswer}&nowPosition=${nowPosition}`)
    } else {
        quduostatus.value = 0
    }
}

// 多选题按钮，点击判断考生是否选择正确
const completeduo = () => {
    quduostatus.value = 1
    quduofinalsel.value = quduo.value.toString()
    var count = 0
    for (let index = 0; index < quduo.value.length; index++) {
        const element = correctanswer.value[index];
        if (quduo.value.indexOf(element) != -1) {
            count += 1
        }
    }
    if (count == quduo.value.length) {
        quduoWR.value = 0
    }
    if (quduo.value.length == 0) {
        quduoWR.value = 1
    }
}

// backhome
const backhome = () => {
    sessionStorage.removeItem("qupracticeid");
    sessionStorage.removeItem("qupracticequstorename");
    router.push('/studentMainpage/questionstore')
}

// opendrawer
const drawer_visible = ref(false)
const showDTcard = () => {
    drawer_visible.value = true;
}

const scrollToQuestion = (quid) => {
    nowPositon.value = allquesidlist.value.indexOf(quid)
    get_one_question(quid)
    drawer_visible.value = false;
}
</script>
<style lang="css">
.qupractice {
    width: 100vw;
    height: 100vh;
    background-color: white;
    color: #000;
}

.questiondiv {
    display: flex;
    justify-content: center;
    align-items: center;
}

.question {
    width: 80%;
}
</style>