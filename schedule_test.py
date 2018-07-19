# coding:utf-8

import time
import schedule

def remind(msg):
    print(msg)
    
    
def main():
    schedule.every().friday.at("0:25").do(remind, "ゴミ出し行こうね")
    while True:
        schedule.run_pending()
        print("まだ時間じゃない")
        time.sleep(1)
        
        
if __name__ == "__main__":
    main()
    
