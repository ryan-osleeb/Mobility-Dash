import requests

#url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=6d352e35dcffafce"
url = 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=7d0cb7d254d29111'

r = requests.get(url)
url_content = r.content
csv_file = open('go_downloaded.csv', 'wb')
csv_file.write(url_content)
csv_file.close()