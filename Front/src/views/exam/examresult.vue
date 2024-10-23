<template>
    <div class="examresultpage">
        <el-card style="height: 100%;width:100%">
            <center><el-button type="primary" size="large" @click="backhome">返回主页面</el-button></center>
            <div style="height:50px;text-align:center;font-size: x-large;">考试成绩: <el-text type="primary"
                    style="font-size: x-large;">{{ fenshu
                    }}分</el-text>
            </div>
            <div>
                <el-scrollbar height="100%" style="width:100%">
                    <div>
                        <h2>一、选择题</h2>
                        <div v-for="(question, index) in danquestions" :key="question.id" :id="question.id"
                            class="question">
                            <el-text tag="b" style="font-size: x-large;">{{ index + 1
                                }}、{{
                                    question.question
                                }} </el-text>
                            <br />
                            <br />
                            <el-row v-for="(qu, idx) in question.options" :value="idx" :key="idx">
                                <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                <el-text style="font-size: large;">{{ qu }}</el-text>
                            </el-row>
                            <br />
                            <div>您的答案：<el-text style="font-size: large;"
                                    :type="danWRanswerlist[index] == 'Right' ? 'primary' : 'danger'">{{
                                        dananswerlist[index]
                                    }}</el-text></div>
                            <div>正确答案：<el-text style="font-size: large;" type="primary">{{ dancorrectanswerlist[index]
                                    }}</el-text></div>
                            <div>解析：{{ question.analysis }}</div>
                        </div>
                        <br />
                        <h2>二、多选题</h2>
                        <div v-for="(question, index) in duoquestions" :key="question.id" :id="question.id"
                            @click="scrollToQuestion(question.id)" class="question">
                            <el-text tag="b" style="font-size: x-large;">{{ index + 1
                                }}、{{
                                    question.question
                                }} </el-text>
                            <br />
                            <br />
                            <el-row v-for="(qu, idx) in question.options" :label="idx" size="large" :key="idx">
                                <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                <el-text style="font-size: large;">{{ qu }}</el-text>
                            </el-row>
                            <br />
                            <div>您的答案：<el-text style="font-size: large;"
                                    :type="duoWRanswerlist[index] == 'Right' ? 'primary' : 'danger'">{{
                                        duoanswerlist[index].toString()
                                    }}</el-text></div>
                            <div>正确答案：<el-text style="font-size: large;" type="primary">{{ question.correctanswer
                                    }}</el-text></div>
                            <div>解析：{{ question.analysis }}</div>
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
                            <el-row v-for="(qu, idx) in question.options" :label="idx" size="large" :key="idx">
                                <el-text style="font-size: large;" type="primary">{{ idx }}、</el-text>
                                <el-text style="font-size: large;">{{ qu }}</el-text>
                            </el-row>
                            <br />
                            <div>您的答案：<el-text style="font-size: large;"
                                    :type="panWRanswerlist[index] == 'Right' ? 'primary' : 'danger'">{{
                                        pananswerlist[index]
                                    }}</el-text></div>
                            <div>正确答案：<el-text style="font-size: large;" type="primary">{{ question.correctanswer
                                    }}</el-text></div>
                            <div>解析：{{ question.analysis }}</div>
                        </div>
                    </div>
                    <center><el-button type="primary" size="large" @click="backhome">返回主页面</el-button></center>
                </el-scrollbar>
            </div>
        </el-card>
    </div>

</template>

<script lang="js" setup>
import axios from 'axios';
import { ref } from 'vue';
import router from '@/router';

const danquestions = ref([]);
const dananswerlist = ref([]);
const dancorrectanswerlist = ref([]);
const danWRanswerlist = ref([]);

const duoquestions = ref([]);
const duoanswerlist = ref([]);
const duoWRanswerlist = ref([]);

const panquestions = ref([]);
const pananswerlist = ref([]);
const panWRanswerlist = ref([]);

const danfen = ref(null)
const duofen = ref(null)
const panfen = ref(null)
const fenshu = ref(null)
// 获取考生考试结果
const get_user_result = async () => {
    const examname = sessionStorage.getItem('examname');
    const id = sessionStorage.getItem('id');
    const result = await axios.get(`http://localhost:8000/api/exam/get_examresult_page_data?examname=${examname}&id=${id}`)
    console.log(result.data);
    danquestions.value = result.data['data'].danquestions;
    dananswerlist.value = result.data['data'].dananswerlist;
    dancorrectanswerlist.value = result.data['data'].dancorrectanswerlist
    danWRanswerlist.value = result.data['data'].danWRanswerlist

    duoquestions.value = result.data['data'].duoquestions;
    duoanswerlist.value = result.data['data'].duoanswerlist;
    duoWRanswerlist.value = result.data['data'].duoWRanswerlist

    panquestions.value = result.data['data'].panquestions;
    pananswerlist.value = result.data['data'].pananswerlist;
    panWRanswerlist.value = result.data['data'].panWRanswerlist

    danfen.value = result.data['data'].danfen
    duofen.value = result.data['data'].duofen
    panfen.value = result.data['data'].panfen
    const dannum = danWRanswerlist.value.filter(item => item === 'Right').length
    const duonum = duoWRanswerlist.value.filter(item => item === 'Right').length
    const pannum = panWRanswerlist.value.filter(item => item === 'Right').length
    fenshu.value = dannum * danfen.value + duofen.value * duonum + pannum * panfen.value
}
get_user_result()

const backhome = () => {
    const role = sessionStorage.getItem('role')
    if (role == 'admin') {
        router.push({ path: "/adminMainpage/home" })
        sessionStorage.setItem("currpageurl", '1')
    } else {
        router.push({ path: "/studentMainpage/home" })
        sessionStorage.setItem("currpageurl", '1')
    }
}
</script>

<style lang="css">
.examresultpage {
    align-items: center;
    height: 100%;
    width: 99vw;
    background-color: #f2f2f2;
    font-family: Arial, sans-serif;
    color: #333;
}
</style>