String.prototype.trim = function() {
    return this.replace(/^\s+/g,"").replace(/\s+$/g,"");
};
String.prototype.replaceAll  = function(s1,s2){
  return this.replace(new RegExp(s1,"gm"),s2);
};

function StringUtil(){};
StringUtil.uuid = function () {
    let str = '0123456789abcdef'
    let arr = []
    for(let i = 0; i < 32; i++){
        arr.push(str.substr(Math.floor(Math.random() * 0x10), 1))
    }
    return arr.join('');
};
StringUtil.isEmpty = function (a) {
    return StringUtil.isNull(a) || a === undefined || a.length === 0;
};
StringUtil.trimEmpty = function (a) {
    return StringUtil.isNull(a) || a.toString().trim().length === 0;
};
StringUtil.isNotEmpty = function (a) {
    return !StringUtil.isEmpty(a);
};
StringUtil.trimNotEmpty = function (a) {
    return !StringUtil.trimEmpty(a);
};
StringUtil.isNull = function (a) {
    return a === null || a=== undefined;
};
StringUtil.hasEmpty = function () {
    for(var i = 0;i<arguments.length;i++){
        if(StringUtil.isEmpty(arguments[i])){
            return true;
        }
    }
    return false;
};
StringUtil.allEmpty = function () {
    for(var i = 0;i<arguments.length;i++){
        if(StringUtil.isNotEmpty(arguments[i])){
            return false;
        }
    }
    return true;
};
StringUtil.hasNull = function () {
    for(var i = 0;i<arguments.length;i++){
        if(StringUtil.isNull(arguments[i])){
            return true;
        }
    }
    return false;
};
StringUtil.trim = function (str) {
    return str == null ? null : str.toString().trim();
};
StringUtil.safeToString = function (a,dv) {
    return !StringUtil.isEmpty(a) ? a.toString() : dv;
};
StringUtil.nvl = function (str) {
    var len = arguments.length;
    for(var i=0;i<len;i++){
        if(StringUtil.isNotEmpty(arguments[i])){
            return arguments[i];
        }
    }
    return null;
};
StringUtil.join = function (arr,sec) {
    if(sec === undefined){
        sec = ",";
    }
    var array = [];
    if(arr.constructor===Array){
        array = arr;
    }else if(arr.constructor===String){
        array.push(arr);
    }else if(arr.constructor===Object){
        for(var key in arr){
            array.push(arr[key]);
        }
    }
    return array.join(sec);
};
/**
 * a startwidth b
 */
StringUtil.startWidth = function (a,b) {
    return !StringUtil.hasNull(a,b) && a.indexOf(b) === 0;
};
StringUtil.endWidth = function (a,b) {
    return !StringUtil.hasNull(a,b) && a.indexOf(b) === a.length -b.length;
};