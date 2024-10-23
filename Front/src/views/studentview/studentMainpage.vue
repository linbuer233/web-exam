<script lang="js" setup>
import { ref } from 'vue'
import 'element-plus/dist/index.css'
import { Document, Menu as IconMenu, Notebook, List } from '@element-plus/icons-vue'
import { ArrowDown } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios';
import { RouterView, useRouter } from 'vue-router'
const router = useRouter();
let token = localStorage.getItem('Authorization');
async function loginjiaoyan() {
    var res = await axios.post('http://localhost:8000/api/login_yz', {
        token: token
    })
    if (res.data['status'] == 200) {
        console.log('')
    } else {
        localStorage.removeItem('Authorization');
        localStorage.removeItem('user');
        localStorage.removeItem('role');
        localStorage.removeItem('id');
        router.push("/login");
        return
    }
}
loginjiaoyan()
// var user = ref()
var user = localStorage.getItem('user')
if (user == "admin") {
    router.push("/adminMainpage");
}
const handleOpen = (key, keyPath) => {
    console.log(key, keyPath)
}

const handleClose = (key, keyPath) => {
    console.log(key, keyPath)
}

const changepassword = () => {
    ElMessageBox.prompt('输入新密码', '修改密码', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        center: true,
    }).then(async ({ value }) => {
        // 假设修改密码的 API 路径为 '/api/change-password'
        var res = await axios.post("http://localhost:8000/api/change_password", {
            pwd: value,
            user: localStorage.getItem("user"),
            id: localStorage.getItem("id")
        })
        console.log(res.data)
        ElMessage({
            type: 'success',
            message: `修改密码成功`,
        })
        localStorage.removeItem('Authorization');
        localStorage.removeItem('user');
        localStorage.removeItem('role');
        localStorage.removeItem('id');
        router.push("/login");
        return
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '取消修改',
        })
    })
}
const currpageurl = ref(sessionStorage.getItem("currpageurl"))
if (currpageurl.value === null) {
    currpageurl.value = "1"
    sessionStorage.setItem("currpageurl", currpageurl.value)
}
const outSign = () => {
    localStorage.removeItem('Authorization');
    localStorage.removeItem('user');
    localStorage.removeItem('role');
    localStorage.removeItem('id');
    currpageurl.value = "1"
    sessionStorage.setItem("currpageurl", currpageurl.value)
    router.push("/login");
}
const tohome = () => {
    currpageurl.value = "1"
    sessionStorage.setItem("currpageurl", currpageurl.value)
    router.push("/studentMainpage/home");
}
const toexam = () => {
    currpageurl.value = "2-1"
    sessionStorage.setItem("currpageurl", currpageurl.value)
    router.push("/studentMainpage/exam");
}
const toexamrecords = () => {
    currpageurl.value = "2-2"
    sessionStorage.setItem("currpageurl", currpageurl.value)
    router.push("/studentMainpage/examrecords");
}
const toquesstore = () => {
    currpageurl.value = "3"
    sessionStorage.setItem("currpageurl", currpageurl.value)
    router.push("/studentMainpage/questionstore");
}
const towrongqu = () => {
    currpageurl.value = "4"
    sessionStorage.setItem("currpageurl", currpageurl.value)
    router.push("/studentMainpage/wrongquestion");
}
</script>

