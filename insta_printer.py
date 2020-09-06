
from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings
import sys
import argparse


def usage():
    return """
        python3 insta_printer.py -s1 5 
        python3 insta_printer.py -n 20 -s2 3
        python3 insta_printer.py -n 100 -s1 10 -s2 10 -s3 100

        The default number : -n 60 -t shopping -s1 4 -s2 4 -s3 50
    """

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Crawler", usage=usage())

    parser.add_argument("-n", "--number", type=int, default = 60, help="number of returned posts")
    parser.add_argument("-t", "--tag", type = str, default = "shopping", help="instagram's tag name")
    parser.add_argument("-s1", "--sleep1", type = int, default = "4", help="sleep after making sample mask")
    parser.add_argument("-s2", "--sleep2", type = int, default = "4", help="sleep after making text")
    parser.add_argument("-s3", "--sleep3", type = int, default = "50", help="sleep before printing")
    args = parser.parse_args()

    sleep_list = [args.sleep1,args.sleep2,args.sleep3]
    ins_crawler = InsCrawler(has_screen=True)

    while(True) : 
        try:
            ins_crawler.get_latest_posts_by_tag(args.tag, args.number,sleep_list)
        except :
            print("[Error] restart crawlinng & visualization")
            break
    
        



