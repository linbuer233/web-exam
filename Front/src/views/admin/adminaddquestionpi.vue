<template>
    <el-input v-model="textarea" style="width: 48%; height: 100%; padding-right: 2%"
        :autosize="{ minRows: 22, maxRows: 22 }" type="textarea" placeholder="输入区" />
    <el-input v-model="textarea1" style="width: 48%; height: 100%" :autosize="{ minRows: 22, maxRows: 22 }"
        type="textarea" placeholder="检查区" disabled />
    <!-- footer -->
    <el-select v-model="valuetag" filterable allow-create default-first-option :reserve-keyword="false"
        placeholder="无标签" style="width: 140px;margin-top:10px;margin-right:10px;height:30px">
        <el-option v-for="item in optionstag" :key="item.value" :label="item.label" :value="item.value" />
    </el-select>
    <el-select v-model="valuequstore" filterable allow-create default-first-option :reserve-keyword="false"
        placeholder="默认题库" style="width: 140px;margin-top:10px;margin-right:10px;height:30px">
        <el-option v-for="item in optionsqustore" :key="item.value" :label="item.label" :value="item.value" />
    </el-select>
    <el-button size="small" type="primary" @click="addpiquestion" style="margin-top: 12px; height: 30px">
        <span>导入试题</span>
    </el-button>
</template>

<script lang="js" setup>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ref, watch } from 'vue';

const textarea = ref('');
const textarea1 = ref('');

const valuetag = ref('无标签')
const valuequstore = ref('默认题库')
const optionsqustore = [{ value: "默认题库", label: "默认题库" }];
const optionstag = [{ value: "无标签", label: "无标签" }];
// 获取标签和题库信息
const getqutagandstore = async () => {
    try {
        const res = await axios.get('http://localhost:8000/api/question/get_questionstore_info');
        console.log(res.data);
        var data = res.data
        // 处理数据
        for (let index = 0; index < data.qustore.length; index++) {
            if (data.qustore[index] == "默认题库") {
                continue
            }
            optionsqustore.push({ value: data.qustore[index], label: data.qustore[index] });
        }
        for (let index = 0; index < data.tag.length; index++) {
            if (data.tag[index] == "无标签") {
                continue
            }
            optionstag.push({ value: data.tag[index], label: data.tag[index] });
        }
    } catch (error) {
        console.error(error);
    }
}
getqutagandstore()


// 使用 watch 来监听 textarea 的变化
watch(textarea, (newValue) => {
    newValue = newValue + "\n\n"
    // 使用正则表达式匹配题干、任意数量的选项、答案和可选的解析
    const questionRegex = /(\d+、.+?\n)((?:A\..+?\n)+)答案: (.+?)\n?(解析：.+?)?\n\n/gms;
    let match;
    const questionList = [];
    while ((match = questionRegex.exec(newValue)) !== null) {
        const question = {
            question: match[1].trim(),
            options: {},
            answer: match[3].trim(),
            analysis: match[4] ? match[4].trim() : null // 解析可能不存在
        };
        // 匹配所有选项
        const optionsMatch = match[2].match(/(A|B|C|D|E|F|G|H|I|J|K|L|M|N)\..+?\n/g);
        if (optionsMatch) {
            optionsMatch.forEach(option => {
                const [letter, text] = option.split('.', 2);
                question.options[letter] = text.trim();
            });
        }
        // 答案是否存在且在选项中
        for (let index = 0; index < question['answer'].length; index++) {
            if (Object.keys(question.options).includes(question['answer'][index])) {
                var panduantemp = 0
                continue
            } else {
                panduantemp = 1
            }
        }
        if (panduantemp == 1) {
            continue
        }
        questionList.push(question);
    }
    // 构建检查文本
    var temp1 = null;
    try {
        // 构建原始文本
        let originalText = '';
        questionList.forEach((question, index) => {
            originalText += question.question.trim() + '\n';
            for (const [key, value] of Object.entries(question.options)) {
                originalText += `${key}.${value}\n`;
            }
            originalText += `答案: ${question.answer}\n`;
            originalText += `解析：${question.analysis}\n`;
            if (index < questionList.length - 1) {
                originalText += '\n'; // 在题目之间添加换行符
            }
        });
        temp1 = originalText;
    } catch (error) {
        console.error('导入试题发生错误:', error);
        return;
    }
    textarea1.value = temp1;

}, { immediate: true });

const addpiquestion = async () => {
    // 这里可以添加其他导入试题的逻辑
    const questionRegex_out = /\d+、(.+?\n)((?:A\..+?\n)+)答案: (.+?)\n?(解析：.+?)?\n\n/gms;
    let match_out;
    const questionList_out = [];

    while ((match_out = questionRegex_out.exec(textarea.value + "\n\n")) !== null) {
        const question = {
            question: match_out[1].trim(),
            options: {},
            correctanswer: match_out[3].trim(),
            analysis: match_out[4] ? match_out[4].trim() : null, // 解析可能不存在
            // 题目基础信息
            tag: valuetag.value,
            qustore: valuequstore.value,
            question_images: "0",
            answer_images: "0"
        };
        // 匹配所有选项
        const optionsMatch = match_out[2].match(/(A|B|C|D|E|F|G|H|I|J|K|L|M|N)\..+?\n/g);
        if (optionsMatch) {
            optionsMatch.forEach(option => {
                const [letter, text] = option.split('.', 2);
                question.options[letter] = text.trim();
            });
        }
        // 答案是否存在且在选项中
        for (let index = 0; index < question['correctanswer'].length; index++) {
            if (Object.keys(question.options).includes(question['correctanswer'][index])) {
                var panduantemp = 0
                continue
            } else {
                panduantemp = 1
            }
        }
        if (panduantemp == 1) {
            continue
        }
        // 构建题目基础信息
        if (Object.keys(question.options).length == 2) {
            question['qutype'] = '2'
        }
        if (Object.keys(question.options).length >= 4) {
            if (question['correctanswer'].length == 1) {
                question['qutype'] = '0'
            } else {
                question['qutype'] = '1'
            }
        }
        questionList_out.push(question);
    }
    console.log(valuetag.value, valuequstore.value)
    console.log('导入试题:', questionList_out);
    // 如果提交题库为空返回
    if (questionList_out.length === 0) {
        ElMessage({
            type: 'error',
            message: `导入试题为空`,
        });
        return;
    }
    // 向后台提交题目
    await axios.post('http://localhost:8000/api/createquestion/pidao', { data: questionList_out })
    ElMessage({
        type: 'success',
        message: `导入题库成功`,
    })
};
</script>

<style lang="css">
.custom-textarea {
    width: 100%;
    color: red;
}
</style>