<template>
    <div class="common-layout">
        <el-container>
            <el-header style="padding: 5px;width:100vw;margin:0px">
                <div class="header">
                    <el-row :gutter="20" style="width: 100vw;">
                        <el-col :span="4">
                            <div class="grid-content ep-bg-purple">
                                <span style="position:relative;left: 20px;">学生端</span>
                            </div>
                        </el-col>
                        <el-col :span="17">
                            <div class="grid-content ep-bg-purple" />
                        </el-col>
                        <el-col :span="3">
                            <el-dropdown>
                                <span class="el-dropdown-link" style="padding-top:5px;font-size:22px">
                                    {{ user }}
                                    <el-icon class="el-icon--right">
                                        <arrow-down />
                                    </el-icon>
                                </span>
                                <template #dropdown>
                                    <el-dropdown-menu>
                                        <el-dropdown-item>
                                            <el-button plain @click="changepassword">
                                                修改密码
                                            </el-button>
                                        </el-dropdown-item>
                                        <el-dropdown-item>
                                            <el-button plain @click="outSign">
                                                退出登录
                                            </el-button>
                                        </el-dropdown-item>
                                    </el-dropdown-menu>
                                </template>
                            </el-dropdown>
                        </el-col>
                    </el-row>
                </div>
            </el-header>
            <el-container style="width:100vw">
                <el-aside class="aside" width="200px">
                    <el-menu :default-active=currpageurl class="exam-menu" @open="handleOpen" @close="handleClose">
                        <el-menu-item index="1" @click="tohome">
                            <el-icon><icon-menu /></el-icon>
                            <span plain @click="tohome">首页</span>
                        </el-menu-item>
                        <el-sub-menu index="2">
                            <template #title>
                                <el-icon>
                                    <list />
                                </el-icon>
                                <span>考试列表</span>
                            </template>
                            <el-menu-item index="2-1" @click="toexam"><span>在线考试</span></el-menu-item>
                            <el-menu-item index="2-2" @click="toexamrecords"><span>考试记录</span></el-menu-item>
                        </el-sub-menu>
                        <el-menu-item index="3" @click="toquesstore">
                            <el-icon>
                                <document />
                            </el-icon>
                            <span>题库</span>
                        </el-menu-item>
                        <el-menu-item index="4" @click="towrongqu">
                            <el-icon>
                                <Notebook />
                            </el-icon>
                            <span>错题本</span>
                        </el-menu-item>
                    </el-menu>
                    <!-- <nav>
                        <RouterLink to="/">Home</RouterLink>
                        <RouterLink to="/about">About</RouterLink>
                    </nav> -->
                </el-aside>
                <el-main class="mainField">
                    <router-view />
                </el-main>
            </el-container>
        </el-container>
    </div>

</template>

<style scoped>
.example-showcase .el-dropdown-link {
    cursor: pointer;
    color: var(--el-color-primary);
    display: flex;
    align-items: center;
}

.common-layout {
    display: flex;
    min-height: 100vh;
    min-width: 100vw;
    flex-direction: column;
    background-color: white;
}

.aside {
    border-radius: 4px;
    padding-right: 0px;
    margin-right: 5px;
    margin-left: 5px;
    margin-bottom: 5px;
    border: 1px solid #e6ebf5;
    box-shadow: 0px 0px 0px 0px rgba(0, 0, 0, 0.1);
}

.exam-menu {
    height: 100%;
    background-color: white;
}


.header {
    width: 100vw;
    max-width: 100vw;
    line-height: 1.8;
    max-height: 100vh;
    color: #000;
    font-size: 24px;
    padding-left: 0px;
    margin: 0px;
    border: 1px solid #e6ebf5;
    box-shadow: 1px 1px 0px 0px rgba(0, 0, 0, 0.1);
}

.mainField {
    border-radius: 4px;
    width: 90%;
    color: #000;
    background-color: white;
    border: 1px solid #e6ebf5;
    box-shadow: 1px 1px 0px 0px rgba(0, 0, 0, 0.1);
    margin: 5px;
}

.logo {
    display: block;
    margin: 0 auto 2rem;
}

nav {
    width: 100%;
    font-size: 12px;
    text-align: center;
    margin-top: 2rem;
}

nav a.router-link-exact-active {
    color: var(--color-text);
}

nav a.router-link-exact-active:hover {
    background-color: transparent;
}

nav a {
    display: inline-block;
    padding: 0 1rem;
    border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
    border: 0;
}

@media (min-width: 1024px) {
    header {
        display: flex;
        place-items: center
    }

    .logo {
        margin: 0 0rem 0 0;
    }

    .wrapper {
        display: flex;
        place-items: flex-start;
        flex-wrap: wrap;
    }

    nav {
        text-align: left;
        margin-left: -1rem;
        font-size: 1rem;

        padding: 1rem 0;
        margin-top: 1rem;
    }
}
</style>
