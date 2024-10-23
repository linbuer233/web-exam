<template>
    <el-main style="height: 100%;">
        <div>
            <p>试题类型</p>
            <el-radio-group v-model="radio" @change="raidochange">
                <el-radio :value="0">单选题</el-radio>
                <el-radio :value="1">多选题</el-radio>
                <el-radio :value="2">判断题</el-radio>
            </el-radio-group>
        </div>
        <div>
            <p>试题题目</p>
            <QuillEditor ref="quillEditRef" :toolbar="toolbarOptions" theme="snow" @focus="onEditfocus"
                @blur="onEditblur" @ready="onEditready" />
        </div>
        <div>
            <p>试题选项</p>
            <div v-if="isPanduan">
                <div v-for="(i, index) in quillEditRefList" :key="index">
                    <div>
                        <el-row style="margin-bottom: 30px;">
                            <el-col :span="1">
                                <p style="text-align: center;">{{ i[1] }}、</p>
                            </el-col>
                            <el-col :span="20">
                                <QuillEditor :ref="i[0]" :toolbar="toolbarOptions" theme="snow"
                                    @ready="() => onEditready1(i[0], index)" @blur="() => onEditblur1(i[0], index)"
                                    @focus="() => onEditfocus1(i[0], index)" />
                            </el-col>
                            <el-col :span="3">
                                <el-button type="primary" :icon="Delete" circle @click="deletexuanX"
                                    style="margin-top: 5px;margin-left:12px" />
                            </el-col>
                        </el-row>
                    </div>
                </div>
                <el-button size="small" type="primary" @click="addxuanX" style="margin-top: -30px;">
                    <span>增加选项</span>
                </el-button>
            </div>
            <div v-else>
                <el-radio-group v-model="radiopanduan" @change="raidochange">
                    <el-text>A、 正确</el-text>
                    <el-text style="margin-left: 20px;">B、 错误</el-text>
                </el-radio-group>
            </div>
        </div>
        <div>
            <p>解析</p>
            <el-input v-model="analysisinput" style="width: 240px" :rows="2" type="textarea" placeholder="" />
        </div>
        <div>
            <p>答案</p>
            <el-radio-group v-if="isRadio" v-model="value">
                <el-radio :value="index" v-bind:key="index" v-for="(i, index) in Editoption">{{
                    i }}</el-radio>
            </el-radio-group>
            <el-checkbox-group v-else v-model="valued">
                <el-checkbox :value="index" v-bind:key="index" v-for="(i, index) in Editoption">{{ i }}</el-checkbox>
            </el-checkbox-group>
        </div>
        <!-- footer -->
        <el-select v-model="valuetag" filterable allow-create default-first-option :reserve-keyword="false"
            placeholder="无标签" style="width: 140px;margin-top:10px;margin-right:10px;height:30px">
            <el-option v-for="item in optionstag" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-select v-model="valuequstore" filterable allow-create default-first-option :reserve-keyword="false"
            placeholder="默认题库" style="width: 140px;margin-top:10px;margin-right:10px;height:30px">
            <el-option v-for="item in optionsqustore" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-button size="small" type="primary" @click="addsinglequestion" style="margin-top: 12px; height: 30px">
            <span>导入试题</span>
        </el-button>
    </el-main>
</template>

