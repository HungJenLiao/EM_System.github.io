def data_cleaning(df):
    #處理缺失值
    df.fillna("0", inplace = True)
    #處理時間格式
    df_time = df["案發日期"]
    # df_time_num = df_time.count()
    context = []

    for index, single_time in enumerate(df_time):
        if single_time == "0":
            single_time = '9999/12/31 12:12:12'
        single_time = single_time.replace("/", "-")
        context.append(single_time)
    df["案發日期"] = context
    
    return df

###########################
#1. login google rechapta OK
#   Record UUID OK
#2. 使用者編輯案件function  DELETE
#   register bootstrape OK
#3. dashboard統計圖表 bootstrape OK
#4. message.html and message bootstrape OK
#   message in login and register page
#4. third party google API
#5. 自我介紹1分鐘雨1分半鐘
#6. 頭10家履歷
###########################