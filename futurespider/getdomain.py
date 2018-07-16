import re
import urllib.parse

job = input('请输入搜索职位名称：')
wd = {"":job}
en_job = urllib.parse.urlencode(wd)
jobs = en_job.split("=")[-1]
re_job = re.sub("%","%25",jobs)
front = "https://search.51job.com/list/180200,000000,0000,00,9,99,"
behind = ",2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
print(front + re_job + behind)