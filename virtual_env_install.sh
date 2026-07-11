#!/bin/bash -il

if workon|grep -q 'api-forward';then
        echo "已存在api-forward虚拟环境"
        workon api-forward
else
        mkvirtualenv api-forward
        echo "创建api-forward虚拟环境"
        workon api-forward
fi

pip install -r requirements.txt
