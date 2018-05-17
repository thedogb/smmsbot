#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-16 下午8:29
# @Author  : thedoga
# @Site    : 
# @File    : tools.py
# @Software: PyCharm

import logging
import json
import requests
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import cloudstorage as gcs
from google.appengine.api import app_identity
from google.appengine.api import images
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
bucket = '/' + bucket_name
API_URL = 'https://sm.ms/api/'



def download(bot, file_id):
    # 测试文件写入
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    filename = '%s/%s'%(bucket,file_id)
    gcs_file = gcs.open(filename, 'w',
                        content_type='application/octet-stream',
                        retry_params=write_retry_params)
    F = bot.getFile(file_id)
    url = F._get_encoded_url()
    buf = bot.request.retrieve(url)
    gcs_file.write(str(buf))
    gcs_file.close()


def upload(file_id):
    filename = '%s/%s'%(bucket,file_id)
    gcs_file = gcs.open(filename, 'r')
    img = bytes(gcs_file.read())
    f = {
        'smfile': img
    }
    r = requests.post(API_URL + 'upload', files=f)
    gcs_file.close()
    link = r.json()
    return link

def error_handler(bot, update, error):
    logger.exception(error)



def upload_handler(bot, update):
    try:
        file_id = update.message.document.file_id
        if not update.message.document.mime_type.startswith('image/'):
            return update.message.reply_text('File has an invalid extension.', quote=True)
    except:
        file_id = update.message.photo[-1].file_id
    download(bot, file_id)
    uploader = upload(file_id)
    filename = '%s/%s'%(bucket,file_id)
    gcs.delete(filename)
    if uploader['code'] == 'error':
        update.message.reply_text(uploader['msg'], quote=True)
    else:
        kb = [[InlineKeyboardButton('Click Here To Delete', callback_data=uploader['data']['hash'])]]
        update.message.reply_text('`%s`' % uploader['data']['url'], quote=True, parse_mode='markdown',
                                  disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(kb))
def download_sticker(bot, file_id):
    # 测试文件写入
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    filename = '%s/%s'%(bucket,file_id)
    gcs_file = gcs.open(filename, 'w',
                        content_type='application/octet-stream',
                        retry_params=write_retry_params)
    F = bot.getFile(file_id)
    url = F._get_encoded_url()
    buf = bot.request.retrieve(url) # 从tg下载sticker保存为webp格式
    img = images.Image(image_data=buf)
    img.im_feeling_lucky()
    pngImg = img.execute_transforms(output_encoding=images.PNG)
    gcs_file.write(pngImg)
    gcs_file.close()

def upload_sticker_handler(bot, update):
    file_id = update.message.sticker.file_id
    download_sticker(bot, file_id)
    uploader = upload(file_id)
    filename = '%s/%s'%(bucket,file_id)
    gcs.delete(filename)
    if uploader['code'] == 'error':
        update.message.reply_text(uploader['msg'], quote=True)
    else:
        kb = [[InlineKeyboardButton('Click Here To Delete', callback_data=uploader['data']['hash'])]]
        update.message.reply_text('`%s`' % uploader['data']['url'], quote=True, parse_mode='markdown',
                                  disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(kb))



def callback_handler(bot, update):
    key = update.callback_query.data
    requests.get(API_URL + 'delete/%s' % key)
    update.callback_query.message.edit_text('Photo Deleted!')
