<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">用户管理</div>
    <el-button size="large" type="primary" @click="dialogFormVisible = true" style="margin-bottom: 10px;">
        <el-icon>
            <Plus />
        </el-icon>
        <span>新增用户</span>
    </el-button>
    <el-dialog v-model="dialogFormVisible" title="新增用户" width="500">
        <center><span style="text-align: center;color:red;padding:2px">学号要为GX000格式</span></center>
        <el-form :model="form">
            <el-form-item label="用户名" :label-width="formLabelWidth">
                <el-input v-model="form.user" autocomplete="off" />
            </el-form-item>
            <el-form-item label="学号" :label-width="formLabelWidth">
                <el-input v-model="form.id" autocomplete="off" />
            </el-form-item>
            <el-form-item label="密码" :label-width="formLabelWidth">
                <el-input v-model="form.pwd" autocomplete="off" />
            </el-form-item>
            <el-form-item label="用户类型" :label-width="formLabelWidth">
                <el-select v-model="form.role" placeholder="">
                    <el-option label="admin" value="admin" />
                    <el-option label="student" value="student" />
                </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="adduser(form)">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
    <el-table :data="filterTableData" border style="width: 100%;align-items: center;max-height:75%">
        <el-table-column prop="user" label="用户名"><template #header>
                <el-input v-model="search" size="small" placeholder="搜索用户" />
            </template></el-table-column>
        <el-table-column prop="id" label="用户id" />
        <el-table-column prop="role" label="用户类型" />
        <el-table-column align="right" label="操作" width="320">
            <template #default="scope">
                <center>
                    <el-button size="small" type="primary" @click="drawervisible = true; getCurrentRow(scope.row)"
                        plain>
                        修改
                    </el-button>
                    <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)" plain>
                        删除
                    </el-button>
                </center>
            </template>
        </el-table-column>
    </el-table>
    <el-pagination background layout="prev, pager, next" :default-page-size="20" :total="totalItems"
        style="padding-top: 20px;" />
    <el-drawer v-model="drawervisible" :show-close="false">
        <template #header="{ close, titleId, titleClass }">
            <h4 :id="titleId" :class="titleClass">修改用户信息</h4>
            <el-button type="danger" @click="close">
                <el-icon class="el-icon--left">
                    <CircleCloseFilled />
                </el-icon>
                关闭
            </el-button>
        </template>
        <div style="margin-bottom: 20px;">
            <center><span>重置密码之后默认密码为1</span></center>
        </div>
        <el-form :model="form1">
            <el-form-item label="用户名" :label-width="formLabelWidth">
                <el-input v-model="form1.user" autocomplete="off" />
            </el-form-item>
            <el-form-item label="学号" :label-width="formLabelWidth">
                <el-input v-model="form1.id" autocomplete="off" disabled />
            </el-form-item>
            <el-form-item label="用户类型" :label-width="formLabelWidth">
                <el-select v-model="form1.role" placeholder="">
                    <el-option label="admin" value="admin" />
                    <el-option label="student" value="student" />
                </el-select>
            </el-form-item>
        </el-form>
        <center>
            <div class="dialog-footer">
                <el-button type="primary" @click="confirmchange_userinfo(form1)">
                    确认修改
                </el-button>
                <el-button @click="resetuserpwd(currentrow.id)">重置密码</el-button>
            </div>
        </center>

    </el-drawer>

</template>

<script lang="js" setup>
import axios from 'axios';
import { useRouter } from 'vue-router'
import { computed, reactive, ref } from 'vue';
import { Plus, CircleCloseFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, ElButton, ElDrawer } from 'element-plus'

const router = useRouter();
const search = ref('');
const tableData = ref([]);
const totalItems = ref(15); // 初始值，稍后从后端获取
const dialogFormVisible = ref(false)
const formLabelWidth = '100px'
const drawervisible = ref(false)
const currentrow = ref([])
const form = reactive({
    user: '',
    role: '',
    id: '',
    pwd: '',
})
const form1 = reactive({
    user: '',
    id: '',
    role: '',
})
const filterTableData = computed(() =>
    tableData.value.filter(data =>
        !search.value ||
        data.user.toLowerCase().includes(search.value.toLowerCase())
    )
);

const confirmchange_userinfo = (formtemp) => {
    console.log(formtemp)
    ElMessageBox.confirm('确认修改?', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        var token = localStorage.getItem('Authorization')
        await axios.post('http://localhost:8000/api/change_userinfo', { id: formtemp.id, user: formtemp.user, role: formtemp.role, token: token })
        ElMessage({
            type: 'success',
            message: '修改成功',
        })
        get_users()
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '修改密码',
        })
    })
}

const resetuserpwd = (id) => {
    console.log(id)
    ElMessageBox.confirm('确认重置?', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        await axios.post("http://localhost:8000/api/change_password", {
            pwd: "1",
            id: id
        })
        var localid = localStorage.getItem("id")
        if (localid == id) {
            localStorage.removeItem("Authorization");
            localStorage.removeItem("id");
            localStorage.removeItem("name");
            localStorage.removeItem('role');
            router.push("/login");
        }
        ElMessage({
            type: 'success',
            message: '重置密码成功',
        })
        get_users()
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '取消重置密码',
        })
    })
}

const getCurrentRow = (scoperow) => {
    console.log(scoperow)
    currentrow.value = scoperow
    form1.user = currentrow.value.user
    form1.id = currentrow.value.id
    form1.role = currentrow.value.role
};

const handleDelete = (index, row) => {
    console.log(index, row);
    ElMessageBox.confirm('确认删除?', '提示', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        var token = localStorage.getItem('Authorization')
        await axios.post('http://localhost:8000/api/delete_user', { id: row.id, token: token })
        ElMessage({
            type: 'success',
            message: '删除成功',
        })
        get_users()
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '取消删除',
        })
    })
};

const adduser = async (from) => {
    var pattern = /^GX\d{3}$/;
    if (form.user == "" || form.pwd == "" || form.role == "" || form.role == "") {
        ElMessage({
            type: 'error',
            message: `不能为空`,
        })
        return
    }
    if (!pattern.test(from.id)) {
        ElMessage({
            type: 'error',
            message: `学号一定为GX000格式`,
        })
        return
    }
    var id = from.id;
    const response = await axios.get('http://localhost:8000/api/userisexists?id=' + id)
    if (response.data) {
        ElMessage({
            type: 'error',
            message: `学号已存在`,
        })
        return
    } else {
        console.log(form)
        const response = await axios.post('http://localhost:8000/api/add_user', {
            id: from.id,
            user: from.user,
            pwd: from.pwd,
            role: from.role,
        })
        if (response.data['status'] === 200) {
            ElMessage({
                type: 'success',
                message: `添加成功`,
            })
            dialogFormVisible.value = false;
            get_users();
        }
    }
}

async function get_users() {
    try {
        const response = await axios.get("http://localhost:8000/api/get_users");
        tableData.value = response.data; // 将后端数据赋值给 tableData
        totalItems.value = response.data.length; // 根据后端数据设置总页数
    } catch (error) {
        console.error("请求失败：", error);
    }
}

get_users(); // 调用函数以获取用户数据

</script>
<style lang="css">
.el-table .cell {
    text-align: center;
}
</style>