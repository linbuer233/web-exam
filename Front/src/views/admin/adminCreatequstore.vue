<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">题库信息</div>
    <el-table :data="filterTableData" border style="width: 100%;align-items: center;max-height:90%" height="100%">
        <el-table-column prop="qustorename" label="题库"><template #header>
                <el-input v-model="search" size="small" placeholder="搜索题库" />
            </template></el-table-column>
        <el-table-column prop="allnum" label="题目数量" width="100" />
        <el-table-column prop="dannum" label="选择题数量" width="100" />
        <el-table-column prop="duonum" label="多选题数量" width="100" />
        <el-table-column prop="pannum" label="判断题数量" width="100" />
        <el-table-column align="right" label="操作" width="220">
            <template #default="scope">
                <center>
                    <el-button size="small" type="primary" @click="drawervisible = true; getCurrentRow(scope.row)"
                        plain>
                        添加试题
                    </el-button>
                    <el-button v-if="scope.row.tiandisabled" size="small" type="danger"
                        @click="handleDelete(scope.$index, scope.row)" plain disabled>
                        删除
                    </el-button>
                    <el-button v-else size="small" type="danger" @click="handleDelete(scope.$index, scope.row)" plain>
                        删除
                    </el-button>
                </center>
            </template>
        </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="添加试题" width="1000" :before-close="handleClose">
        <adminaddquestionsingle />
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="dialogVisible = false">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="js" setup>
import axios from 'axios';
import { computed, ref } from 'vue';
import { ElButton } from 'element-plus'
import adminaddquestionsingle from './adminaddquestionsingle.vue';

const dialogVisible = ref(false)
const search = ref('');
const tableData = ref([]);
const totalItems = ref(15); // 初始值，稍后从后端获取
const filterTableData = ref(computed(() =>
    tableData.value.filter(data =>
        !search.value ||
        data.qustorename.toLowerCase().includes(search.value.toLowerCase())
    )
));
const getqutagandstore = async () => {
    try {
        const res = await axios.get('http://localhost:8000/api/question/get_questionstore_info');
        var data = res.data
        for (let index = 0; index < data.qustore.length; index++) {
            if (data.qustore[index] == "默认题库") {
                tableData.value.push({
                    qustorename: data.qustore[index],
                    allnum: data.allnum[index],
                    dannum: data.dannum[index],
                    duonum: data.duonum[index],
                    pannum: data.pannum[index],
                    tiandisabled: true,
                });
                continue;
            }
            tableData.value.push({
                qustorename: data.qustore[index],
                allnum: data.allnum[index],
                dannum: data.dannum[index],
                duonum: data.duonum[index],
                pannum: data.pannum[index],
                tiandisabled: false,
            });
        }
        totalItems.value = data.qustore.length
    } catch (error) {
        console.error(error);
    }
}
getqutagandstore()

const getCurrentRow = (scoperow) => {
    dialogVisible.value = true
}

// const handleClose = () => {
//     ElMessageBox.confirm('Are you sure to close this dialog?')
//         .then(() => {
//             dialogVisible.value = false
//         })
//         .catch(() => {
//             // catch error
//         })
// }
</script>