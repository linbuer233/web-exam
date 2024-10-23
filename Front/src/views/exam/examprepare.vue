<template>
    <div style="height: 100vh;width:100vw;background-color: white;">
        <el-card class="prepareCard">
            <h1 style="text-align: center;">{{ examname }}</h1>
            <el-text style="font-size: x-large;" type="info">总分：</el-text>
            <el-text style="font-size: x-large;" type="primary">{{ examallfen }}</el-text>
            <br><br>
            <el-text style="font-size: x-large;" type="info">及格分：</el-text>
            <el-text style="font-size: x-large;" type="primary">{{ examallfen * 0.6 }}</el-text>
            <br><br>
            <el-text style="font-size: x-large;" type="info">考试开始时间：</el-text>
            <el-text style="font-size: x-large;" type="primary">{{ examnameBT }}</el-text>
            <br><br>
            <el-text style="font-size: x-large;" type="info">考试时长：</el-text>
            <el-text style="font-size: x-large;" type="primary">{{ examtimelong }}</el-text>
            <br>
            <center>
                <el-text style="font-size: x-large;" type="info">距离考试开始</el-text>
                <br>
                <el-text style="font-size: xxx-large;" type="primary">{{ timere }}</el-text>
                <br><br>
                <el-button ref="beginButton" type="primary" size="large" @click="BeginExam"
                    id="beginExam">开始考试</el-button>
            </center>
        </el-card>
    </div>
</template>

<script lang="js" setup>
import { ref } from 'vue';
import { ElMessage, ElButton } from 'element-plus'
import { useRouter } from 'vue-router'
const router = useRouter();

const timere = ref("")
const times = ref(0)
// 从sessionStorage提取信息
const inputTime = new Date(sessionStorage.getItem("examnameBT"))
const examnameBT = sessionStorage.getItem("examnameBT")
const examallfen = sessionStorage.getItem("examallfen")
const examtimelong = sessionStorage.getItem("examtimelong")
const examname = sessionStorage.getItem("examname")

// 开始考试函数
const BeginExam = () => {
    if (times.value > 0) {
        ElMessage({
            type: 'error',
            message: '还未到考试时间',
        })
        return
    }
    // 前往考试页面
    router.push({ path: '/exam/exampage' })
}

// 倒计时
// 先调用countDown函数，可以避免在打开界面后停一秒后才开始倒计时
countDown();
// 定时器 每隔一秒变化一次
const tid = setInterval(countDown, 1000);
function clearI() {
    var a = sessionStorage.getItem("examBegin")
    if (a == 1) {
        clearInterval(tid);
        sessionStorage.removeItem("examBegin")
    }
}
function countDown() {
    // 获取当前时间的时间戳（单位毫秒）
    var nowTime = +new Date();
    // 把剩余时间毫秒数转化为秒
    times.value = (inputTime - nowTime) / 1000;
    if (times.value <= 0) {
        timere.value = "00" + ":" + "00" + ":" + "00";
        sessionStorage.setItem("examBegin", 1)
        setTimeout(clearI, 100)
        return
    }
    // 计算小时数 转化为整数
    var h = parseInt(times.value / 60 / 60);
    // 如果小时数小于10，要变成0 + 数字的形式 赋值给盒子
    h = h < 10 ? "0" + h : h;
    // 计算分钟数 转化为整数
    var m = parseInt((times.value - parseInt(h) * 3600) / 60);
    // 如果分钟数小于10，要变成0 + 数字的形式 赋值给盒子
    m = m < 10 ? "0" + m : m;
    // 计算秒数 转化为整数
    var s = parseInt((times.value - parseInt(h) * 3600 - parseInt(h) * 60) % 60);
    // 如果秒钟数小于10，要变成0 + 数字的形式 赋值给盒子
    s = s < 10 ? "0" + s : s;
    // 赋值给 refs
    timere.value = h + ":" + m + ":" + s;
}
</script>

<style lang="css">
.prepareCard {
    width: 800px;
    height: 500px;
    position: relative;
    left: 25%;
    top: 15%;
    background-color: #faf8f8;
}
</style>