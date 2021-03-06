import os

# 平台
PLATFORM = 'Android'

PLATFORM_VERSION = '11.0'

# 设备名称 通过 adb devices -l 获取
DEVICE_NAME = 'MI 10 Pro'

# APP路径
APP = os.path.abspath('.') + '/weixin.apk'

# APP包名
APP_PACKAGE = 'com.tencent.mm'

# 入口类名
APP_ACTIVITY = '.ui.LauncherUI'

# Appium地址
DRIVER_SERVER = 'http://localhost:4723/wd/hub'
# 等待元素加载时间
TIMEOUT = 30

# 微信手机号密码
USERNAME = ''
PASSWORD = ''

# 滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 1000

# MongoDB配置
MONGO_URL = 'localhost'
MONGO_DB = 'moments'
MONGO_COLLECTION = 'moments'

# 滑动间隔
SCROLL_SLEEP_TIME = 1
