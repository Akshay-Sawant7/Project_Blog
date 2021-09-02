import sys

import requests
import json
import os
import time

expiry_changes = ['OCT','SEP']

available_segment = ['nse_index', 'nse_eq', 'ncd_fo', 'nse_fo', 'bse_index', 'bse_eq', 'bcd_fo', 'mcx_index',
                     'mcx_fo']


symbol_changes = {'BAJAJ_AUTO':'BAJAJ-AUTO', 'MCDOWELL_N':'MCDOWELL-N', 'M_M':'M&M', 'L_TFH':'L&TFH',
                  'BANKNIFTY_I': 'BANKNIFTY1', 'BANKNIFTY1I': 'BANKNIFTY2', 'BANKNIFTY2I':'BANKNIFTY3',
                  'NIFTY_I':'NIFTY1', 'NIFTY1I':'NIFTY2', 'NIFTY2I':'NIFTY3'}

def remove_extra(dir_path):
    directory = dir_path
    os.chdir(directory)

    for filename in os.listdir():
        # new_directory = directory + "\" + str(filename) + '\Contract Futures'
        # new_directory = "{}\{}\Contract Futures".format(directory,filename)
        new_directory = "{}\{}\Continuous Futures".format(directory, filename)
        print("WE ARE HERE: {}".format(new_directory))
        try:
            os.chdir(new_directory)
        except Exception as e:
            print(e)
            pass
        for value in expiry_changes:
            for extrafiles in os.listdir():
                if extrafiles.__contains__(value):
                    os.remove(extrafiles)



def change_file_names():
    for key, value in symbol_changes.items():
        for filename in os.listdir():
            # print("{} - {}".format(filename[:-4], key))
            if filename.__contains__(key):
                new_file = filename.replace(key,value)
                os.rename(filename, new_file)


def upload_market_data(dir_path, token):
    try:
        # login_url = "https://api.keev.tech:8001/api/user/v2/login/"
        # # upload_url = "https://chakravyuh.in:8001/candlestick/upload/"
        # # Enter email and password of admin for file upload
        # username = 'info@keev.co.in'
        # password = 'keev1234'
        # result = requests.post(login_url, data={'email': username, 'password': password}, verify=False)
        # if result.status_code != 200:
        #     return f"Error while loging. Error text is {result.text}"
        #
        # token = json.loads(result.text)['data']['token']

        upload_url = "https://api.keev.tech:8001/candlestick/upload/"
        segment = 'nse_index'
        if segment not in available_segment:
            return f"{segment} is not a valid segment. Please enter segment from the give list {available_segment}"
        data = {'segment': segment}
        headers = {
            'Authorization': f'JWT {token}',
        }
        # Change directory acc to your folder location
        # [For dynamic we can set folder path and add folder by date and we can use os.walk to get data of current day]
        directory = dir_path
        # print(dir_path)
        # os.chdir(directory)
        dict_data = {'success_symbol': [], 'duplicate_data_symbol': [], 'invalid_data_in_symbol': [],
                     'not_found_symbol': [], 'errors': []}
        change_file_names()
        for filename in os.listdir():
            if 'NIFTY' in filename:
                with open(filename, 'rb') as f:
                    print("FILE NAME: {}".format(f))
                    r = requests.post(upload_url, headers=headers, verify=False, data=data, files={'FILES': f})
                    print(r)
                    if r.status_code == 200:
                        req_data = json.loads(r.text)['data']
                        req_data.pop('message')
                        for key, value in req_data.items():
                            dict_data[key].extend(value)
                    else:
                        print(f"error: {r.text}")
                        error_data = json.loads(r.text)
                        if error_data['errors']['message'] == "You don't have permission to post data":
                            return error_data['errors']['message']
                        dict_data['errors'].extend([{filename: error_data['errors']['message']}])

        print(dict_data)
        with open('data.json', 'w') as d:
            json.dump(dict_data, d)
        return "Data uploaded successfully"

    except Exception as e:
        # print("Exception is ", e, " line ", sys.exc_info()[-1].tb_lineno, "Type is: ", type(e).__name__)
        import traceback
        tb = traceback.format_exc()
        print(tb)


if __name__ == "__main__":

    login_url = "https://api.keev.tech:8001/api/user/v2/login/"
    # upload_url = "https://chakravyuh.in:8001/candlestick/upload/"
    # Enter email and password of admin for file upload
    username = 'info@keev.co.in'
    password = 'keev1234'
    result = requests.post(login_url, data={'email': username, 'password': password}, verify=False)
    if result.status_code != 200:
        print(f"Error while loging. Error text is {result.text}")

    token = json.loads(result.text)['data']['token']


    dir_path='D:/Drona/Market Data/Daily IEOD/NSE_FUT_1MIN_20210825'

    # for filename in os.listdir():
    #     new_directory = "{}\{}".format(dir_path, filename)
    #     # print(new_directory)
    #     os.chdir(new_directory)
    # for eachdate in os.listdir():
    #     if not '.zip' in eachdate:
    new_dir = """{}\Continuous Futures""".format(dir_path)
    os.chdir(new_dir)
    try:
        print(new_dir)
        message = upload_market_data(new_dir, token)
        # print(message)
        time.sleep(1)
        # os.chdir(dir_path)
        # break
    except Exception as e:
        print(e)
        pass


    # remove_extra(dir_path)
