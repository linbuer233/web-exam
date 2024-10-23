<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">考试成绩</div>
    <el-table :data="tableData" border style="width: 100%;align-items: center;max-height:90%" height="100%">
        <el-table-column type="expand">
            <template #default="props">
                <div style="width:95%;margin-left: 20px;">
                    <h3>考试情况</h3>
                    <el-table :data="props.row.uoer" border>
                        <el-table-column label="姓名" prop="user" />
                        <el-table-column label="学号" prop="id" />
                        <el-table-column label="成绩" prop="onefenshu" />
                        <!-- <el-table-column label="考试次数" prop="user_exam_cishu" /> -->
                    </el-table>
                </div>
            </template>
        </el-table-column>
        <el-table-column prop="examname" label="考试名称" />
        <el-table-column prop="examBT" label="考试开始时间" />
        <el-table-column prop="allfen" label="总分" />
        <el-table-column prop="bestfenshu" label="最佳成绩" />
        <el-table-column prop="examstatus" label="考试状态" />
        <el-table-column prop="roleofexamcreater" label="创建人身份">
            <template #default="scope">
                <el-tag :type="scope.row.roleofexamcreater === 'admin' ? 'primary' : 'success'" disable-transitions>
                    {{ scope.row.roleofexamcreater }}
                </el-tag>
            </template>
        </el-table-column>
        <el-table-column align="right" width="100" label="操作">
            <template #default="scope">
                <center>
                    <el-button v-if="scope.row.roleofexamcreater == 'student'" size="small" type="danger"
                        @click="delExamresult(scope.row)" :icon="Delete" circle></el-button>
                </center>
            </template>
        </el-table-column>
    </el-table>
</template>

<script lang="js" setup>
import { ref } from 'vue';
import axios from 'axios';
import { Delete } from '@element-plus/icons-vue'
import { ElMessage, ElButton } from 'element-plus'

const tableData = ref([])

const get_userown_examresult = async () => {
    const userid = localStorage.getItem('id')
    const result = await axios.get(`http://localhost:8000/api/exam/get_userown_examresult?id=${userid}`)
    const data = result.data["data"]
    for (let index = 0; index < data.length; index++) {
        const element = data[index];
        const examBT = new Date(element.examBT)
        const examBT1 = new Date(element.examBT)
        const nowT = new Date()
        if (nowT < examBT1.setMinutes(examBT1.getMinutes() + element.examtimelong)) {
            if (nowT < examBT) {
                var examstatus = "未开始"
            } else {
                examstatus = "进行中"
            }
        } else {
            examstatus = "已结束"
        }
        tableData.value.push({
            id: element.uid,
            roleofexamcreater: element.roleofexamcreater,
            allfen: element.allfen,
            examBT: element.examBT,
            examname: element.examname,
            bestfenshu: element.fenshu,
            examstatus: examstatus,
            uoer: element.uoer,// user one exam results
        })
    }
}
get_userown_examresult()

const delExamresult = async (scoperow) => {
    await axios.post("http://localhost:8000/api/exam/delete_user_examresult", {
        examname: scoperow.examname
    })
    ElMessage({
        type: 'success',
        message: '删除成功',
    })
    get_userown_examresult()
}
</script>
<style lang="css">
.el-table .cell {
    text-align: center;
}
</style>