<script lang="js" setup>
import axios from 'axios'
import { computed, defineProps, ref } from 'vue'
import { ElMessage } from 'element-plus';
import {
    Delete
} from '@element-plus/icons-vue'
const analysisinput = ref('')
const radio = ref(0)
const isRadio = ref(true);
const isPanduan = ref(true);
const value = ref(null); // 默认选中选项A
const valued = ref([]); // 默认选中选项A
const ABCList = ref(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
const Editoption = ref(['A', 'B', 'C', 'D'])
const quillEditRefList = ref([])

const valuetag = ref('无标签')
const valuequstore = ref('默认题库')
const optionsqustore = [{ value: "默认题库", label: "默认题库" }];
const optionstag = [{ value: "无标签", label: "无标签" }];

// 父组件传值
const msgpanduan = ref(0) // 防止quill多次赋值，只有点修改的时候赋值
const props = defineProps({ msg: ref(null) });
// 用computed使用props
const msg = props.msg;
const msgoption = msg.options
const msgquestion = msg.question
const xuannum = Object.keys(msg.options).length
Editoption.value = ABCList.value.slice(0, xuannum)
const tixlist = { "选择题": 0, "多选题": 1, "判断题": 2 }
radio.value = tixlist[msg.qutype]

if (msg.qutype == '多选题') {
    valued.value = []
    for (let index = 0; index < msg.correctanswer.length; index++) {
        valued.value.push(Editoption.value.indexOf(msg.correctanswer[index]));
    }
    isRadio.value = false;
} else {
    value.value = Editoption.value.indexOf(msg.correctanswer);
    // isRadio.value = true;
}


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

const raidochange = () => {
    value.value = null
    valued.value = []
    msgpanduan.value = 0
    if (radio.value == 1) {
        isRadio.value = false;
    } else {
        isRadio.value = true;
    }
    if (radio.value == 2) {
        isPanduan.value = false;
        Editoption.value = ['A', 'B'];
    } else {
        isPanduan.value = true;
        // Editoption.value = ['A', 'B', 'C', 'D']
        quillEditRefList.value = []
        for (let index = 0; index < Editoption.value.length; index++) {
            const temp = ref(null)
            quillEditRefList.value.push([temp, Editoption.value[index]])
        }
    }
}


// quill-editor
const quillEditRef = ref(null);
const toolbarOptions = ref(['bold', 'italic', 'underline', 'image'])
const onEditfocus = () => {
    const editor = quillEditRef.value;
    editor.getToolbar().style.display = 'block';
}

const onEditblur = () => {
    const editor = quillEditRef.value;
    editor.getToolbar().style.display = 'none';
}
const onEditready = () => {
    const editor = quillEditRef.value;
    editor.getToolbar().style.display = 'none';
    if (msgpanduan.value == 0) {
        if (msg.answer_images == '0') {
            editor.setContents([
                { insert: msgquestion },
            ]);
        } else {
            editor.setContents([
                { insert: msgquestion },
            ]);
        }
    }

}

for (let index = 0; index < Editoption.value.length; index++) {
    const temp = ref(null)
    quillEditRefList.value.push([temp, Editoption.value[index]])
}
const onEditready1 = (reftemp, index) => {
    const editor = reftemp.value[0];
    editor.getToolbar().style.display = 'none';
    if (msgpanduan.value == index) {
        console.log(msg.answer_images[Editoption.value[index]])
        if (msg.answer_images == '0') {
            editor.setContents([
                { insert: msgoption[Editoption.value[index]] },
                // { image: msg.answer_images[Editoption.value[index]][0] }
            ]);
        } else {
            editor.setContents([
                { insert: msgoption[Editoption.value[index]] },
                // { image: msg.answer_images[Editoption.value[index]][0] }
            ]);
        }
        msgpanduan.value += 1;
    }
}
const onEditblur1 = (reftemp, index) => {
    const editor = reftemp.value[0];
    editor.getToolbar().style.display = 'none';
}
const onEditfocus1 = (reftemp, index) => {
    const editor = reftemp.value[0];
    editor.getToolbar().style.display = 'block';
}
//增加选项
const addxuanX = () => {
    Editoption.value.push(ABCList.value[Editoption.value.length])
    const temp = ref(null)
    quillEditRefList.value.push([temp, Editoption.value[Editoption.value.length - 1]])
}
const deletexuanX = () => {
    Editoption.value.pop()
    quillEditRefList.value.pop()
}
//导入试题
const addsinglequestion = async () => {
    console.log('导入试题');
    var msg_xuan = 1
    if (radio.value == 0 || radio.value == 1) {
        //题干
        const tigan = quillEditRef.value.getContents().ops
        var question_imageslist = []
        var question_tigan = ''
        for (let index = 0; index < tigan.length; index++) {
            const element = tigan[index].insert;
            if (element.image == undefined) {
                question_tigan += element
                continue
            }
            question_imageslist.push(element.image)
        }
        //选项
        var xuanX_imageslist = {}
        var xuanX_options = {}
        for (let index = 0; index < quillEditRefList.value.length; index++) {
            const temp = quillEditRefList.value[index][0];
            var xuanX = temp.value[0].getContents().ops
            var xuanX_textContent = ''
            var xuanX_imageslist_sub = []
            for (let index = 0; index < xuanX.length; index++) {
                const element = xuanX[index].insert;
                if (element.image == undefined) {
                    xuanX_textContent += element.replace('\n', '')
                    continue
                }
                xuanX_imageslist_sub.push(element.image)
            }
            if (xuanX_textContent == '\n') {
                msg_xuan = 0
            }
            const xuanX_textContent1 = xuanX_textContent
            xuanX_options[Editoption.value[index]] = xuanX_textContent1
            xuanX_imageslist[Editoption.value[index]] = xuanX_imageslist_sub
        }
        //答案
        var answer = ''
        if (radio.value == 1) {
            for (let index = 0; index < valued.value.length; index++) {
                answer += Editoption.value[valued.value[index]]
            }
        } else {
            answer += Editoption.value[value.value]
        }
    } else {
        //题干
        const tigan = quillEditRef.value.getContents().ops
        var question_imageslist = []
        var question_tigan = ''
        for (let index = 0; index < tigan.length; index++) {
            const element = tigan[index].insert;
            if (element.image == undefined) {
                question_tigan += element
                continue
            }
            question_imageslist.push(element.image)
        }
        // 选项
        var xuanX_options = {}
        xuanX_options['A'] = '正确'
        xuanX_options['B'] = '错误'
        var answer = ''
        answer += Editoption.value[value.value]
    }
    //判断题干
    if (question_tigan == '\n') {
        ElMessage({
            type: 'error',
            message: `题干为空`,
        });
        return
    }
    // 判断选项
    if (msg_xuan == 0) {
        ElMessage({
            type: 'error',
            message: `选项为空`,
        });
        return
    }
    // 判断答案
    if (answer == 'undefined' || answer == '') {
        ElMessage({
            type: 'error',
            message: `答案为空`,
        });
        return
    }
    // 整理成json
    const questiondict = {
        question: question_tigan.replace('\n', ''),
        options: xuanX_options,
        correctanswer: answer,
        analysis: analysisinput.value.replace('\n', ''),
        //基本信息
        tag: valuetag.value,
        qustore: valuequstore.value,
        question_images: question_imageslist,
        answer_images: xuanX_imageslist,
        qutype: String(radio.value)
    }
    console.log('最终试题')
    console.log(questiondict)
    // 如果提交题库为空返回
    if (questiondict.length === 0) {
        ElMessage({
            type: 'error',
            message: `导入试题为空`,
        });
        return;
    }
    // 向后台提交题目
    await axios.post('http://localhost:8000/api/createquestion/update_singledao', {
        data: questiondict,
        uid: msg.uid,
    })
    ElMessage({
        type: 'success',
        message: `导入题库成功，请保存退出`,
    })
}
</script>

<style lang="css">
.ql-container.ql-snow {
    border: 1px solid #ccc !important;
}
</style>