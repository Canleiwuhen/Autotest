#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version    : V1.0.0
# @Author     : 孙春旭
# @Datetime   : 2024/12/3 14:17
# @File       : app.py
# @Project    : apiforward
# @Description:
import csv
import io
import json
import os
import sys
import time
from urllib.parse import urlencode

import pytest
import requests
from flask import Flask, request, render_template, send_from_directory, Response, jsonify
import multiprocessing
from flask_sqlalchemy import SQLAlchemy

record_id = 0
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
db = SQLAlchemy(app)

csv_data = None

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_info = db.Column(db.String(999999))
    path = db.Column(db.String(50))
    last_step = db.Column(db.String(50))
    abnormal_input = db.Column(db.String(50))
    run_time = db.Column(db.String(50))
    user_name = db.Column(db.String(100))
    generate_data_volume = db.Column(db.String(50))
    indexConfig = db.Column(db.String(100))
    sequencePlatform = db.Column(db.String(100))
    sequenceType = db.Column(db.String(100))
    isChipCode = db.Column(db.String(100))
    chipCode = db.Column(db.String(100))
    result = db.Column(db.String(999999))
    env_dropdown = db.Column(db.String(50))

def run_in_process():
    pytest.main(["--cache-clear", "testcase/samplecenter/test_api.py"])
    # 重定向标准输出和标准错误
    # sys.stdout = io.StringIO()
    #
    # # 执行pytest
    # pytest.main(["--cache-clear", "testcase/samplecenter/test_api.py"])
    #
    # # 获取输出和错误日志
    # output = sys.stdout.getvalue()
    # # 恢复标准输出和标准错误
    # sys.stdout = sys.__stdout__
    # lines = output.splitlines()
    # error_lines = [line for line in lines if "| ERROR    |" in line]
    # output=error_lines
    # return output

def run_in_process_nifty():
    # sys.stdout = io.StringIO()
    import os
    test_path = os.path.abspath('testcase/nifty/test_api.py')
    pytest.main(["--cache-clear", test_path])
    # output = sys.stdout.getvalue()
    # sys.stdout = sys.__stdout__
    # # print(output)
    # lines = output.splitlines()
    # error_lines = [line for line in lines if "| ERROR    |" in line]
    # output = error_lines
    # return output

@app.route('/get_data', methods=['GET'])
def data():
    data_id = request.args.get('id')
    form_data = FormData.query.filter_by(id=data_id).first()
    data_list = [form_data.sample_info,form_data.path,form_data.last_step,form_data.abnormal_input,form_data.run_time,form_data.user_name,form_data.generate_data_volume,form_data.indexConfig,form_data.sequencePlatform,form_data.sequenceType,form_data.isChipCode,form_data.chipCode,form_data.result]
    data = {"message": data_list}
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def make_sense_data():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        dropdown = request.form.get('dropdown')
        textbox = request.form.get('textbox')
        input1 = request.form['input1']
        input2 = request.form['input2']
        user_dropdown = request.form['user_dropdown']
        with open('var_dir/sample/var.txt', 'w') as file:
            file.write('')
        with open('var_dir/sample/var.txt', 'w') as file:
            file.write(request.form['dropdown'] + '\n')
            file.write(str(int(request.form['input1']) - 1) + '\n')
            file.write(request.form['input2'] + '\n')
            file.write(request.form['user_dropdown'] + '\n')
            # global output
        try:
            process = multiprocessing.Process(target=run_in_process)
            process.start()
            process.join()
            # out_put = run_in_process()
            res_data_list = []
            for i in range(len(os.listdir('var_dir/sample'))):
                filename = f"var{i}.txt"
                with open('var_dir/sample/' + filename, 'r') as file:
                    for line in file:
                        data = line.strip()
                res_data_list.append(data)
            res_data = eval(data)[0]
            # data = data[0]
            translate_data = [{'sample': '样本编号', 'expressnum': '快递单号', 'container_prefix': '容器编号前缀',
                               'specifications': '容器规格', 'outbound_apply_order_number': '出库单号',
                               'inbound_apply_order_number': '入库单号', 'unpack_result': '拆包结果',
                               'arrvSerie': '到达序列号', 'container_num': '容器编号', 'container_id': '容器ID'}]
            translate_data = translate_data[0]
            translate_values = [value for value in translate_data.values()]
            keys = [key for key in res_data.keys()]
            values = [value for value in res_data.values()]
            values_list = []
            for i in range(len(res_data_list)):
                value = [value for value in eval(res_data_list[i])[0].values()]
                values_list.append(value)
            result_list = []
            for i in range(len(values_list)):
                result = [{'translate': translate, 'name': name, 'value': value} for translate, name, value in
                          zip(translate_values, keys, values_list[i])]
                result_list.append(result)
            return render_template('home.html', table_data=result_list, dropdown=dropdown, textbox=textbox,
                                   input1=input1, input2=input2, user_dropdown=user_dropdown)
        except Exception as e:
            response_data = str(e)
            # global output, error
            return render_template('home.html', value=response_data)


