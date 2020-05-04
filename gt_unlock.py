import re,random,os,requests,time
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image;
from io import BytesIO;
class gt_unlock:

    def __init__(self):
        pass

    def getXY(self,a,b):
        '''
        用来获取图片缺块坐标\r\n
        a : 第一张图片\r\n
        b : 第二张图片\r\n
        '''
        img1 = Image.open(a)
        img2 = Image.open(b)
        for xx in range(0,img1.size[0]):
            for yy in range(0,img1.size[1]):
                pixel=img1.load()[xx,yy]
                pixel2=img2.load()[xx,yy]
                if pixel[0] - pixel2[0] >50:
                    return xx,yy
        return None;

    def mergerImagePro(self,data,width,height,draw_width,out_path,out_name,out_end):
        '''
        用来下载合并滑块图片\r\n
        data : 传入网页滑块验证图片链接集合\r\n
        width : 每块图片的宽度\r\n
        height : 每块图片的高度\r\n
        draw_width : 新图片宽度\r\n
        draw_height : 新图片高度\r\n
        out_path : 合并后图片输出路径\r\n
        out_name : 合并后图片输出名字\r\n
        out_end : 图片类型\r\n
        '''
        up=[]
        down=[]
        count=0
        tmp_img_src_link=re.compile("\(&quot;(.+?.webp)").findall(data[0])[0]
        Img=Image.open(BytesIO(requests.get(tmp_img_src_link).content))
        for d in data:
            # print(d)
            img_src_point=re.compile("background-position:(.+?;)").findall(d)[0]
            img_src_point=re.sub("px|;|-","",img_src_point)
            x=int(img_src_point.split(" ")[1])
            y=int(img_src_point.split(" ")[2])
            # print(x,y)
            # nn=img.crop((y,x,x+10,58))
            if y == 0:
                up.append(Img.crop((x,0,x+width,height)))
            else:
                down.append(Img.crop((x,height,x+width,(height+height))))

        # new_img=Image.new('RGB',(draw_width,draw_height))
        new_img=Image.new('RGB',(draw_width,Img.size[1]))
        for u in up:
            new_img.paste(u,(count,height))
            count=count+u.width
        count=0;
        for d in down:
            new_img.paste(d,(count,0))
            count=count+d.width
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        new_img.save(out_path+"/"+out_name+"."+out_end)

    def getGTpoint(self,img1_path,img1_name,img2_path,img2_name):
        '''
        用来获取图片缺块坐标\r\n
        img1_path : 第一张图片保存路径\r\n
        img1_name : 第一张图片名字(可包含后缀，如果没有默认jpg代替)\r\n
        img2_path : 第二张图片保存路径\r\n
        img2_name : 第二张图片名字(可包含后缀，如果没有默认jpg代替)\r\n
        '''
        img1=img1_path+"/"+img1_name;
        img2=img2_path+"/"+img2_name;
        if img1.find(".jpg") == -1:
            img1=img1+".jpg"
        if img2.find(".jpg") == -1:
            img2=img2+".jpg"
        return self.getXY(img1,img2)

    def mergerImage(self,data,width,height,draw_width,out_path,out_name):
        '''
        用来下载合并滑块图片\r\n
        data : 传入网页滑块验证图片链接集合\r\n
        width : 每块图片的宽度\r\n
        height : 每块图片的高度\r\n
        draw_width : 新图片宽度\r\n
        out_path : 合并后图片输出路径\r\n
        out_name : 合并后图片输出名字\r\n
        '''
        self.mergerImagePro(data,width,height,draw_width,out_path,out_name,"jpg");

    def move(self,xy,driver,element,count):
        '''
        用来移动滑块\r\n
        xy : 缺块坐标\r\n
        driver : webdriver\r\n
        element : 滑块元素\r\n
        count : 第几次调用此函数，默认0
        '''
        size=4;
        if count < 5:
            size = size+count;
        x=xy[0]
        tmp=0
        part=2
        ActionChains(driver).click_and_hold(element).perform();
        time.sleep(2)
        while (x-tmp) > size:
            ActionChains(driver).move_by_offset(part,tmp).perform();
            # time.sleep(random.randint(0,1))
            tmp=tmp+1;
            if tmp <= (x/2):
                part=1
            # print(tmp)
            
        ActionChains(driver).release().perform()