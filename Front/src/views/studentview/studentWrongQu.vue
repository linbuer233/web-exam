<template>
    <div style="height: 80vh;">
        <div data-v-106c86ed="" class="title" style="padding-top: 0px;">错题库</div>
        <div><el-button type="primary" @click="WrongquPractice">错题本练习</el-button>
            <el-button type="danger" @click="delete_alluser_wrong_question">清空错题本</el-button>
        </div>
        <el-table :data="tableData" style="width: 100%;align-items: center;max-height:85%" height="100%">
            <el-table-column prop="name" label="错题列表">
                <template #default="scope">
                    <el-descriptions direction="vertical" border column=2>
                        <el-descriptions-item width="40%" label="题干" align="center">
                            <template #label>
                                <div class="cell-item">
                                    <el-icon :style="iconStyle">
                                        <tickets />
                                    </el-icon>
                                    题干
                                </div>
                            </template>
                            {{ scope.row.quname }}
                        </el-descriptions-item>
                        <el-descriptions-item width="60%" label="选项
                    " align="center">
                            <template #label>
                                <div class="cell-item">
                                    <el-icon :style="iconStyle">
                                        <Grid />
                                    </el-icon>
                                    选项
                                </div>
                            </template>
                            <p v-for="(qu, idx) in scope.row.selectlist" :key="idx" class="text item">{{ idx + '、'
                                }}{{ qu }}</p>
                        </el-descriptions-item>
                        <el-descriptions-item label="你的选项/正确选项" align="center">
                            <template #label>
                                <div class="cell-item">
                                    <el-icon :style="iconStyle">
                                        <InfoFilled />
                                    </el-icon>
                                    你的选项/正确选项
                                </div>
                            </template>
                            <span style="color: red;">{{ scope.row.selectanswer }}</span>
                            <span>/</span>
                            <span style="color: green;">{{ scope.row.correctanswer }}</span>
                        </el-descriptions-item>
                        <el-descriptions-item label="解析" align="center">
                            <template #label>
                                <div class="cell-item">
                                    <el-icon :style="iconStyle">
                                        <QuestionFilled />
                                    </el-icon>
                                    解析
                                </div>
                            </template>
                            {{ scope.row.analysis }}
                        </el-descriptions-item>
                    </el-descriptions>
                </template>
            </el-table-column>
            <el-table-column prop="dosomething" label="操作" width="100">
                <template #default="scope">
                    <el-button type="danger" :icon="Delete" @click="delete_wrong_question(scope.row)" circle />
                </template>
            </el-table-column>
        </el-table>
        <el-pagination v-model:current-page="currentPage" background layout="prev, pager, next" :total="lengthtotal"
            style="padding-top: 20px;" @change="pagechange" />
    </div>
</template>
<script lang="js" setup>
import { ref } from 'vue';
import {
    QuestionFilled,
    Grid,
    Delete,
    Tickets,
    InfoFilled,
} from '@element-plus/icons-vue'
import axios from 'axios';
import { ElMessage, ElMessageBox, ElButton } from 'element-plus'
import { useRouter } from 'vue-router'
const router = useRouter();

const lengthtotal = ref(10)
var currentPage = ref(1)
var startindex = ref(0)
const tableData = ref([])
const get_user_wrongquestions = async () => {
    tableData.value = []
    //id: str, start: int, limit: str
    const id = localStorage.getItem("id");
    startindex.value = (currentPage.value - 1) * 10;
    const limit = "True";
    const result = await axios.get(`http://localhost:8000/api/get_user_wrongquestions?id=${id}&start=${startindex.value}&limit=${limit}`)
    const data = result.data.data
    for (let index = 0; index < data.length; index++) {
        const element = data[index];
        var selectanswer = ''
        if (element['qutype'] == '1') {
            selectanswer = element['useranswer'].toString()
        } else {
            selectanswer = element['useranswer']
        }
        tableData.value.push({
            uid: element["id"],
            quid: element['quid'],
            quname: element['question']['question'],
            selectlist: element['question']['options'],
            selectanswer: selectanswer,
            correctanswer: element['question']['correctanswer'],
            analysis: element['question']['analysis'],
        })
    }
    lengthtotal.value = result.data.length
}
get_user_wrongquestions();

const pagechange = () => {
    get_user_wrongquestions();
}

const delete_wrong_question = async (scoperow) => {
    console.log(scoperow)
    await axios.post(`http://localhost:8000/api/delete_user_wrongquestions?id=${scoperow.uid}&quid=${scoperow.quid}`)
    ElMessage({
        type: 'success',
        message: '删除成功',
    })
    get_user_wrongquestions();
}
const delete_alluser_wrong_question = () => {
    ElMessageBox.confirm('确认删除?', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        const uid = localStorage.getItem('id')
        await axios.post(`http://localhost:8000/api/delete_alluser_wrong_question?id=${uid}`)
        ElMessage({
            type: 'success',
            message: '删除成功',
        })
        get_user_wrongquestions();
    })
}
const WrongquPractice = () => {
    router.push({ path: '/wrongqu/wrongqustorepractice' });
}
</script>
<style lang="css">
.el-table .cell {
    text-align: center;
}
</style>