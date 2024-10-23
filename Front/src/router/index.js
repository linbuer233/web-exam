import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import Login from '@/views/Login.vue'
// 学生
import studentMainpage from '@/views/studentview/studentMainpage.vue'
import studentHomepage from '@/views/studentview/studentHomepage.vue'
import studentExampage from '@/views/studentview/studentExampage.vue'
import studentExamrecordspage from '@/views/studentview/studentExamrecordspage.vue'
import studentQuestionStore from '@/views/studentview/studentQuestionStore.vue'
import studentWrongQu from '@/views/studentview/studentWrongQu.vue'
// 管理员
import adminMainpage from '@/views/admin/adminMainpage.vue'
import adminHomepage from '@/views/admin/adminHomepage.vue'
import adminExampage from '@/views/admin/adminExampage.vue'
import adminExamrecord from '@/views/admin/adminExamrecord.vue'
import adminCreateexam from '@/views/admin/adminCreateexam.vue'
import adminCreatequstore from '@/views/admin/adminCreatequstore.vue'
import adminCreatequlist from '@/views/admin/adminCreatequlist.vue'
import adminUsersetting from '@/views/admin/adminUsersetting.vue'
import adminaddquestion from '@/views/admin/adminaddquestion.vue'
import adminaddquestionpi from '@/views/admin/adminaddquestionpi.vue'
import adminaddquestionsingle from '@/views/admin/adminaddquestionsingle.vue'
// 考试界面
import exampage from '@/views/exam/exampage.vue'
import examprepare from '@/views/exam/examprepare.vue'
import examresult from '@/views/exam/examresult.vue'
// 题库练习
import quPractice from '@/views/qustorepractice/quPractice.vue'
import WrongquPractice from '@/views/qustorepractice/WrongquPractice.vue'

// import axios from 'axios'

const router = createRouter({
  history: createWebHistory(),
  // history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'h',
      redirect: "/login",
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/studentMainpage',
      redirect: '/studentMainpage/home'
    },
    {
      path: '/adminMainpage',
      redirect: '/adminMainpage/home'
    },
    // exampage
    {
      path: "/exam/examprepare",
      name: 'examprepare',
      component: examprepare,
    },
    {
      path: "/exam/exampage",
      name: 'exampage',
      component: exampage,
    },
    {
      path: "/exam/examresult",
      name: 'examresult',
      component: examresult,
    },
    // qustore practice
    {
      path: "/qustore/qustorepractice",
      name: 'qustorepractice',
      component: quPractice,
    },
    {
      path: "/wrongqu/wrongqustorepractice",
      name: 'wrongqustorepractice',
      component: WrongquPractice,
    },
    // admin & student
    {
      path: '/studentMainpage',
      // name: 'studentMainpage',
      component: studentMainpage,
      children: [
        { path: 'home', name: 'studentMainpagehome', component: studentHomepage },
        { path: 'exam', name: 'studentMainpageexam', component: studentExampage },
        { path: 'examrecords', name: 'studentMainpageexamrecords', component: studentExamrecordspage },
        { path: 'questionstore', name: 'studentMainpagequestionstore', component: studentQuestionStore },
        { path: 'wrongquestion', name: 'studentMainpagewrongquestion', component: studentWrongQu },
      ],
    },
    {
      path: '/adminMainpage',
      // name: 'studentMainpage',
      component: adminMainpage,
      children: [
        { path: 'home', name: 'adminMainpagehome', component: adminHomepage },
        { path: 'exam', name: 'adminMainpageexam', component: adminExampage },
        { path: 'examrecords', name: 'adminMainpageexamrecords', component: adminExamrecord },
        { path: 'createexam', name: 'adminMainpagecreateexam', component: adminCreateexam },
        { path: 'createqustore', name: 'adminMainpagecreatequstore', component: adminCreatequstore },
        { path: 'createqulist', name: 'adminMainpagecreatequlist', component: adminCreatequlist },
        { path: 'usersetting', name: 'adminMainpageusersetting', component: adminUsersetting },
        {
          path: 'addquestion', component: adminaddquestion, children: [
            { path: 'pi', name: 'adminaddquestionpi', component: adminaddquestionpi },
            { path: 'single', name: 'adminaddquestionsingle', component: adminaddquestionsingle },
          ]
        },
      ],
    },
    // {
    //   path: '/studentMainpage',
    //   name: 'studentMainpage',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: studentMainpage
    // },

  ]
})

// 导航守卫
// 使用 router.beforeEach 注册一个全局前置守卫，判断用户是否登陆
router.beforeEach(async (to, from) => {
  let token = localStorage.getItem('Authorization');
  var user = localStorage.getItem('user');
  console.log(to.path, from.path, (to.path == '/exam/exampage' && from.path != "/exam/examprepare"))
  if (to.path !== '/login' && !token) {
    return { name: 'login' };
  }
  if (to.path == '/exam/exampage' && from.path == "/exam/examresult") {
    return { path: "/exam/examresult" };
  }
  if (to.path == '/exam/examprepare' && from.path == "/exam/examresult") {
    return { path: "/exam/examresult" };
  }
  if (to.path == '/exam/exampage' && ["/exam/examprepare", '/', "/exam/exampage"].indexOf(from.path) == -1) {
    const role = localStorage.getItem("role")
    sessionStorage.setItem("currpageurl", '2-1')
    if (role == 'admin') {
      return { name: 'adminMainpageexam' };
    } else {
      return { name: 'studentMainpageexam' };
    }
  }
  // 只能从特定页面前往该页面
  if (to.path == '/qustore/qustorepractice' && ['/', '/qustore/qustorepractice', '/studentMainpage/questionstore'].indexOf(from.path) == -1) {
    sessionStorage.setItem("currpageurl", '3')
    return { path: '/studentMainpage/questionstore' }
  }
  if (to.path == '/wrongqu/wrongqustorepractice' && ['/', '/studentMainpage/wrongquestion', '/wrongqu/wrongqustorepractice'].indexOf(from.path) == -1) {
    sessionStorage.setItem("currpageurl", '3')
    return { path: '/studentMainpage/wrongquestion' }
  }
  setTimeout(() => {
    localStorage.removeItem('Authorization');
    localStorage.removeItem('user');
    localStorage.removeItem('role');
  }, 21600000);
});

export default router;