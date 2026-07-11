var excelTool ={
    setReadOnly: function(column,obj){
        var type = column['type'];
        var readonly = column['readonly'];
        if(readonly === true){
            if(type === 'input'){
                obj.attr('readonly','readonly');
            }else if(type==='select'){
                //obj.attr("onfocus","this.defaultIndex=this.selectedIndex;").attr("onchange","this.selectedIndex=this.defaultIndex;");
                obj.attr("disabled",'disabled');
            }else if(type==='checkbox' || type==='radio'){
                //obj.attr("onfocus","this.defaultIndex=this.selectedIndex;").attr("onchange","this.selectedIndex=this.defaultIndex;");
                obj.attr("disabled",'disabled');
            }
            obj.css('cursor','not-allowed');
        }
    },
    setCss: function(column,obj){
        var css = column['css'];
        if(StringUtil.isNotEmpty(css)){
            for (let cssKey in css) {
                obj.css(cssKey,css[cssKey]);
            }
        }
    },
    setCellStyle: function(column,obj){
        var cellStyle = column['cellStyle'];
        if(StringUtil.isNotEmpty(cellStyle)){
            var align = cellStyle['align'];
            if(StringUtil.isNotEmpty(align)){
                obj.css('text-align',align);
            }
        }
    },
    buildSelect: function(column,obj){
        var list = column['list'];
        var defaultValue = column['defaultValue'];
        if(StringUtil.isNotEmpty(list)){
            defaultValue = StringUtil.safeToString(defaultValue,'');
            for (let x1 in list) {
                var opt = new Tag('option').append(StringUtil.safeToString(list[x1].v,''));
                var k ;
                opt.val(k = StringUtil.safeToString(list[x1].k,''));
                if(k == defaultValue){
                    opt.attr('selected','selected');
                }
                obj.append(opt);
            }
        }
    },
    inputObj: function(column){
        var obj = new Tag('input',true);
        var emptyText = column['emptyText'];
        var fieldName = column['fieldName'];
        //obj.attr('id',fieldName+"_"+r+"_"+l).name(fieldName);
        obj.attr('type','text').clazz('dreahover');
        if(StringUtil.isNotEmpty(emptyText)){
            obj.attr('placeholder',emptyText);
        }
        this.setReadOnly(column,obj);
        this.setCss(column,obj);
        this.setCellStyle(column,obj);
        return obj;
    },
    selectObj: function(column){
        var obj = new Tag('select').clazz('dreahover');
        var fieldName = column['fieldName'];
        //obj.attr('id',fieldName+"_"+r+"_"+l).name(fieldName);
        excelTool.buildSelect(column,obj);
        this.setReadOnly(column,obj);
        this.setCss(column,obj);
        this.setCellStyle(column,obj);
        return obj;
    },
    checkboxObj: function(column,type){
        var obj = new Tag('div').clazz('excel-table-checkbox-div');
        var fieldName = column['fieldName'];
        var defaultValue = column['defaultValue'];
        var key = StringUtil.uuid();

        var choices = column['choices'];
        if(StringUtil.isNotEmpty(choices)){
            //obj.attr('id',fieldName+"_"+key+"_div").name(fieldName+"_div");
            for (let choicesKey in choices) {
                var ck = new Tag('input',true).clazz('dreahover').attr('id',fieldName+"_"+key+"_"+choicesKey).name(fieldName+"_"+key).attr('type',type).val(choicesKey);
                if(type === 'radio'){
                    if(defaultValue == choicesKey){
                        ck.attr('checked','checked');
                    }
                }else{
                    if(defaultValue== choicesKey || defaultValue.indexOf(","+choicesKey+",") > -1
                        || new RegExp(","+choicesKey+"$","gm").test(defaultValue) || new RegExp("^"+choicesKey+",","gm").test(defaultValue)){
                        ck.attr('checked','checked');
                    }
                }

                var label = new Tag('label').append(StringUtil.safeToString(choices[choicesKey],'')).attr('for',fieldName+"_"+key+"_"+choicesKey);
                ck.after(label);
                excelTool.setReadOnly(column,ck);
                obj.append(ck);
            }

        }

        return obj;
    },
    cloneRow: function(table,target){
        var tr = $(target).parents('tr').eq(0).clone();
        var tim = StringUtil.uuid();
        tr.children().find('.dreahover').each(function(i,o){
            if($(o).is('input[type=checkbox]') || $(o).is('input[type=radio]')){
                $(o).attr('id',$(o).attr('id')+'_'+tim);
                $(o).attr('name',$(o).attr('name')+'_'+tim);
                $(o).prop('checked',false);
                var label = $(o).next();
                if(label.is('label')){
                    label.attr('for',$(o).attr('id'));
                }
            }else{
                $(o).attr('id',$(o).attr('id')+'_'+tim);
                $(o).val('');
            }
        })
        //console.log(tr);
        this.addEvent(tr);
        $(target).parents('tr').eq(0).after(tr);
    },
    addEvent: function (tr) {
        $(tr).children().find(".dreahover").each(function(i,o){
            $(o).bind("focus",function(){
                $(o).parents('td').eq(0).addClass("td-hover");
            }).bind("blur",function(){
                $(o).parents('td').eq(0).removeClass("td-hover");
            });
        })


    },
    newRow: function(columns){
        var trr = new Tag('tr');
        for (let x in columns) {
            var column = columns[x];
            var width = column['width'];
            var type = column['type'];
            var td = new Tag('td');
            var obj;
            if(type === 'input'){
                obj = excelTool.inputObj(column);
            }else if(type==='select'){
                obj = excelTool.selectObj(column);
            }else if(type==='checkbox'){
                obj = excelTool.checkboxObj(column,'checkbox');
            }else if(type==='radio'){
                obj = excelTool.checkboxObj(column,'radio');
            }
            if(StringUtil.isNotEmpty(width)){
                td.attr('width',width);
            }
            td.append(obj);
            trr.append(td);
        }
        var obj = $(trr.toString());
        excelTool.addEvent(obj);
        return obj;
    }
};
$.fn.extend({
    initExcelTable: function (set) {
        var table = new Tag('table').clazz('excel-table full');
        table.attr('id','excelTable');
        var columns = set.columns;
        this.columns = columns;
        this.showHeader = set.showHeader;
        var row = set.row;
        var that = this;
        var addHeaderFunc = function(){
            var tableElem = $(that).children('.excel-table');
            if(tableElem.length == 0){
                var header = new Tag('tr');
                for (let x in columns) {
                    var column = columns[x];
                    var headerColumn = column['header'];
                    var fieldName = column['fieldName'];
                    var td = new Tag('td');
                    var headerText = StringUtil.safeToString(headerColumn['text'],'column'+x);
                    var width = column['width'];
                    var obj = new Tag('input',true).attr('type','text').clazz('dreahover').val(headerText).css('text-align','center');
                    obj.attr('id','header_'+fieldName).name('header_'+fieldName);
                    obj.attr('title',headerText);
                    excelTool.setCss(headerColumn,obj);
                    td.append(obj);
                    if(StringUtil.isNotEmpty(width)){
                        td.attr('width',width);
                    }
                    header.append(td);
                }
                table.pretend(header);
            }else{
                $(that).children('.excel-table').children().find('tr').eq(0).show();
            }
        }
        var removeHeaderFunc = function () {
            $(that).children('.excel-table').children().find('tr').eq(0).hide();
        }
        if(this.showHeader !== false){
            addHeaderFunc();
        }
        for(var i =0;i<row;i++){
            var trr = excelTool.newRow(columns,i);
            table.append(trr);
        }
        $(this).addClass('excel-table-div').empty().append(table.toString());
        /*$(that).children('.excel-table').find('tr').each(function(i,o){
            excelTool.addEvent(o);
        });*/
        excelTool.addEvent($(that).children('.excel-table').find('tr').eq(0));
        this.hideHeader = function(b){
            if(b !== false){
                if(this.showHeader){
                    removeHeaderFunc();
                }
                this.showHeader = false;
            }else{
                if(!this.showHeader){
                    addHeaderFunc();
                }
                this.showHeader = true;
            }
        }
        this.getRowData = function(n,tds){
            if(n == 0){
                return {};
            }
            if(tds == null){
                tds = $(that).children('.excel-table').find('tr').eq(parseInt(n)).children('td');
            }
            var data = {};
            for (let x in columns) {
                var column = columns[x];
                var fieldName = column['fieldName'];
                var items = tds.eq(x).find('.dreahover');
                var v = '';
                if($(items).is('input[type=radio]') || $(items).is('input[type=checkbox]')){
                    for (let itemsKey in items) {
                        if(items.eq(itemsKey).prop('checked')){
                            v += v.length > 0 ? ',' : '';
                            v += items.eq(itemsKey).val();
                        }
                    }
                }else{
                    v = $(items).val();
                }
                data[fieldName] = StringUtil.safeToString(v,"");
            }
            return data;
        }
        this.getData = function(){
            var res = [];
            var trs = $(that).children('.excel-table').find('tr');
            for(var i=1;i<trs.length;i++){
                if(i == 0){
                    continue;
                }
                var tds = $(trs).eq(i).children('td');
                res.push(this.getRowData(i,tds));
            }
            return res;
        }
        this.setRowData = function(r,row,sec){
            if(sec == null || sec < 0){sec = -1;}
            var tds = $(that).children('.excel-table').find('tr').eq(parseInt(r)+1+sec).find('td');
            if(tds.length > 0){
                for (let x in columns) {
                    var column = columns[x];
                    var fieldName = column['fieldName'];
                    var cType = column['type'];
                    var items = tds.eq(x).find('.dreahover');
                    var v = StringUtil.safeToString(row[fieldName],'');
                    if($(items).is('input[type=radio]') || $(items).is('input[type=checkbox]')){
                        $(items).prop('checked',false);
                        var arr = [];
                        if(StringUtil.isNotEmpty(v)){
                            arr = v.split(',');
                        }else{
                            arr.push('');
                        }
                        for (let itemsKey in items) {
                            var con = false;
                            for (let arrElement in arr) {
                                if(items.eq(itemsKey).val() == arr[arrElement]){
                                    con = true;
                                    break;
                                }
                            }
                            if(con){
                                items.eq(itemsKey).prop('checked',true);
                                if(cType === 'radio'){
                                    break;
                                }
                            }
                        }
                    }else{
                        $(items).val(row[fieldName]);
                    }
                }
            }
        }
        this.getDataRowNum = function(){
            return $(that).children('.excel-table').find('tr').length - 1;
        }
        this.setData = function(list){
            if(StringUtil.isNotEmpty(list)){
                var trs = $(that).children('.excel-table').find('tr');
                var sec = list.length - (trs.length - 1);
                if(sec > 0){
                    this.insertRow(trs.length - 1,sec);
                    trs = $(that).children('.excel-table').find('tr');
                }
                for (let i in list) {
                    var row = list[i];
                    var tds = trs.eq(parseInt(i)).find('td');
                    if(tds.length > 0){
                        this.setRowData(i,list[i],0)
                    }
                }
            }
        }
        this.insertRow = function(r,n){
            if(n == null || n <= 0){n = 1;}
            var stand = $(that).children('.excel-table').find('tr').eq(parseInt(r)-1+1);
            if(stand.length > 0){
                for (let c = 0;c < n ;c++) {
                    var tr = excelTool.newRow(columns);
                    stand.after(tr);
                }
            }
        }
        this.deleteRow = function(r,n){
            if(n == null || n <= 0){n = 1;}
            if(r == null || r <= 0){r = 1;}
            var stand = $(that).children('.excel-table').find('tr').eq(parseInt(r));
            if(stand.length > 0){
                for (let c = 0;c < n ;c++) {
                    var ntr = stand.after();
                    if(ntr.length == 0){
                        break;
                    }else{
                        ntr.remove();
                        stand = $(that).children('.excel-table').find('tr').eq(parseInt(r));
                    }
                }
            }
        }
        return this;
    }
});
