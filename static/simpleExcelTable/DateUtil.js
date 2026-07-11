/******************************************************************************
 *********************************通用时间工具***********************************
 ******************************************************************************
 ******************************************************************************/
function DateUtil(){};

Date.prototype.format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};
/**
 * 对日期进行格式化
 * 使用说明：返回对应格式的时间字符串，如getTimeByFormat("yyyy-MM-dd hh:mm:ss")
 */
DateUtil.formartDate = function(date,format){
    if(typeof date === 'string'){
        return date;
    }
    return date.format(format);
};
DateUtil.formartNow = function(format){
    var date = new Date();
    return date.format(format);
};
/**
 * 将日期对象强转为日期类型
 * @param date  日期或者日期格式字符串
 * @returns {null|Date}
 */
DateUtil.parseDate = function(date){
    if(date instanceof Date){
        return date;
    }
    if(DateUtil.isDateStr(date)){
        return new Date(date);
    }
    return null;
};


/**
 * 功能：比较两个日期字符串的大小
 * 使用说明：返回true或false
 */
DateUtil.compareDate = function(t1,t2){
    if(!StringUtil.hasEmpty(t1,t2)){
        var d1;
        var d2;
        if(t1 instanceof Date){
            d1 = t1;
        }else{
            d1 = new Date(t1);
        }
        if(t2 instanceof Date){
            d2 = t2;
        }else{
            d2 = new Date(t2);
        }
        return d1 <= d2;
    }
    return false;
};


/**
 * 验证日期字符串格式是否合法
 */
DateUtil.isDateStr = function(str){
    return new Date(str).toString() !== "Invalid Date";
};
/**
 * 对日期进行天数的加减操作
 * @param date1
 * @param n     负数代表减去n天
 */
DateUtil.addDay = function(date1,n){
    var d = DateUtil.parseDate(date1);
    var dms = 1000*60*60*24 * n;
    d = new Date(d.getTime() + dms);
    return d;
};

/**
 * 计算两个日期之间相差的天数
 */
DateUtil.getBetweenDay = function(date1,date2){
    var d1 = DateUtil.parseDate(date1);
    var d2 = DateUtil.parseDate(date2);
    /*var time1 = Date.parse(date1.length==6 ? date1+"/01" : (date1.length==4 ? date1+"/01/01" : date1));
    var time2 = Date.parse(date2.length==6 ? date2+"/01" : (date2.length==4 ? date2+"/01/01" : date2));*/
    var time1 = d1.getTime();
    var time2 = d2.getTime();
    return parseInt((time2 - time1) / 1000 / 3600 / 24);
};
/**
 * 计算两个日期之间相差的周数
 */
DateUtil.getBetweenWeek = function(date1,date2){
    var n=DateUtil.getBetweenDay(DateUtil.getFirstDayOfWeek(date1),DateUtil.getFirstDayOfWeek(date2));
    return parseInt(n/7);
};
/**
 * 计算两个日期之间相差的月数
 */
DateUtil.getBetweenMonth = function(date1,date2){
    var d1 = DateUtil.parseDate(date1);
    var d2 = DateUtil.parseDate(date2);
    date1 = parseInt(DateUtil.formartDate(d1,'yyyyMMdd'));
    date2 = parseInt(DateUtil.formartDate(d2,'yyyyMMdd'));
    var year1 = parseInt(date1/10000);
    var year2 = parseInt(date2/10000);
    var month1 = parseInt((date1-year1*10000)/100);
    var month2 = parseInt((date2-year2*10000)/100);
    if(month2 < month1){
        year2--;
        month2+=12;
    }
    return (year2-year1)*12 + month2 - month1;
};
/**
 * 计算date1所在周的第一天
 */
DateUtil.getFirstDayOfWeek = function(date1){
    var d1=DateUtil.parseDate(date1);
    var dec;
    var weekday1 = d1.getDay()||7;
    dec=1-weekday1;
    d1.setDate(d1.getDate()+dec);
    return DateUtil.formartDate(d1,'yyyy-MM-dd');
};
/**
 * 计算date1所在周的最后一天
 */
DateUtil.getLastDayOfWeek = function(date1){
    var d1=DateUtil.getFirstDayOfWeek(date1);
    var d2 = DateUtil.addDay(d1,6);
    return DateUtil.formartDate(d2,'yyyy-MM-dd');
};
/**
 * 计算date1所在月份的第一天
 */
DateUtil.getFirstDayOfMonth = function(date1){
    var date = DateUtil.parseDate(date1);
    var d=new Date(date.getFullYear(),date.getMonth(),1);
    return DateUtil.formartDate(d,'yyyy-MM-dd');
};
/**
 * 计算date1所在月份的最后一天
 */
DateUtil.getLastDayOfMonth = function(date1){
    var date = DateUtil.parseDate(date1);
    var currentMonth=date.getMonth();
    var nextMonth=++currentMonth;
    var nextMonthFirstDay=new Date(date.getFullYear(),nextMonth,1);
    //var oneDay=1000*60*60*24;
    //var lastTime = new Date(nextMonthFirstDay-oneDay);
    var lastTime = DateUtil.addDay(nextMonthFirstDay,-1);
    return DateUtil.formartDate(lastTime,'yyyy-MM-dd');
};






