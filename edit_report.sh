#!/bin/bash

system_name=$1    # 系统名称
jenkins_home=$2   # Jenkins数据目录
job_name=$3       # 构建任务的名称
build_number=$4   # 当前构建编号

# 拼接本次构建路径和初始化待修改文件路径
build_archive_path="${jenkins_home}/jobs/${job_name}/builds/${build_number}/archive"
zip_name="allure-report.zip"
report_name="allure-report"
index_path="./allure-report/index.html"
summary_path="./allure-report/widgets/summary.json"
logo_css_path="./allure-report/plugins/custom-logo/styles.css"
graphs_severity_path="./allure-report/app.js"
severity_json_path="./allure-report/widgets/severity.json"
test_cases_path="${build_archive_path}/allure-report/data/test-cases/*"
environment_json_path="./allure-report/widgets/environment.json"

# 进入本次构建归档目录
cd $build_archive_path

# 通过系统名称获取测试环境地址，覆盖environment.json文件【注意：有新系统接入时，一定要先在下面增加系统名称的判断，否则会直接报错退出】
if [ $system_name = "样本中心" ]; then
    system_url="https://sample-test.bgi.com/ybzx/"
elif [ $system_name = "NIFTY" ]; then
    system_url="https://nifty-test.bgi.com/presapMS/#/sign/"
elif [ $system_name = "omicsone" ]; then
    system_url="https://omicsone-test.bgi.com/login"
else
    echo "当前系统名称在edit_report.sh脚本中不存在，请添加对应系统和url！"
    system_url="https://XXXXX"
fi

# 解压报告zip包
unzip -q $zip_name

# 编辑网页title
sed -i "s/Allure Report/${system_name}项目接口自动化测试报告/g" $index_path

# 编辑总览页左上角标题
sed -i "s/Allure Report/${system_name}项目接口自动化测试报告/g" $summary_path

# 编辑logo的css文件，隐藏文本内容
cat >> $logo_css_path <<EOF
.side-nav__brand-text {
    visibility: hidden;
}
EOF

# 编辑app.js图表菜单的优先级
sed -i 's/\["blocker","critical","normal","minor","trivial"\]/\["p0(高)","p1(中)","p2(低)"\]/g' $graphs_severity_path

# 编辑severity_json里test_case的优先级
sed -i "s/blocker/p0(高)/g; s/critical/p1(中)/g; s/normal/p2(低)/g" $severity_json_path

# 遍历test_cases目录每个case的json，修改test_case的优先级
for file in $test_cases_path
do
    if [ -f "${file}" ]; then
        sed -i "s/blocker/p0(高)/g; s/critical/p1(中)/g; s/normal/p2(低)/g" $file
    fi
done

# 在报告页面中打印测试环境地址
echo "[{\"values\":[\"${system_url}\"],\"name\":\"${system_name}测试环境地址\"}]" > $environment_json_path

# 删除原压缩文件
rm $zip_name

# 把修改好的report目录打包压缩
zip -qr $zip_name $report_name

# 删除原解压后的report目录
rm -r $report_name