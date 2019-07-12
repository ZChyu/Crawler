from urllib.request import urlretrieve
# 网络上图片的地址
img_src = 'http://hlj.nongwang.com/extend/image.php?auth=AmNXMQBtVzgMZAEwUzdWZAZoXmEBOA'

# 将远程数据下载到本地，第二个参数就是要保存到本地的文件名
urlretrieve(img_src,'1.jpg')