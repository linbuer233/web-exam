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
                    <center>
                        <el-text type="deafult" style="font-size:30px"> 错题本 </el-text>
                        <!-- <el-text type="primary" style="font-size:30px">{{ start_index + 1 }}/{{ allWrongqulength
                            }}</el-text> -->
                    </center>
                </el-col>
                <el-col :span="1">
                    <!-- <el-button type="primary" style="position: absolute;top:8px" @click="showDTcard">答题卡</el-button> -->
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
                    <el-col :span="11"> </el-col>
                    <el-col :span="8">
                        <el-button-group>
                            <!-- <el-button type="primary" :icon="ArrowLeft" @click="prequ">上一题</el-button> -->
                            <el-button v-if="start_index < allWrongqulength - 1" type="primary" @click="nextqu">
                                下一题
                                <el-icon class="el-icon--right">
                                    <ArrowRight />
                                </el-icon>
                            </el-button>
                            <el-button v-else type="primary" @click="nextqu">
                                从头开始
                            </el-button>
                        </el-button-group>
                    </el-col>
                    <el-col :span="5"> </el-col>
                </el-row>
            </el-card>
        </div>
    </div>
</template>

<script lang="js" setup>
import {
    ArrowRight,
} from '@element-plus/icons-vue'
import { ref } from 'vue';
import axios from 'axios';
import { ElButton } from 'element-plus'
import { useRouter } from 'vue-router'
const router = useRouter();

// 题目信息
var qutype = ref(null)
var tigan = ref(null)
var options = ref(null)
var analysis = ref(null)
var correctanswer = ref(null)
var quid = ref("")
// qutype选项
var quradio = ref(null)
var qupan = ref(null)
// duo
var quduo = ref([])
var quduofinalsel = ref('')
var quduoWR = ref(1)
var quduostatus = ref(0)
const start_index = ref(0)
const allWrongqulength = ref(0)
const get_wrongqu = async () => {
    const userid = localStorage.getItem("id")
    const res = await axios.get(`http://localhost:8000/api/get_user_wrongquestions?id=${userid}&start=${start_index.value}&limit=${"False"}`);
    allWrongqulength.value = res.data.length
    qutype.value = res.data.data[0].qutype
    tigan.value = res.data.data[0].question.question
    options.value = res.data.data[0].question.options
    analysis.value = res.data.data[0].question.analysis
    correctanswer.value = res.data.data[0].question.correctanswer
    quid.value = res.data.data[0].quid
}
get_wrongqu()

const nextqu = async () => {
    if (start_index.value >= allWrongqulength.value - 1) {
        start_index.value = -1
    }
    var qustatus = 0
    if (qutype.value == "0") {
        // console.log(quradio.value)
        // console.log(correctanswer.value)
        if (quradio.value == correctanswer.value) {
            qustatus = 1
        }
    }
    if (qutype.value == "1") {
        // console.log(quduo.value)
        // console.log(correctanswer.value)
        var count = 0
        for (let index = 0; index < quduo.value.length; index++) {
            const element = correctanswer.value[index];
            if (quduo.value.indexOf(element) != -1) {
                count += 1
            }
        }
        if (count == quduo.value.length) {
            qustatus = 1
        }
        if (count != quduo.value.length) {
            qustatus = 0
        }
        if (quduo.value.length == 0) {
            qustatus = 0
        }
    }
    if (qutype.value == "2") {
        // console.log(qupan.value)
        // console.log(correctanswer.value)
        if (qupan.value == correctanswer.value) {
            qustatus = 1
        }
    }
    start_index.value += 1
    // 如果选择正确就删除错题库的
    if (qustatus == 1) {
        const userid = localStorage.getItem("id")
        await axios.post(`http://localhost:8000/api/delete_user_wrongquestions?id=${userid}&quid=${quid.value}`)
        start_index.value = 0
    }
    quradio.value = null
    quduo.value = []
    qupan.value = null
    quduostatus.value = 0
    get_wrongqu()
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

const backhome = () => {
    router.push({ path: '/studentMainpage/wrongquestion' })
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