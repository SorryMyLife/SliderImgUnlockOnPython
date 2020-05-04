import random
from selenium import webdriver;
from selenium.webdriver.chrome.options import Options
import time,re;
from gt_unlock import gt_unlock;
gt = gt_unlock();

def t(driver,count):
    driver.find_element_by_css_selector("[class='gt_refresh_button']").click()
    time.sleep(2)
    img_path="C:\\Desktop\\";
    img1_name="test";
    img2_name="test-1";
    data=driver.page_source
    tdata= re.compile("gt_cut_fullbg gt_show(.+?gt_flash)").findall(data)
    tdata=re.compile("gt_cut_fullbg_slice(.+?</div)").findall(tdata[0]);
    w=10
    h=58
    # draw_h=img.size[1]
    draw_w=260
    gt.mergerImage(tdata,w,h,draw_w,img_path,img1_name)
    tdata= re.compile("gt_cut_bg gt_show(.+?gt_slic)").findall(data)
    tdata=re.compile("gt_cut_bg_slice(.+?</div)").findall(tdata[0]);
    gt.mergerImage(tdata,w,h,draw_w,img_path,img2_name)
    gt.move(gt.getGTpoint(img_path,img1_name,img_path,img2_name),driver,driver.find_element_by_css_selector("[class='gt_slider_knob gt_show']"),count)
    time.sleep(random.randint(2,3))
    page=driver.page_source+"";
    if page.find("怪物吃了") != -1 or page.find("验证失败") != -1:
        count = count +1;
        time.sleep(3)
        t(driver,count)
    elif page.find("请关闭验证重试") != -1:
        driver.quit()
        run();
    else:
        return page+"";
        

def run():
    chrome_driver="F:\\新建文件夹\\chromedriver_win32\\chromedriver.exe"
    driver= webdriver.Chrome(executable_path=chrome_driver);
    driver.get("https://www.huxiu.com/")
    time.sleep(3)
    driver.find_element_by_css_selector("[class='avatar']").click()
    time.sleep(2)
    driver.find_element_by_css_selector("[class='login-input-box']").click()
    # time.sleep(2)
    driver.find_element_by_css_selector("[class='login-input login-input-phone']").send_keys('15179966934')
    time.sleep(2)
    driver.find_element_by_css_selector("[class='hx-button login-input login-button hx-btn-default login-button--active']").click();
    time.sleep(2)
    if t(driver,0).find("button-disable") != -1:
        driver.quit()
    else:
        driver.quit()
        run();
# run()
img_path="C:\\Desktop\\";
img1_name="test";
img2_name="test-1";
print(gt.getGTpoint(img_path,img1_name,img_path,img2_name))

