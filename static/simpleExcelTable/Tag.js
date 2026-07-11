
var Tag=function(tagN,inDolt,single){
    var defaultDolt="\"";
    this.dolt=defaultDolt;
    if(inDolt==="\"" || inDolt==="'"){
        this.dolt=inDolt;
    }
    this.tagName=tagN;
    this.attributes={};
    this.id='';
    this.preBodyContent=[];
    this.bodyContent=[];
    this.aftBodyContent=[];
    this.cssContent={};
    var isNull=function(a){
        return a==undefined || a== null || a.length==0;
    };
    if(tagN === 'input'){
        single = true;
    }
    this.isTagType="tag_severlized_123asd";
    this.attr=function(key,value){
        this.saveCheck();
        if(!isNull(key)){
            if(key==="id" || key==="ID" || key==="iD" || key==="Id"){
                if(isNull(value)){
                    this.id=null;
                }else{
                    this.id=value;
                }

            }else if(key==="style"){
                if(!isNull(value)){
                    var cssTemp=value.split(";");
                    for(var i=0;i<cssTemp.length;i++){
                        var ct=cssTemp[i];
                        if(!isNull(ct) && ct.indexOf(":")>-1){
                            var cssKey=ct.split(":")[0];
                            var cssVal=ct.split(":")[1];
                            this.css(cssKey,cssVal);
                        }
                    }
                }
            }else{
                this.attributes[key]=value;
            }
        }
        return this;
    };
    this.css=function(key,value){
        this.saveCheck();
        if(!isNull(key)){
            if(isNull(value)){
                delete this.cssContent[key];
            }else{
                this.cssContent[key]=value;
            }
        }
        return this;
    };
    this.append=function(obj){
        if(!isNull(obj)){
            this.saveCheck();
            if(typeof obj==="string"){
                this.bodyContent.push(obj);
            }else if(obj.isTagType===this.isTagType){
                this.bodyContent.push(obj.toHtml());
            }
        }
        return this;
    };
    this.pretend=function(obj){
        if(!isNull(obj)){
            this.saveCheck();
            if(typeof obj==="string"){
                this.bodyContent.unshift(obj);
            }else{
                this.bodyContent.unshift(obj.toString());
            }
        }
        return this;
    };
    this.before=function(obj){
        if(!isNull(obj)){
            this.saveCheck();
            if(typeof obj==="string"){
                this.preBodyContent.push(obj);
            }else{
                this.preBodyContent.push(obj.toString());
            }
        }
        return this;
    };
    this.after=function(obj){
        if(!isNull(obj)){
            this.saveCheck();
            if(typeof obj==="string"){
                this.aftBodyContent.unshift(obj);
            }else{
                this.aftBodyContent.unshift(obj.toString());
            }
        }
        return this;
    };
    this.name=function(name){
        return this.attr('name',name);
    };
    this.clazz=function(clazz){
        return this.attr('class',clazz);
    };
    this.is=function(tagName){
        return this.tagName===tagName;
    };
    this.setId=function(id){
        this.id=id;
    };
    this.cancleHref=function(){
        return this.attr("href","javascript:void(0);");
    };
    this.onClick=function(f){
        return this.attr("onclick",f);
    };
    this.val=function(v){
        return this.attr("value",v);
    };
    this.title=function(v){
        return this.attr("title",v);
    };
    this.class=function(v){
        var cla = StringUtil.safeToString(this.attributes[v],'');
        if(cla.length > 0){
            cla += ' ';
        }
        cla += v;
        return this.attr("class",cla);
    };

    this.toHtml=function(){
        if(isNull(this.tagName)){
            return '';
        }
        this.saveCheck();
        var res="";
        for(var i=0;i<this.preBodyContent.length;i++){
            res+=this.preBodyContent[i];
        }
        res+="<"+this.tagName;
        if(!isNull(this.id)){
            res+=" id="+this.dolt+this.id+this.dolt;
        }
        for(var k in this.attributes){
            res+=" "+k+"="+this.dolt+this.attributes[k]+this.dolt;;
        }
        var cssCount=0;
        for(var sty in this.cssContent){
            if(!isNull(this.cssContent[sty])){
                if(cssCount==0){
                    res+=" style="+this.dolt;
                }
                res+=sty+":"+this.cssContent[sty]+";";
                cssCount++;
            }
        }
        if(cssCount>0){
            res+=this.dolt;
        }
        if(single === true){
            res+="/";
        }
        res+=">";
        for(var i=0;i<this.bodyContent.length;i++){
            res+=this.bodyContent[i].toString();
        }
        if(single !== true){
            res+="</"+this.tagName+">";
        }
        for(var i=0;i<this.aftBodyContent.length;i++){
            res+=this.aftBodyContent[i].toString();
        }
        return res;
    };
    this.toString=function(){
        return this.toHtml();
    };
    this.saveCheck=function(){
        if(this.attributes==undefined || this.attributes==null){
            this.attributes={};
        }
        if(this.bodyContent==undefined || this.bodyContent==null){
            this.bodyContent=[];
        }
        if(this.cssContent==undefined || this.cssContent==null){
            this.cssContent={};
        }
        if(this.preBodyContent==undefined || this.preBodyContent==null){
            this.preBodyContent=[];
        }
        if(this.aftBodyContent==undefined || this.aftBodyContent==null){
            this.aftBodyContent=[];
        }
        if(isNull(this.dolt)){
            this.dolt=defaultDolt;
        }
    };
    return this;
};