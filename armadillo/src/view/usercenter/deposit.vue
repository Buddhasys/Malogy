<template>
  <el-card show="always" class="main-card">
    <el-form :model="form">
      <el-form-item>
        <el-select placeholder="选择环境" size="large" filterable v-model="form.env" style="width: 560px"
                   @change="queryCoin">
          <el-option v-for="item in primEnvList" :value="item.name" :key="item">{{ item.name }}</el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select placeholder="选择币种" size="large" filterable v-model="coinSel" style="width: 560px;"
                   v-show="coinSelShow">
          <el-option v-for="item in coinList" :value="item.coinName" :key="item.coinName">{{
              item.coinName
            }}
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select placeholder="充值账户-默认现货" size="large" filterable v-model="form.toAccountType" style="width: 560px;"
                   v-show="coinSelShow">
          <el-option v-for="item in accountList" :value="item.toAccountType" :label="item.accountName" :key="item.toAccountType">{{
              item.accountName
            }}
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-input size="large" placeholder="UID" v-model="form.UID"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input size="large" placeholder="充值金额" v-model="form.amount"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button class="btn-center" type="success" size="large" round :loading="isLoading" @click="charge">充值
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from "element-plus"
import utils from '../../libs/utils'
import axios from 'axios'
let form = ref({
  env: "test1",
  coinId: "",
  UID: "",
  amount: 100,
  toAccountType: ""
})
let coinSelShow = ref(true)
let bizType = ref("coin")
let isLoading = ref(false)
let coinList = ref([])
let coinSel = ref('')
let primEnvList = utils.primEnvList
let accountList = ref([{
  "accountName":"现货",
  "toAccountType":"1"
},
  // {
  // "accountName":"全仓杠杆",
  // "toAccountType":"10"
// }
])

const charge = () => {
  coinList.value.forEach((element) => {
    if (element.coinName === coinSel.value) {
      form.value.coinId = element.coinId
    }
  });

  isLoading.value = true

  let apiPath = ""
  let postData = {}
  if (bizType.value === 'coin') {
    apiPath = "/api/usercenter/deposit"
    postData = form.value
  } else {
    apiPath = "/proxy/flask/get_user_card"
    let cardType = 0
    if (bizType.value === "deduction") {
      cardType = 1
    }
    if (bizType.value === "experience") {
      cardType = 2
    }
    postData["env"] = form.value.env
    postData["uid"] = form.value.UID
    postData["amount"] = form.value.amount
    postData["tokenid"] = coinSel.value
  }



  axios.post(apiPath, postData).then(resp => {
    // console.log({resp})
    isLoading.value = false
    if (resp.data.code === '0000') {
      ElMessage({
        message: resp.data.msg,
        type: 'success'
      })
    } else {
      ElMessage({
        message: resp.data.msg,
        type: 'error'
      })
    }

  }).catch(error => {
    isLoading.value = false
    ElMessage({
      message: error,
      type: 'error'
    })
  })
}
const queryCoin = (env) => {
  form.value.env = env
  axios
      .get("/api/coinslist", {
        env: env,
      })
      .then((resp) => {
        // console.log({resp})
        coinList.value = resp.data;
      });
}
const bizChange = () => {
  if (bizType.value === 'coin') {
    queryCoin(form.value.env)
    coinSelShow.value = true
  }
  if (bizType.value === 'experience') {
    coinList.value = [
      { "coinName": "USDT", "coinId": "" },
      { "coinName": "USDC", "coinId": "" }]
    coinSelShow.value = true
  }
  if (bizType.value === 'deduction') {
    coinList.value = []
    coinSelShow.value = false
  }
}
onMounted(() => {
  queryCoin('test')
  // axios.get('/build/queryEnvList').then(resp => {
  //     envList.value = resp.data
  // })
  // envList.value = util.env
})
</script>

<style></style>