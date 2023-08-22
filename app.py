import uiautomator2 as u2
d = u2.connect() # connect to device

# https://github.com/openatx/uiautomator2
# UiAutomator是Google提供的用来做安卓自动化测试的一个Java库，基于Accessibility服务。功能很强，可以对第三方App进行测试，获取屏幕上任意一个APP的任意一个控件属性，并对其进行任意操作，但有两个缺点：1. 测试脚本只能使用Java语言 2. 测试脚本要打包成jar或者apk包上传到设备上才能运行。

# 我们希望测试逻辑能够用Python编写，能够在电脑上运行的时候就控制手机。这里要非常感谢 Xiaocong He (@xiaocong)，他将这个想法实现了出来（见xiaocong/uiautomator），原理是在手机上运行了一个http rpc服务，将uiautomator中的功能开放出来，然后再将这些http接口封装成Python库。 因为xiaocong/uiautomator这个库，已经很久不见更新。所以我们直接fork了一个版本，为了方便做区分我们就在后面加了个2 openatx/uiautomator2

# 除了对原有的库的bug进行了修复，还增加了很多新的Feature。主要有以下部分：

# 设备和开发机可以脱离数据线，通过WiFi互联（基于atx-agent）
# 集成了openstf/minicap达到实时屏幕投频，以及实时截图
# 集成了openstf/minitouch达到精确实时控制设备
# 修复了xiaocong/uiautomator经常性退出的问题
# 代码进行了重构和精简，方便维护
# 实现了一个设备管理平台(也支持iOS) atxserver2
# 扩充了toast获取和展示的功能
# 这里要先说明下，因为经常有很多人问 openatx/uiautomator2 并不支持iOS测试，需要iOS自动化测试，可以转到这个库 openatx/facebook-wda。

# PS: 这个库 https://github.com/NeteaseGame/ATX 目前已经不维护了，请尽快更换。

# 这里有一份快速参考，适合已经入门的人 QUICK REFERENCE GUIDE，欢迎多提意见。

def foundAboutThisApp():
  loop = 0
  while loop < 10:
    for elem in d.xpath("//android.widget.TextView").all():
        print("Text:", elem.text)
        if elem.text == 'About this app':
          # click
          elem.click()
          # d.xpath("//*[@text='About this app']").click()
          return
    loop += 1
    d(scrollable=True).scroll(steps=100)

def foundAppSize():
  appSize = ''
  found = False
  loop = 0
  # foreach elements
  while loop < 10:
    # scroll to page bottom
    d(scrollable=True).fling.vert.forward()
    for elem in d.xpath("//android.widget.TextView").all():
        print("Text:", elem.text)
        if elem.text == 'Download Size':
          found = True
        elif found:
          found = False
          split = elem.text.split(' ')
          appSize = split[0]
          print(split)
          return appSize
    loop += 1

def startApp():
  # com.android.vending/.AssetBrowserActivity
  d.app_start("com.android.vending", ".AssetBrowserActivity")
  d.app_wait("com.android.vending")

def stopApp():
  d.app_stop("com.android.vending")

# launch app
startApp()

# foreach package name
packages = ["com.zzkko", "com.einnovation.temu"]
for package in packages:

  d.open_url("https://play.google.com/store/apps/details?id=" + package)

  # found about this app
  foundAboutThisApp()

  # found app size
  foundAppSize()

stopApp()
