<template>
    <div style="background-color:rgb(236, 236, 236);width:100vw;height:100vh">
        <div>
            <el-form :model="form" label-width="auto" class="logindiv">
                <h1 class="loginheader">Login</h1>
                <el-form-item label="学号">
                    <el-input v-model="form.id" placeholder="学号" />
                </el-form-item>
                <el-form-item label="密码">
                    <el-input v-model="form.pwd" type="password" placeholder="密码" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit" style="width: 100%;">登录</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script lang="js" setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router';
const router = useRouter();
// do not use same name with ref
const form = reactive({
    id: '',
    pwd: '',
    region: '',
    date1: '',
    date2: '',
    delivery: false,
    type: [],
    resource: '',
    desc: '',

})

const onSubmit = async () => {
    console.log('submit!')
    if (form.pwd.length == 0 && form.id.length == 0) {
        ElMessage.error('学号或密码错误')
        return  // return to avoid continue request
    }
    var res = await axios.post('http://localhost:8000/api/login', {
        id: form.id,
        pwd: form.pwd
    })
    if (res.data == 500) {
        ElMessage.error('学号或密码错误')
        return
    }
    if (res.status === 200) {
        console.log('login success')
        localStorage.setItem('user', res.data.user)
        localStorage.setItem('id', res.data.id)
        localStorage.setItem('Authorization', res.data.token)
        localStorage.setItem('role', res.data.role)
        if (res.data.user === 'admin') {
            router.push('/adminMainpage')
        } else {
            router.push('/studentMainpage')
        }
        return
    }
}
</script>

<style lang="css">
.logindiv {
    height: 38vh;
    width: 25vw;
    position: absolute;
    top: -0%;
    left: 30%;
    background-color: white;
    box-shadow: 2px 2px 0;
    margin: 10%;
    padding-top: 10px;
    padding-right: 30px;
    padding-bottom: 10px;
    padding-left: 30px;
}

.loginheader {
    text-align: center;
    color: #000;
    font-size: 24px;
    font-weight: bold;
    text-emphasis-color: black;
    margin-bottom: 10%;
}
</style>