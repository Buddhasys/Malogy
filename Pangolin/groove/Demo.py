from locust import HttpUser, task, between, constant
import os
import webbrowser


class Demo(HttpUser):

    wait_time = between(1, 5)  # 3表是每个task间隔3秒

    def on_start(self):
        # 点击开始压测时，所有用户都会去运行一次，如：用做模拟登录，采用self.client模拟登录接口
        print("开始压测")

    def on_stop(self):
        # 点击stop时，所有用户都会去运行一次。
        print("结束压测结束")

    @task(3)  # 需要压测的接口都需要加task，后面的数据为权重，默认权重1
    def function(self):

        data = {}
        url = "http://www.xt-dev.com/sapi/v4/market/public/ticker/24h?symbol=btc_usdt"
        header = {}
        with self.client.get(url) as obj:
            if obj.status_code == 200:
                print("连接成功")
            else:
                print(f"连接失败： {obj.status_code}")



if __name__ == '__main__':
    webbrowser.open_new_tab("http://localhost:8089")
    os.system("locust -f Demo.py --host=http://www.xt-dev.com")




