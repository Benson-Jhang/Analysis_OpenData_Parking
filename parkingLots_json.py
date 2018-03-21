# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import json
import urllib.request
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Read file
    saveDirectory = os.getcwd()
    filename = 'parkingLot.json'
    filepath = saveDirectory + '\\' + filename

    output_json = json.load(open(filepath,'r',encoding='utf-8'))
    output_json = output_json['parkingLots']
    df_file = pd.DataFrame.from_dict(output_json,orient='columns')
    #print(df_file)

    # df = pd.read_json(filepath, encoding="utf-8",orient= 'list')
    # print(df)

    # Read URL directly
    with urllib.request.urlopen("http://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=f4cc0b12-86ac-40f9-8745-885bddc18f79&rid=0daad6e6-0632-44f5-bd25-5e1de1e9146f") as url:
        data = json.loads(url.read().decode())
        data = data['parkingLots']
        org_df= pd.DataFrame.from_dict(output_json, orient='columns')
        df= org_df.loc[:, ['areaName','parkName','totalSpace','surplusSpace']] # 保留所需要的欄位
        df['surplusSpace']= df['surplusSpace'].replace(['車位已滿','暫停開放'],['0','0']) #整理資料
        df['surplusSpace'] = np.where(df['surplusSpace'] == '開放中', df['totalSpace'], df['surplusSpace']) #整理資料
        df2 = df.loc[df['areaName'].isin(['桃園區'])]
        df2['surplusSpace'] = df2['surplusSpace'].astype(int)

        #df2 = df2.loc[:, ['parkName', 'totalSpace', 'surplusSpace']]  # 保留所需要的欄位
        print(df2)

        #畫長條圖
        fig, axes = plt.subplots(nrows=1, ncols=1)
        fig.tight_layout()
        df2[['totalSpace', 'surplusSpace']].plot(ax=axes, kind='bar', stacked=False, width=0.7,
                                                                       title="停車位數量", figsize=(15, 10), legend=True,
                                                                       fontsize=10)
        axes.set_xticklabels(df2.parkName)

        axes.set_xlabel("地區", fontsize=12)
        axes.set_ylabel("停車位數量", fontsize=12)

        height = 1.005
        for p in axes.patches:
            # height += 0.02
            axes.annotate(str(round(p.get_height())), (p.get_x() * 1.005, p.get_height() * height), va='bottom')

        plt.subplots_adjust(wspace=0, hspace=1)
        plt.show()
