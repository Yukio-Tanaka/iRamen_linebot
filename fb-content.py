import pandas as pd
f = open('1_fb_crawling.txt', 'r', encoding='utf8')
shop_count = 0
ramen_list = []
ramen_shop_list = []
ramen_name_list = []
ramen_review_list = []
unorganized_shops = []
unorganized_unorganized_shops = []
temp_s = ''
ramen_list_group = []
for line in f:
    line = line.strip()
    #### add endpoint and startpoint to items for striping later
    #### catch 店家:(first item of each sublist) to % for 店名
    #### catch G to Z, if not Z catch to the first 0
    start_point = line.replace('… 更多','').replace(' ','').replace('$','').replace('%','')\
                    .replace('／','').replace('區域','').replace('：',':').replace(':',':')\
                    .replace('店家:','$店家:')\
                    .replace('▎店家:','$店家:').replace('▎店　　名:','$店家:')\
                    .replace('店名:','$店家:').replace('▎店　　家:','$店家:')\
                    .replace('【店家】','$店家:').replace('店家名稱:','$店家:')\
                    .replace('■店家資訊:','$店家:')\
                    .replace('鄰近地點','%鄰近地點').replace('臨近地點:','%鄰近地點:')\
                    .replace('鄰近地區','%鄰近地點').replace('鄰近:','%鄰近地點:')\
                    .replace('拉麵名稱','%.G拉麵名稱').replace('餐點名稱:','%.G拉麵名稱')\
                    .replace('餐點:','%.G拉麵名稱').replace('拉麵品項:','%.G拉麵名稱')\
                    .replace('品項:','%.G拉麵名稱').replace('品名:','%.G拉麵名稱')\
                    .replace('名稱:','%.G拉麵名稱').replace('品項價格:','%.G拉麵名稱')\
                    .replace('配置:','Z配置').replace('配　　置','Z配置')\
                    .replace('\'','').replace('Description','')\
                    .replace('_','').replace('分隔線','')\
                    .replace('▎','').replace('🁢',' ').replace('-','').replace('◎','')\
                    .replace('【',' ').replace('】',':')
    # print(start_point)
    #### replace \u3000 doesnt work
    #### devide all the stores and store them in a list
    for w in start_point:
        temp_s += w
        if w == '$':
            ramen_list.append(temp_s)
            temp_s = ''
# print(ramen_list)

#### first filtering:put items with all the startpoint and endpoint to lists
#### if not sufficient then put into unorganized_shops list
for shops in ramen_list:
    if ('%'not in shops or 'G' not in shops or 'Z' not in shops\
        or shops.index('Z')>shops.index('G')+80) :
        unorganized_shops.append(shops)
    else:
        ramen_shop_list.append(shops[:shops.index('%')])
        ramen_name_list.append(shops[shops.index('G')+1:shops.index('Z')])
        ramen_review_list.append(shops[shops.index('Z')+1:shops.index('Z')+265]+'...')
# print(ramen_shop_list)
# print(ramen_name_list)
# print(ramen_review_list)
# print(ramen_list)

#### second filtering
for shops in unorganized_shops:
    if ('G' in shops and '0' in shops):
        ramen_shop_list.append(shops[:shops.index('%')])
        ramen_name_list.append(shops[shops.index('G')+1:shops.index('G')+21])
        ramen_review_list.append(shops[shops.index('G')+19:shops.index('G')+285]+'...')

    else:
        unorganized_unorganized_shops.append(shops)

#### debug
# print(len(unorganized_unorganized_shops))
# print(unorganized_unorganized_shops)
# print(len(ramen_shop_list))
# print(len(ramen_name_list))
# print(len(ramen_review_list))
print(ramen_shop_list)
print(ramen_name_list)
print(ramen_review_list)#cut the last 2 words and add ...

# print(ramen_name_list.index("拉麵名稱價格:濃厚雞白湯拉麵雞腿捲230"))
# print(ramen_shop_list.index('店家:樂趣Lovecheers'))

####csv
df = pd.DataFrame(list(zip(*[ramen_shop_list, ramen_name_list, ramen_review_list])))
col_names = ['stores', 'ramens', 'reviews']
df.columns = col_names
df.to_csv('fb_crawling.csv', index=True)
