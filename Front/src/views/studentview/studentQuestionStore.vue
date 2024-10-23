<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">题库</div>
    <el-table :data="filterTableData" border style="width: 100%;align-items: center;max-height:90%" height="100%">
        <el-table-column prop="qustorename" label="题库"><template #header>
                <el-input v-model="search" size="small" placeholder="搜索题库" />
            </template></el-table-column>
        <el-table-column prop="allnum" label="题目数量" width="100" />
        <el-table-column prop="dannum" label="选择题数量" width="100" />
        <el-table-column prop="duonum" label="多选题数量" width="100" />
        <el-table-column prop="pannum" label="判断题数量" width="100" />
        <el-table-column align="right">
            <template #default="scope">
                <center>
                    <el-button size="small" type="primary" @click="Sequentialpractice(scope.$index, scope.row)" plain>
                        顺序练习
                    </el-button>
                    <el-button size="small" type="success" @click="Randompractice(scope.$index, scope.row)" plain>
                        随机练习
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
import { useRouter } from 'vue-router'
const router = useRouter();
const search = ref('');
const tableData = ref([]);
const totalItems = ref(15); // 初始值，稍后从后端获取
const filterTableData = ref(computed(() =>
    tableData.value.filter(data =>
        !search.value ||
        data.qustorename.toLowerCase().includes(search.value.toLowerCase())
    )
));
// 获取题库
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
};
getqutagandstore();

const Sequentialpractice = (index, row) => {
    const id = localStorage.getItem("id")
    sessionStorage.setItem('qupracticeid', id)
    sessionStorage.setItem('qupracticequstorename', row.qustorename)
    sessionStorage.setItem('qupracticeType', 'SunXu')
    router.push("/qustore/qustorepractice")
};

const Randompractice = (index, row) => {
    const id = localStorage.getItem("id")
    sessionStorage.setItem('qupracticeid', id)
    sessionStorage.setItem('qupracticequstorename', row.qustorename)
    sessionStorage.setItem('qupracticeType', 'Random')
    router.push("/qustore/qustorepractice")
};

</script>
<style lang="css">
.el-table .cell {
    text-align: center;
}
</style>