@app.route('/simpleExcelTable/<path:path>')
def send_js(path):
    return send_from_directory('static/simpleExcelTable', path)


@app.route('/loading_mask/<path:path>')
def send_loading_js(path):
    return send_from_directory('static/loading_mask', path)

def insert_db(mydata,dropdown,input1,exce_dropdown,input2,user_dropdown,data_dropdown,index_dropdown,platform_dropdown,type_dropdown,chip_dropdown,chip_input,env_dropdown):
    new_data = FormData(sample_info=mydata, path=dropdown, last_step=input1, abnormal_input=exce_dropdown,
                        run_time=input2, user_name=user_dropdown, generate_data_volume=data_dropdown,
                        indexConfig=index_dropdown, sequencePlatform=platform_dropdown, sequenceType=type_dropdown,
                        isChipCode=chip_dropdown, chipCode=chip_input, result="", env_dropdown=env_dropdown)
    db.session.add(new_data)
    db.session.flush()
    global record_id
    record_id = new_data.id
    db.session.commit()
    os.environ['LAST_RECORD_ID'] = str(record_id)

@app.route('/update_data', methods=['POST'])
def update_db():
    result_data = request.get_json()
    result_data = result_data.get("data")
    record_id = os.environ.get('LAST_RECORD_ID')
    update_data = db.session.query(FormData).filter_by(id=record_id).first()
    update_data.result = str(result_data)
    db.session.commit()
    data = {"message": result_data}
    return jsonify(data)
