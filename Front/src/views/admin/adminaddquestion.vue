<template>
    <div data-v-106c86ed="" class="title" style="padding-top: 0px;">导入试题</div>
    <el-radio-group v-model="radio1" size="default" style="margin-bottom: 10px;">
        <el-radio-button label="批量导入" value="批量导入" @click="topi" />
        <el-radio-button label="单题导入" value="单题导入" @click="tosingle" />
    </el-radio-group>
    <el-main>
        <router-view />
    </el-main>
</template>

<script lang="js" setup>
import { ref } from 'vue'
import { RouterView, useRouter } from 'vue-router'
const router = useRouter();
const radio1 = ref(sessionStorage.getItem("radio1"))
if (radio1.value === null) {
    radio1.value = "批量导入"
    sessionStorage.setItem("radio1", radio1.value)
}
function topi() {
    router.push("/adminMainpage/addquestion/pi");
    sessionStorage.setItem("radio1", "批量导入")
}
function tosingle() {
    router.push("/adminMainpage/addquestion/single");
    sessionStorage.setItem("radio1", "单题导入")
}
</script>