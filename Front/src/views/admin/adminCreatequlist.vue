<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">创建试题</div>
    <el-row :gutter="150" style="width: 100%;">
        <el-col :span="2">
            <el-button size="small" type="primary" @click="toaddquestion" style="margin-bottom: 10px;height:30px">
                <el-icon>
                    <Plus />
                </el-icon>
                <span>新增试题</span>
            </el-button>
        </el-col>
        <el-col :span="2">
            <el-select v-model="value" placeholder="全部题型" style="width: 140px;margin-top:-1px;height:30px"
                @change="updatequestionlist">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
        </el-col>
        <el-col :span="2">
            <el-select v-model="valuetag" placeholder="全部标签" style="width: 140px;margin-top:-1px;height:30px"
                @change="updatequestionlist">
                <el-option v-for="item in optionstag" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
        </el-col>
        <el-col :span="2">
            <el-select v-model="valuestore" placeholder="全部题库" style="width: 140px;margin-top:-1px;height:30px"
                @change="updatequestionlist">
                <el-option v-for="item in optionsqustore" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
        </el-col>
        <el-col :span="2">
            <el-input v-model="search" size="small" placeholder="搜索试题" style="width: 240px;height:30px" />
        </el-col>
    </el-row>
    <!-- <span style="margin-bottom: 5px;"></span> -->
    <el-table :data="filterTableData" border style="width: 100%;align-items: center;max-height:80%" height="100%">
        <el-table-column type="expand">
            <template #default="props">
                <el-descriptions column=2 border>

                    <el-descriptions-item :width="240" rowspan="1" label="题干" label-align="center" align="center">{{
                        props.row.question
                        }}</el-descriptions-item>
                    <el-descriptions-item rowspan="3" label="选项" label-align="center" align="center">
                        <el-row v-for="(i, j) in props.row.options" :key="i">
                            <el-col>
                                <span style="font-weight: bolder;color:blue">{{ j }}、</span>{{ i }}
                            </el-col>
                        </el-row>
                    </el-descriptions-item>
                    <el-descriptions-item rowspan="1" label="正确答案" label-align="center" align="left">
                        <p style="color: red;">{{
                            props.row.correctanswer
                            }}</p>
                    </el-descriptions-item>

                    <el-descriptions-item rowspan="1" label="解析" label-align="center" align="left">{{ props.row.analysis
                        }}</el-descriptions-item>
                </el-descriptions>
            </template>
        </el-table-column>
        <el-table-column prop="qutype" label="题型" width="80" />
        <el-table-column prop="id" label="编号" width="80" />
        <el-table-column prop="tag" label="标签" width="80" />
        <el-table-column prop="qustore" label="所属题库" width="120" />
        <el-table-column prop="question" label="题干" />
        <el-table-column prop="correctanswer" label="正确答案" width="80" />
        <el-table-column align="right" width="120" label="操作">
            <template #default="scope">
                <el-button type="primary" :icon="Edit" @click="drawervisible = true; getCurrentRow(scope.row)" circle />
                <el-button type="danger" :icon="Delete" @click="delete_question(scope.row)" circle />
            </template>
        </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="currentPage" background layout=" prev, pager, next" :total="qulength"
        style="padding-top: 20px;" @change="pagechange" />
    <!--  -->
    <el-drawer v-model="drawervisible" :show-close="false">
        <template #header="{ close, titleId, titleClass }">
            <h4 :id="titleId" :class="titleClass">修改题目</h4>
            <el-button type="danger" @click="get_questions(); close()">
                <el-icon class="el-icon--left">
                    <CircleCloseFilled />
                </el-icon>
                保存退出
            </el-button>
        </template>
        <question_single :msg="msgquestion" :key="question_singlekey" />
    </el-drawer>
</template>

<script lang="js" setup>
import axios from 'axios';
import { computed, ref } from 'vue';
import {
    Plus,
    Delete,
    Edit,
    CircleCloseFilled,
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElButton, ElDrawer } from 'element-plus'
import question_single from '@/components/Question_single.vue';
const router = useRouter();
const question_singlekey = ref(0)
const drawervisible = ref(false)
var msgquestion = ref({})
const getCurrentRow = (scoperow) => {
    console.log("当前传值", scoperow)
    msgquestion.value = scoperow
    console.log(msgquestion)
    question_singlekey.value += 1
};

const delete_question = (scoperow) => {
    console.log(scoperow)
    console.log(scoperow.uid)
    ElMessageBox.confirm('确认删除?', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        var token = localStorage.getItem('Authorization')
        await axios.post('http://localhost:8000/api/question/delete_question', { id: scoperow.uid, token: token })
        ElMessage({
            type: 'success',
            message: '删除成功',
        })
        get_questions()
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '取消删除',
        })
    })
}


const value = ref('全部题型')
const options = [
    {
        value: '全部题型',
        label: '全部题型',
    },
    {
        value: '选择题',
        label: '选择题',
    },
    {
        value: '多选题',
        label: '多选题',
    },
    {
        value: '判断题',
        label: '判断题',
    },
]
// 获取标签和题库信息
const valuetag = ref('全部标签')
const valuestore = ref('全部题库')
const optionsqustore = [{ value: "全部题库", label: "全部题库" }];
const optionstag = [{ value: "全部标签", label: "全部标签" }];
const getqutagandstore = async () => {
    try {
        const res = await axios.get('http://localhost:8000/api/question/get_questionstore_info');
        const data = res.data
        console.log(data)
        // 处理数据
        for (let index = 0; index < data.qustore.length; index++) {
            optionsqustore.push({ value: data.qustore[index], label: data.qustore[index] });
        }
        for (let index = 0; index < data.tag.length; index++) {
            optionstag.push({ value: data.tag[index], label: data.tag[index] });
        }
    } catch (error) {
        console.error(error);
    }
}
getqutagandstore()

const toaddquestion = () => {
    router.push('/adminMainpage/addquestion/pi')
}
// 定义对象的结构
const search = ref('');
var tableData = ref([])
var filterTableData = ref(computed(() =>
    tableData.value.filter(data =>
        !search.value ||
        data.question.toLowerCase().includes(search.value.toLowerCase())
    )
));
var currentPage = ref(1)
var startindex = ref(0)
var qulength = ref(10)
// 初始化表格数据
const get_questions = async () => {
    tableData.value = []
    startindex.value = (currentPage.value - 1) * 10
    const res = await axios.get(`http://localhost:8000/api/question/get_questions?qustore=${valuestore.value}&qutag=${valuetag.value}&tix=${value.value}&start=${startindex.value}`);
    var dataqu = res.data.data;
    const tixing = ['选择题', '多选题', '判断题']
    for (let index = 0; index < dataqu.length; index++) {
        const temp = dataqu[index]
        const qutype = tixing[parseInt(temp['qutype'])]
        tableData.value.push(
            {
                id: index + 1 + startindex.value,
                uid: temp.id,
                qutype: qutype,
                question: temp.question,
                tag: temp.tag,
                qustore: temp.qustore,
                correctanswer: temp.correctanswer,
                analysis: temp.analysis,
                options: temp.options,
                question_images: temp.question_images,
                answer_images: temp.answer_images
            }
        )
    }
    qulength.value = res.data.qulength
}
get_questions()

const updatequestionlist = () => {
    get_questions()
}
const pagechange = () => {
    get_questions()
}
</script>