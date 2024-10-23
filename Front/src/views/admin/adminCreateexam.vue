<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">发起考试</div>
    <el-button size="small" type="primary" @click="toaddexam" style="margin-bottom: 10px;height:30px">
        <el-icon>
            <Plus />
        </el-icon>
        <span>新增考试</span>
    </el-button>
    <el-table :data="filterTableData" border style="width: 100%;align-items: center;max-height:85%" height="100%">
        <el-table-column prop="examname" label="搜索考试">
            <template #header>
                <el-input v-model="search" placeholder="搜索考试" />
            </template>
        </el-table-column>
        <el-table-column prop="exambegintime" label="考试开始时间" width="180" />
        <el-table-column prop="allnum" label="总题数" width="80" />
        <el-table-column prop="dannum" label="选择题/分值" width="80" />
        <el-table-column prop="duonum" label="多选题/分值" width="80" />
        <el-table-column prop="pannum" label="判断题/分值" width="80" />
        <el-table-column prop="fenshu" label="总分" width="80" />
        <el-table-column prop="createtime" label="创建时间" />
        <el-table-column prop="examstatus" label="考试状态" />
        <el-table-column prop="examCiShu" label="允许考试次数" />
        <el-table-column align="right" label="操作" width="150">
            <template #default="scope">
                <center>
                    <el-button size="small" type="primary" @click="drawervisible = true; getCurrentRow(scope.row)"
                        plain>
                        修改
                    </el-button>
                    <el-button size="small" type="danger" @click="delExam(scope.row)" plain>
                        删除
                    </el-button>
                </center>
            </template>
        </el-table-column>
    </el-table>
    <el-dialog :key="diakey" v-model="dialogFormVisible" title="新增考试" width="900">
        <center><span style="text-align: center;color:red">题库和标签必须至少选择一个</span></center>
        <el-form ref="from" :model="form">
            <el-form-item label="考试名称" :label-width="formLabelWidth" :rules="[{ required: true, message: '必须填写' }]">
                <el-input v-model="form.examname" autocomplete="off" />
            </el-form-item>
            <!--  -->
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-form-item label="选择题数量" :label-width="formLabelWidth" :min="0"
                        :rules="[{ required: true, message: '必须填写' }]">
                        <el-input-number :precision="0" v-model="form.dannum" controls-position="right" />
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="选择题分值" :label-width="formLabelWidth" :min="0"
                        :rules="[{ required: true, message: '必须填写' }]">
                        <el-input-number v-model="form.danfen" controls-position="right" />
                    </el-form-item>
                </el-col>
            </el-row>
            <!--  -->
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-form-item label="多选题数量" :label-width="formLabelWidth" :min="0"
                        :rules="[{ required: true, message: '必须填写' }]">
                        <el-input-number :precision="0" v-model="form.duonum" controls-position="right" />
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="多选题分值" :label-width="formLabelWidth" :min="0"
                        :rules="[{ required: true, message: '必须填写' }]">
                        <el-input-number v-model="form.duofen" controls-position="right" />
                    </el-form-item>
                </el-col>
            </el-row>
            <!--  -->
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-form-item label="判断题数量" :label-width="formLabelWidth" :min="0"
                        :rules="[{ required: true, message: '必须填写' }]">
                        <el-input-number :precision="0" v-model="form.pannum" controls-position="right" />
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="判断题分值" :label-width="formLabelWidth" :min="0"
                        :rules="[{ required: true, message: '必须填写' }]">
                        <el-input-number v-model="form.panfen" controls-position="right" />
                    </el-form-item>
                </el-col>
            </el-row>
            <!--  -->
            <el-form-item label="选择题库" :label-width="formLabelWidth">
                <el-select v-model="form.qustores" placeholder="选择题库" multiple>
                    <el-option v-for="i in options" :label="i.label" :value="i.value" :key="i" />
                </el-select>
            </el-form-item>
            <el-form-item label="选择标签" :label-width="formLabelWidth">
                <el-select v-model="form.tags" placeholder="选择标签" multiple>
                    <el-option v-for="i in optionstag" :label="i.label" :value="i.value" :key="i" />
                </el-select>
            </el-form-item>
            <!--  -->
            <el-row :gutter="10">
                <el-col :span="8">
                    <el-form-item label="考试开始时间" :label-width="120" :rules="[{ required: true, message: '必须填写' }]">
                        <div class="block">
                            <el-date-picker v-model="form.valuecreatetime" type="datetime" placeholder="选择考试开始时间"
                                :shortcuts="shortcuts" />
                        </div>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="考试时长" :label-width="150" :rules="[{ required: true, message: '必须填写' }]">
                        <el-input-number :precision="0" v-model="form.examtimelong" controls-position="right" :min="1">
                            <template #suffix>
                                <span>分钟</span>
                            </template>
                            <template #decrease-icon>
                                <el-icon>
                                    <Minus />
                                </el-icon>
                            </template>
                            <template #increase-icon>
                                <el-icon>
                                    <Plus />
                                </el-icon>
                            </template>
                        </el-input-number>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="允许考试次数" :label-width="120" :rules="[{ required: true, message: '必须填写' }]">
                        <el-input-number :precision="0" v-model="form.examCiShu" controls-position="right" :min="1">
                            <template #decrease-icon>
                                <el-icon>
                                    <Minus />
                                </el-icon>
                            </template>
                            <template #increase-icon>
                                <el-icon>
                                    <Plus />
                                </el-icon>
                            </template>
                        </el-input-number>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
        <template #footer>
            <el-button @click="dialogFormVisible = false">取消</el-button>
            <el-button type="primary" @click="dialogFormVisible = false; createexam2db(form)">
                确认
            </el-button>
        </template>
    </el-dialog>
