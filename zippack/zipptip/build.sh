# @Author: JinZhang
# @Date:   2019-05-07 11:00:52
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-07 17:34:20

client=`awk -F '=' '/\[path\]/{a=1}a==1&&$1~/client/{gsub(/^ +| +$/, "", $2);print $2;exit}' config.ini`
ptip_exe=`awk -F '=' '/\[path\]/{a=1}a==1&&$1~/ptip_exe/{gsub(/^ +| +$/, "", $2);print $2;exit}' config.ini`
py_zip=`awk -F '=' '/\[path\]/{a=1}a==1&&$1~/py_zip/{gsub(/^ +| +$/, "", $2);print $2;exit}' config.ini`
target_dir=`awk -F '=' '/\[path\]/{a=1}a==1&&$1~/target_dir/{gsub(/^ +| +$/, "", $2);print $2;exit}' config.ini`
target_name=`awk -F '=' '/\[path\]/{a=1}a==1&&$1~/target_name/{gsub(/^ +| +$/, "", $2);print $2;exit}' config.ini`

target_path=${target_dir}"/"${target_name}
target_pro_path=${target_path}"/PyToolsIP"
target_zip_name=${target_name}".zip"

# 创建目标文件夹
if [ ! -d $target_dir ]; then
	mkdir $target_dir
fi

# 创建目标文件夹
if [ ! -d "$target_path" ]; then
	mkdir $target_path
fi

# 创建目标工程文件夹
if [ ! -d "$target_pro_path" ]; then
	mkdir $target_pro_path
fi

# 拷贝client
cp -r ${client}"/." $target_pro_path

# 将pytoolsip.exe复制到target_pro_path
cp $ptip_exe $target_pro_path

# 将py_zip解压到$target_pro_path/
unzip $py_zip -d ${target_pro_path}"/include"

# 将$target_path打成PyToolsIP.zip包
cd $target_path
# 移除目标zip文件
target_zip="../"${target_zip_name}
if [ -f $target_zip ]; then
	rm $target_zip
fi
# 打成zip包
zip -r target_zip PyToolsIP/* -x \.*
# 删除中间文件
cd ../
rm -r $target_path