@app.route('/nifty', methods=['POST', 'GET'])
def make_nifty_data():
    if request.method == 'GET':
        global csv_data
        csv_data = None
        return render_template('nifty.html')
    if request.method == 'POST':
        # 样本信息
        mydata = request.form.get('myData')
        # 执行场景
        dropdown = request.form.get('dropdown')
        # 场景对应的技术路线
        textbox = request.form.get('textbox')
        # 执行到哪步
        input1 = request.form['input1']
        # 是否登记异常
        exce_dropdown = request.form['exce_dropdown']
        # 执行次数
        input2 = "1"
        # 执行账号
        user_dropdown = request.form['user_dropdown']
        # 生成数据量
        data_dropdown = request.form['data_dropdown']
        # Index配置
        index_dropdown = request.form['index_dropdown']
        # 测序平台
        platform_dropdown = request.form['platform_dropdown']
        # 测序类型
        type_dropdown = request.form['type_dropdown']
        # 是否自定义芯片号
        chip_dropdown = request.form['chip_dropdown']
        # 预设Pooling总量
        # pooling_dropdown = request.form['pooling_dropdown']
        # 芯片号
        chip_input = request.form['chip_input']
        env_dropdown = request.form['env_dropdown']
        insert_db(mydata,dropdown,input1,exce_dropdown,input2,user_dropdown,data_dropdown,index_dropdown,platform_dropdown,type_dropdown,chip_dropdown,chip_input,env_dropdown)
        # with open('var_dir/nifty/var.txt', 'w') as file:
        #     file.write('')
        # with open('var_dir/nifty/var.txt', 'w', encoding='utf-8') as file:
        #     file.write(request.form['myData'] + '\n')
        #     file.write(request.form['dropdown'] + '\n')
        #     file.write(str(int(request.form['input1'])) + '\n')
        #     file.write(request.form['exce_dropdown'] + '\n')
        #     file.write(input2 + '\n')
        #     file.write(request.form['user_dropdown'] + '\n')
        #     file.write(request.form['data_dropdown'] + '\n')
        #     file.write(request.form['index_dropdown'] + '\n')
        #     file.write(request.form['platform_dropdown'] + '\n')
        #     file.write(request.form['type_dropdown'] + '\n')
        #     file.write(request.form['chip_dropdown'] + '\n')
        #     file.write(request.form['chip_input'] + '\n')
        try:
            process = multiprocessing.Process(target=run_in_process_nifty)
            process.start()
            process.join()
            # out_put = run_in_process_nifty()
            count = 0
            while True:
                count += 1
                time.sleep(1)
                data_id = os.environ.get('LAST_RECORD_ID')
                data = {
                    "id": data_id
                }
                url = "http://127.0.0.1:8087/get_data"
                response = requests.get(url, params=urlencode(data))
                var_list = response.json()["message"][12]
                if var_list:
                    break
                if count >= 3:
                    break
            res_data_list = eval(var_list)
            # res_data_list = []
            # for i in range(len(os.listdir('var_dir/nifty')) - 2):
            #     filename = f"nifty_var{i}.txt"
            #     with open('var_dir/nifty/' + filename, 'r', encoding='utf-8') as file:
            #         for line in file:
            #             data = line.strip()
            #     res_data_list.append(data)
            res_data = eval(res_data_list[0])[0]
            excel_data = eval(mydata)
            sample_data = res_data["sample"]
            for i in range(len(excel_data)):
                excel_dict = excel_data[i]
                excel_dict["sample"] = sample_data[i]
            for d in excel_data:
                d.pop('num')
            csv_data = excel_data
            translate_data = [{'result_data': '分析结果', 'chip_num': '芯片号','sequencing_task_code': '梧桐分析平台任务单号',
                               'jkfdealorder_plate_code': '建库孔板号',
                               'bmg_task_code': 'BMG任务号', 'jkfdealorder_task_code': '建库任务号',
                               'makednb_task_code': 'makeDNB任务号', 'zjob_code': '执行步骤的任务号',
                               'zjcwbh': '质检产物编号', 'sample': '样本编号', 'pooling_scheme': 'Pooling后文库号',
                               'dlhhorder_scheme': '单链后文库号'}]
            translate_data = translate_data[0]
            translate_values = [value for value in translate_data.values()]
            keys = [key for key in res_data.keys()]
            values = [value for value in res_data.values()]
            values_list = []
            for i in range(len(res_data_list)):
                value = [value for value in eval(res_data_list[i])[0].values()]
                values_list.append(value)
            result_list = []
            for i in range(len(values_list)):
                result = [{'translate': translate, 'name': name, 'value': value} for translate, name, value in
                          zip(translate_values, keys, values_list[i])]
                result_list.append(result)
            return render_template('nifty.html', table_data=result_list, dropdown=dropdown,
                                   textbox=textbox, input1=input1, user_dropdown=user_dropdown, myData=mydata,
                                   exce_dropdown=exce_dropdown, data_dropdown=data_dropdown,
                                   platform_dropdown=platform_dropdown,
                                   type_dropdown=type_dropdown, chip_dropdown=chip_dropdown, chip_input=chip_input,
                                   index_dropdown=index_dropdown, excel_data=excel_data, env_dropdown=env_dropdown)
        except Exception as e:
            response_data = str(e)
            return render_template('nifty.html', value=response_data)

@app.route('/export_csv')
def download_csv():
    if csv_data is None:
        return "没有可以导出的数据！"
    else:
        data = csv_data
        new_data = [[d['sampleType'], d['Lane'], d['index'], d['productNum'], d['tireType'], d['qualityControl'],d['special_sample_id'], d['CNV_info'], d['CNV_section_info'], d['test13'], d['test18'], d['test21'], d['test_sex'], d['test_auto'], d['note3'], d['note2'], d['disease'], d['qc'],d['chr'],d['chrTest'],d['filterFlag'],d['fra'],d['risk'],d['t'],d['zScore'], d['report_tag'], d['ZTUBETYPE'], d['sample']] for d in data]
        title = ['样本类型', 'Lane', 'index','产品编号','胎型','是否需要质控品','指定样本编号','CNV区带信息','CNV区间信息','test13','test18','test21','test_sex(性染色体)','test_auto（常染色体）','note3（梧桐）','note2','disease疾病名称','qc','chr（染色体编号）','chrTest（Test值）','filterFlag（是否过滤：0否 1是）','fra（胎儿浓度）','risk（Risk值）','t（T值）','zScore（Z值）','report_tag报告标签','样品管类型','样本编号']
        # 初始化StringIO对象
        exp_data = io.StringIO()
        csv_writer = csv.writer(exp_data)
        # 写入CSV数据
        csv_writer.writerow(title)
        for i in range(len(new_data)):
            csv_writer.writerow(new_data[i])
        # 把StringIO对象的位置重置为文件开始
        exp_data.seek(0)
        # 设置响应的MIME类型为'text/csv'并设置Content-Disposition头
        response = Response(exp_data, mimetype="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        response.data = b'\xef\xbb\xbf' + response.data
        return response

@app.route("/download_template")
def download_template():
    return send_from_directory("excel_temp", "template.xlsx", as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8087)
