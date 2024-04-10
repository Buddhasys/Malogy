<template>
  <el-card show="always" class="main-card">
    <el-form :model="form">
      <el-form-item>
        <el-radio-group v-model="form.system" @change="typeChange">
          <el-radio-button size="large" label="future">合约</el-radio-button>
          <el-radio-button size="large" label="spot">币币</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-radio-group v-model="form.times">
          <el-radio size="large" label="1">1次</el-radio>
          <el-radio size="large" label="10">10次</el-radio>
          <el-radio size="large" label="100">100次</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-select placeholder="选择环境" size="large" filterable v-model="form.env" style="width: 450px">
          <el-option v-for="item in primEnvList" :value="item.url">{{ item.name }}</el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-select v-model="form.symbol" size="large" style="width: 450px;" filterable allow-create
                   placeholder="选择交易对">
          <el-option v-for="item in codeList" :value="item.name" :key="item.name">{{ item.name }}</el-option>
        </el-select>
      </el-form-item>
      <el-form-item >
        <el-input v-model="form.quantity" size="large" placeholder="自定义铺单数量-默认随机" style="width: 450px;"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button class="btn-center" type="warning" size="large" @click="order" :loading="isLoading">开始铺单
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>
<script setup>
import utils from "../../libs/utils";
import axios from 'axios'
import { ref, onMounted } from 'vue'
let form = ref({
  env: "test",
  symbol: "",
  system: "spot",
  times: "1",
  quantity: "0",
})
let codeList = ref([
  { "name": "BTCUSDT" },
  { "name": "BTCUSD" },
  { "name": "SBTCSUSDT" },
  { "name": "ETHUSDT" },
  { "name": "ETHUSD" },
  { "name": "ETHPERP" }
])
let isLoading = ref(false)
let primEnvList = utils.primEnvList
const order = () => {
  isLoading.value = true
  axios.post(utils.baseURL+'/quotation/orderBooks', form.value).then(resp => {
    setTimeout(() => {
      isLoading.value = false
    }, 5000);
  })
}
const typeChange = () => {
  form.value.symbol = ""
  if (form.value.system === 'spot') {
    codeList.value = [
      { "name": "BTCUSDT" },
      { "name": "BTCETH" },
      { "name": "ETHUSDT" },
      { "name": "ETHBTC" },
      { "name": "BGBUSDT" },
      { "name": "BGBUSDC" },
      { "name": "ETHBGB" }
    ]
  } else {
    codeList.value = [
      { "name": "BTCUSDT" },
      { "name": "BTCUSD" },
      { "name": "SBTCSUSDT" },
      { "name": "ETHUSDT" },
      { "name": "ETHUSD" },
      { "name": "ETHPERP" }
    ]
  }
}
onMounted(() => {
  // axios.get('/build/queryEnvList').then(resp => {
  //     primEnvList.value = resp.data
  // })
})
</script>

<style></style>