</template>

<script lang="js" setup>
import { ref, computed, reactive } from 'vue'
import {
    Minus,
    Plus,
} from '@element-plus/icons-vue'
import axios from 'axios';
import { ElMessage, ElMessageBox, ElButton } from 'element-plus'

const diakey = ref(0)
const dialogFormVisible = ref(false)
const formLabelWidth = '100px'
const form = reactive({
    Yuanexamname: '',
    examname: '新建考试' + Date.now().toString(),   // 考试名称
    qustores: '',   // 选择的题库
    tags: '',
    dannum: 96,     //选择题数量
    danfen: 0.5,   // 选择题分值
    duonum: 50,     // 多选题数量
    duofen: 0.8,  // 多选题分值
    pannum: 40,     // 判断题数量
    panfen: 0.3,     // 判断题分值
    valuecreatetime: '', // 考试开始时间
    examtimelong: 90, // 考试时长
    examCiShu: 1, // 考试次数
})
var addoredit = ref(0)
const toaddexam = () => {
    form.examname = '新建考试' + Date.now().toString()   // 考试名称
    form.qustores = ''   // 选择的题库
    form.tags = ''
    form.dannum = 96   //选择题数量
    form.danfen = 0.5   // 选择题分值
    form.duonum = 50     // 多选题数量
    form.duofen = 0.8  // 多选题分值
    form.pannum = 40   // 判断题数量
    form.panfen = 0.3   // 判断题分值
    form.valuecreatetime = '' // 考试开始时间
    form.examtimelong = 90 // 考试时长
    form.examCiShu = 1 // 考试次数
    dialogFormVisible.value = true
    diakey.value += 1
    addoredit.value = 1
}
const createexam2db = async (form) => {
    // 向后台提交 form 表单数据
    console.log(form)
    if (form.examname == "" || form.examCiShu == "" || form.dannum == null || form.duonum == null || form.pannum == null || form.danfen == null || form.duofen == null || form.panfen == null) {
        ElMessage({
            type: 'error',
            message: '必须填写',
        })
        dialogFormVisible.value = true
        return
    }
    if ((form.qustores == "" || form.valuecreatetime == "") && (form.tags == "" || form.valuecreatetime == "")) {
        ElMessage({
            type: 'error',
            message: '时间、题库选择为空',
        })
        dialogFormVisible.value = true
        return
    }
    if (addoredit.value == 1) {
        const userid = localStorage.getItem("id")
        const role = localStorage.getItem("role")
        const user = localStorage.getItem("user")
        const result = await axios.get(`http://localhost:8000/api/exam/get_all_exams?user=${user}&userid=${userid}&role=${role}`)
        for (let index = 0; index < result.data.data.length; index++) {
            const data = result.data.data[index]
            if (form.examname == data.examname) {
                ElMessage({
                    type: 'error',
                    message: '考试名称已存在',
                })
                dialogFormVisible.value = true
                return
            }
        }
        const token = localStorage.getItem("Authorization")
        const res = await axios.post('http://localhost:8000/api/exam/create_exam', {
            token: token,
            data: {
                examname: form.examname,                    // 考试名称
                qustores: form.qustores,                    // 选择的题库
                tags: form.tags,                            //
                dannum: form.dannum,                        // 选择题数量
                danfen: form.danfen,                        // 选择题分值
                duonum: form.duonum,                        // 多选题数量
                duofen: form.duofen,                        // 多选题分值
                pannum: form.pannum,                        // 判断题数量
                panfen: form.panfen,                        // 判断题分值
                valuecreatetime: form.valuecreatetime,      // 考试开始时间
                examtimelong: form.examtimelong,            // 考试时长
                examCiShu: form.examCiShu,                  // 考试次数
            }
        });
        if (res.data['status'] == 500) {
            ElMessage({
                type: 'error',
                message: res.data['error'],
            })
            dialogFormVisible.value = true
            return
        }
        ElMessage({
            type: 'success',
            message: '新建成功',
        })
    }
    if (addoredit.value == 2) {
        const userid = localStorage.getItem("id")
        const role = localStorage.getItem("role")
        const user = localStorage.getItem("user")
        const result = await axios.get(`http://localhost:8000/api/exam/get_all_exams?user=${user}&userid=${userid}&role=${role}`)
        for (let index = 0; index < result.data.data.length; index++) {
            const data = result.data.data[index]
            if (form.examname == data.examname) {
                ElMessage({
                    type: 'error',
                    message: '考试名称已存在',
                })
                dialogFormVisible.value = true
                return
            }
        }
        const token = localStorage.getItem("Authorization")
        const res = await axios.post('http://localhost:8000/api/exam/update_exam', {
            token: token,
            data: {
                Yuanexamname: form.Yuanexamname,
                examname: form.examname,                    // 考试名称
                qustores: form.qustores,                    // 选择的题库
                tags: form.tags,                            //
                dannum: form.dannum,                        // 选择题数量
                danfen: form.danfen,                        // 选择题分值
                duonum: form.duonum,                        // 多选题数量
                duofen: form.duofen,                        // 多选题分值
                pannum: form.pannum,                        // 判断题数量
                panfen: form.panfen,                        // 判断题分值
                valuecreatetime: form.valuecreatetime,      // 考试开始时间
                examtimelong: form.examtimelong,            // 考试时长
                examCiShu: form.examCiShu,                  // 考试次数
            }
        });
        if (res.data['status'] == 500) {
            ElMessage({
                type: 'error',
                message: res.data['error'],
            })
            dialogFormVisible.value = true
            return
        }
        ElMessage({
            type: 'success',
            message: '修改成功',
        })
    }
    getexaminfo()
}
//
const options = []
const optionstag = []
const getqustores = async () => {
    const res = await axios.get('http://localhost:8000/api/question/get_questionstore_info');
    const data = res.data
    for (let index = 0; index < data.qustore.length; index++) {
        options.push({ value: data.qustore[index], label: data.qustore[index] });
    }
    for (let index = 0; index < data.tag.length; index++) {
        optionstag.push({ value: data.tag[index], label: data.tag[index] });
    }
}
getqustores()

