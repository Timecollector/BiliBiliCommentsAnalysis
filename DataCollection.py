import requests
import time
import re
import csv


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

# 获取bv
def get_vedio_urls(url):
    bvs = []
    oids = []
    html = requests.get(url, headers=headers).json()
    for i in html['data']['list']['vlist']:
        bvs.append(i['bvid'])
        oids.append(i['aid'])
    return bvs, oids

# 获取aid以及cid
def get_video_id(bv):
    url = f'https://www.bilibili.com/video/{bv}'
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'
    content = html.text
    aid_regx = '"aid":(.*?),"bvid":"{}"'.format(url.split('/')[-1])
    cid_regx = '{"cid":(.*?),"page":1'
    aid = re.findall(aid_regx, content)[0]
    cid = re.findall(cid_regx, content)[0]
    return aid, cid


# 获取弹幕
def get_video_danmaku(cid):
    danmaku_url = f'https://comment.bilibili.com/{cid}.xml'
    html = requests.get(danmaku_url, headers=headers)
    html.encoding = 'utf-8'
    content = html.text
    danmaku_regx = re.compile('<d .*?>(.*?)</d>')
    danmaku = danmaku_regx.findall(content)
    f = open(f'{cid}danmaku{time.time()}.csv',mode='w',newline='',encoding='gb18030')
    csvwriter = csv.writer(f)
    count = 0
    try:
        for i in danmaku:
            time.sleep(1)
            csvwriter.writerow([i])
            count += 1
            print(f'已保存{count}条弹幕')
    except:
        f.close()
        print(f'共保存{count}条弹幕')
    f.close()
    print(f'共保存{count}条弹幕')
    pass


# 获取评论
def get_video_comments(aid, page_start=1, page_end=5):
    f = open(f'{aid}comments{time.time()}.csv', mode='w', newline='', encoding='gb18030')
    csvwriter = csv.writer(f)
    count = 0
    try:
        for page in range(page_start, page_end+1):
            time.sleep(4)
            comments_url = f'https://api.bilibili.com/x/v2/reply?pn={page}&type=1&oid={aid}&sort=2'
            html = requests.get(comments_url, headers=headers).json()
            comments = html['data']['replies']
            for i in comments:
                time.sleep(1)
                lt = [i['member']['uname'], i['member']['sex'], i['member']['level_info']['current_level'], i['ctime'], i['content']['message']]
                csvwriter.writerow(lt)
                count += 1
                print(f'已保存{count}条评论')
    except:
        f.close()
        print(f'共保存{count}条评论')
    f.close()
    print(f'共保存{count}条评论')
    pass


if __name__ == '__main__':
    # url = 'https://api.bilibili.com/x/space/arc/search?mid=546195&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'
    # urls, oids = get_vedio_urls(url)
    video_bv = 'BV1p7411Y7BC'
    aid, cid = get_video_id(video_bv)
    # get_video_danmaku(cid)
    get_video_comments(aid, 1, 2000)