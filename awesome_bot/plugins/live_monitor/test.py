import  logging
logging.basicConfig(level=logging.INFO,   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
from core.douyinliverecorder import spider
def is_liver_living(id, record_url):
    logging.info(f"id:{id} 获取直播状态")
    try:
        json_data = {}
        # 1.斗鱼
        if record_url.find("https://www.douyu.com")>-1:
            json_data = spider.get_douyu_info_data(
                url=record_url,
                cookies='')

        # 2.b站
        elif record_url.find("https://live.bilibili.com/")>-1:
            json_data = spider.get_bilibili_room_info(
                url=record_url,
                cookies='')
            json_data['is_live']=json_data["live_status"]
        else:
            logging.info(f"id:{id} 不支持的直播平台")
        return  json_data['is_live']
    except Exception as e:
        logging.exception(f"id:{id} 获取直播状态失败")
        return False
if __name__ == '__main__':
    print(is_liver_living(1,"https://live.bilibili.com/84074"))
