<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">考试成绩</div>
    <el-table :data="tableData" border style="width: 100%;align-items: center;max-height:90%" height="100%">
        <el-table-column type="expand">
            <template #default="props">
                <div style="width:95%;margin-left: 20px;">
                    <h3>考生名单</h3>
                    <el-table :data="props.row.uoer" border>
                        <el-table-column label="姓名" prop="user" />
                        <el-table-column label="学号" prop="id" />
                        <el-table-column label="最佳成绩" prop="fenshu" />
                        <el-table-column label="考试次数" prop="user_exam_cishu" />
                    </el-table>
                </div>
            </template>
        </el-table-column>
        <el-table-column prop="examname" label="考试名称" />
        <el-table-column prop="examBT" label="考试开始时间" />
        <el-table-column prop="allfen" label="总分" />
        <el-table-column prop="completeexampeople" label="已完成考试人数" />
        <el-table-column prop="examstatus" label="考试状态" />
        <el-table-column align="right" width="80" label="操作">
            <template #default="scope">
                <center>
                    <el-button size="small" type="danger" @click="delExamresult(scope.row)" :icon="Delete"
                        circle></el-button>
                </center>
            </template>
        </el-table-column>
    </el-table>
    <!-- <el-pagination background layout="prev, pager, next" :total="990" style="padding-top: 20px;" /> -->
</template>

<script lang="js" setup>
import { ref } from 'vue';
import axios from 'axios';
import { Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
// const childBorder = ref(false)
// 定义用户对象的结构
const tableData = ref([])

const get_user_examresult = async () => {
    const result = await axios.get("http://localhost:8000/api/exam/get_user_examresult")
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
            allfen: element.allfen,
            examBT: element.examBT,
            examname: element.examname,
            completeexampeople: element.examcompeletenum,
            examstatus: examstatus,
            uoer: element.uoer,// user one exam results
        })
    }
}
get_user_examresult()

const delExamresult = async (scoperow) => {
    await axios.post("http://localhost:8000/api/exam/delete_user_examresult", {
        examname: scoperow.examname
    })
    ElMessage({
        type: 'success',
        message: '删除成功',
    })
}

</script>
<style lang="css">
.el-table .cell {
    text-align: center;
}
</style>