// 
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
            allnum: data.dannum + data.duonum + data.pannum,
            dannum: `${data.dannum}/${data.danfen}`,
            duonum: `${data.duonum}/${data.duofen}`,
            pannum: `${data.pannum}/${data.panfen}`,
            fenshu: `${fenshu}`,
            createtime: examCT.toLocaleString(),
            examstatus: examstatus,
            qustores: data.qustore,
            tags: data.tags,
            examtimelong: data.examtimelong,
            examCiShu: form.examCiShu,                  // 考试次数
        })
    }
}
getexaminfo()

// 删除考试
const delExam = async (scoperow) => {
    ElMessageBox.confirm('确认删除该考试吗？', '删除考试', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        const token = localStorage.getItem("Authorization")
        if (scoperow.examstatus == "进行中") {
            ElMessage({
                type: 'error',
                message: "正在进行的考试不可以删除",
            })
            return
        }
        const res = await axios.post('http://localhost:8000/api/exam/delete_exam', {
            examname: scoperow.examname,
            token: token
        })
        if (res.data['status'] == 500) {
            ElMessage({
                type: 'error',
                message: res.data['error'],
            })
            return
        }
        ElMessage({
            type: 'success',
            message: '删除成功',
        })
        getexaminfo()
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '已取消删除'
        })
    })
}
// 修改考试
const getCurrentRow = (scoperow) => {
    if (scoperow.examstatus == "进行中") {
        ElMessage({
            type: 'error',
            message: "正在进行的考试不可以删除",
        })
        return
    }
    form.Yuanexamname = scoperow.examname
    form.examname = scoperow.examname  // 考试名称
    form.qustores = scoperow.qustores  // 选择的题库
    form.tags = scoperow.tags //
    form.dannum = scoperow.dannum.split("/")[0]   //选择题数量
    form.danfen = scoperow.dannum.split("/")[1]  // 选择题分值
    form.duonum = scoperow.duonum.split("/")[0]      // 多选题数量
    form.duofen = scoperow.duonum.split("/")[1]   // 多选题分值
    form.pannum = scoperow.pannum.split("/")[0]   // 判断题数量
    form.panfen = scoperow.pannum.split("/")[1]    // 判断题分值
    form.valuecreatetime = scoperow.exambegintime // 考试开始时间
    form.examtimelong = scoperow.examtimelong // 考试时长
    form.examCiShu = scoperow.examCiShu              // 考试次数
    dialogFormVisible.value = true
    diakey.value += 1
    addoredit.value = 2
}
</script>

<style scoped>
.block {
    padding: 0px 0;
    border-right: solid 1px var(--el-border-color);
    flex: 1;
}

.block:last-child {
    border-right: none;
}
</style>