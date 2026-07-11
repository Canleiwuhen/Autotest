#!/bin/bash -il

if workon|grep -q 'nifty';then
        echo "已存在nifty虚拟环境"
        workon nifty
else
        mkvirtualenv nifty
        echo "创建nifty虚拟环境"
        workon nifty
fi

pip install -r requirements.txt
