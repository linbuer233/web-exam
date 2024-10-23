<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">考试列表</div>
    <el-table :data="filterTableData" border style="width: 100%;align-items: center;max-height:85%" height="100%">
        <el-table-column prop="examname" label="考试名称"><template #header>
                <el-input v-model="search" size="small" placeholder="搜索考试" />
            </template></el-table-column>
        <el-table-column prop="examtype" label="考试类型">
            <template #default="scope">
                <el-tag :type="scope.row.examtype === '管理员创建' ? 'primary' : 'success'" disable-transitions>
                    {{ scope.row.examtype }}
                </el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="exambegintime" label="开始时间" />
        <el-table-column prop="examtimelong" label="考试时长" width="120" />
        <el-table-column prop="fenshu" label="考试总分" width="120" />
        <el-table-column prop="jigeline" label="及格线" width="120" />
        <el-table-column prop="examstatus" label="考试状态" width="120" />
        <el-table-column prop="examCiShu" label="考试次数" width="100" />
        <el-table-column align="right" width="220">
            <template #default="scope">
                <center>
                    <el-button size="small" type="primary" @click="handleExam(scope.$index, scope.row)" plain>
                        开始考试
                    </el-button>
                </center>
            </template>
        </el-table-column>
    </el-table>
    <!-- <el-pagination background layout="prev, pager, next" :total="990" style="padding-top: 20px;" /> -->
</template>

<script lang="js" setup>
import { computed, ref } from 'vue';
import axios from 'axios';
import { ElMessage, ElMessageBox, ElButton } from 'element-plus'
import { useRouter } from 'vue-router'
const router = useRouter();

const handleExam = async (index, row) => {
    if (row.examstatus == '已结束') {
        ElMessage({
            type: 'error',
            message: "考试已经结束",
        })
        return
    }
    if (row.examstatus == '未开始') {
        ElMessage({
            type: 'error',
            message: "考试还未开始",
        })
        return
    }
    const user = localStorage.getItem('user');
    const id = localStorage.getItem('id');
    const role = localStorage.getItem('role');
    // 检查考试了多少次
    const result = await axios.get(`http://localhost:8000/api/exam/get_user_examCishu?examname=${row.examname}&id=${id}&examCishu=${row.examCiShu}`)
    console.log(result)
    if (result.data["status"] == 500) {
        ElMessage({
            type: 'error',
            message: "考试次数已用完",
        })
        return
    }
    sessionStorage.setItem('examname', row.examname);
    sessionStorage.setItem('examnameBT', row.exambegintime);
    sessionStorage.setItem('examtimelong', row.examtimelong);
    sessionStorage.setItem('examallfen', row.fenshu);
    sessionStorage.setItem('role', role);
    sessionStorage.setItem("id", id);
    sessionStorage.setItem('user', user);
    router.push({ path: '/exam/examprepare' })
};

const search = ref('');
var tableData = ref([])
var filterTableData = ref(computed(() =>
    tableData.value.filter(data =>
        !search.value ||
        data.question.toLowerCase().includes(search.value.toLowerCase())
    )
));
const getexaminfo = async () => {
    tableData.value = []
    const userid = localStorage.getItem("id")
    const role = localStorage.getItem("role")
    const user = localStorage.getItem("user")
    const result = await axios.get(`http://localhost:8000/api/exam/get_all_exams?user=${user}&userid=${userid}&role=${role}`)
    // tableData.value = result.data.data
    for (let index = result.data.data.length - 1; index >= 0; index--) {
        const data = result.data.data[index]
        const examBT = new Date(data.valuecreatetime)
        const examBT1 = new Date(data.valuecreatetime)
        const examCT = new Date(data.createtime)
        const nowT = new Date()
        if (nowT < examBT1.setMinutes(examBT1.getMinutes() + data.examtimelong)) {
            if (nowT < examBT) {
                var examstatus = "未开始"
            } else {
                examstatus = "进行中"
            }
        } else {
            examstatus = "已结束"
        }
        const fenshu = data.dannum * data.danfen + data.duonum * data.duofen + data.pannum * data.panfen
        tableData.value.push({
            examname: data.examname,
            exambegintime: examBT.toLocaleString(),
            examendtime: new Date(examBT1.setMinutes(examBT1.getMinutes() + data.examtimelong)).toLocaleString(),
            fenshu: `${fenshu}`,
            jigeline: fenshu * 0.6,
            examstatus: examstatus,
            examtype: data.examtype,
            examtimelong: data.examtimelong + "分钟",
            examCiShu: data.examCiShu,
        })
    }
}
getexaminfo()

// 

</script>
<style lang="css">
.el-table .cell {
    text-align: center;
}
</style>