#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import requests
import os

HOME = '/Users/feng.luan/Github/PythonProjects/learnNorwegian'
AUDIO_HOME = f'{HOME}/audio'
WORDS_HOME = f'{HOME}/words'


def get_speech(word_file):
    """Get each word speech by Google translator"""
    with requests.Session() as sess:
        #sess.headers['Authorization'] = f"Bearer {JWT}"
        sess.headers['Referer'] = "http://translate.google.com/"
        sess.headers['User-Agent'] = "stagefright/1.2 (Linux;Android 5.0)"
        api_uri = 'https://translate.google.com/translate_tts'
        params = {'ie': 'utf-8', 'tl': 'no', 'client': "tw-ob"}
        words = []
        s_id = len(AUDIO_HOME)
        page_id = word_file[s_id:-4]
        folder = f"{AUDIO_HOME}/{page_id}"
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(word_file, 'r') as f:
            words = [line.strip('\n') for line in f.readlines()]
        for w in words:
            speech_file = f"{folder}/{w}.mp3"
            if os.path.exists(speech_file):
                print(f"Skip.. {w}")
                continue
            params['q'] = w
            resp = sess.get(api_uri, params=params)
            resp.raise_for_status()
            if resp.status_code != 200:
                print(f"ERROR... {w}")
                continue
            with open(speech_file, 'wb') as out_file:
                out_file.write(resp.content)
                out_file.flush()
            print(f"OK... {w}")

def main():
    files = [f for f in os.listdir(WORDS_HOME) if f.endswith(".txt")]
    for f in files:
        get_speech(f'{HOME}/words/{f}')

if __name__ == '__main__':
    main()
