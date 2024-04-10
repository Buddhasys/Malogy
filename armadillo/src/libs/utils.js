import router from '../router'

let util = {
};
util.baseURL = "/api"   // 本地调试使用
// util.baseURL = "http://XXXX.grateway.com"   // 上线实际地址
// 主站环境列表
util.primEnvList = [
    {name: "dev", url: 'http://www.baidu.com'},
    {name: "test", url: 'http://www.sohu.com'},
    {name: "pre", url: 'http://www.google.com'},
    {name: "prod", url: 'http://www.music.com'},
]
//管理后台环境列表
util.adminEnvList = [
    {name: "dev", url: 'http://www.admin1.com'},
    {name: "test", url: 'http://www.admin2.com'},
    {name: "pre", url: 'http://www.admin3.com'},
    {name: "prod", url: 'http://www.admin4.com'},
]

// 跟单类型
util.copyType = [
    { value: 'future', label: '合约跟单' },
    { value: 'spot', label: '现货跟单' }
]

// 账户类型
util.accountType = [
    { value: 'mobile', label: '手机号' },
    { value: 'email', label: '邮箱' }
]

// 策略类型
util.strategyType = [
    { value: 'spotGrid', label: '现货网格' },
    { value: 'futureGrid', label: '合约网格' }
]

util.getLoginName = function () {
    // let loginName = cookies.get("account");
    let loginName = "dha123";
    if (loginName == undefined) {
        sessionStorage.setItem('index', '0')
        if (this.isOkta) {
            location.replace('https://www.abc.com')
        } else {
            router.push('/login')
        }

    }
    return loginName
};
util.formatDate = function (date) {
    let m = date.getMonth() + 1
    let d = date.getDate()
    m = m < 10 ? "0" + m : m
    d = d < 10 ? "0" + d : d
    return date.getFullYear() + '-' + m + '-' + d + ' ' + date.getHours() +
        ":" + date.getMinutes() + ":" + date.getSeconds()
}


export default util;
