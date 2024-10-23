<template>
    <el-row :gutter="20" style="height: 100%;">
        <el-col :span="16">
            <el-card style="min-width: 480px;height:100%">
                <template #header>
                    <div class="card-header">
                        <span>系统信息</span>
                    </div>
                </template>
                <div data-v-106c86ed="" class="title" style="padding-top: 0px;">系统介绍</div>
                基于Fastapi+MongoDB+Vue开发的考试系统。包含在线考试、题库和错题训练、自动算分等考试功能。
                <!-- <template #footer>Footer content</template> -->
            </el-card>
        </el-col>
        <el-col :span="8">
            <el-card style="max-width: 480px;height:100%">
                <template #header>
                    <div class="card-header">
                        <span>支持信息</span>
                    </div>
                </template>
                <span>联系方式:2487296367@qq.com</span>
                <!-- <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p> -->
                <!-- <template #footer>Footer content</template> -->
            </el-card>
        </el-col>
    </el-row>
</template>

<style lang="css">
.title {
    font-size: 18px;
    font-weight: 700;
    padding-bottom: 10px;
    padding-top: 20px;
    margin-bottom: 10px;
    border-bottom: #eee 1px dotted;
}
</style>