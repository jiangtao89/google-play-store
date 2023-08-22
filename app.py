import uiautomator2 as u2
d = u2.connect() # connect to device

def foundAboutThisApp():
  loop = 0
  while loop < 10:
    for elem in d.xpath("//android.widget.TextView").all():
        print("Text:", elem.text)
        if elem.text == 'About this app':
          print("Found!!!")
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
