import"./index.4d66c970.js";import{d as e,r as t,c as l,i as a,g as o,h as n,D as d,k as i,A as p,F as s,j as r,n as u,a as m,R as c,q as f,b as g,t as b,y as h,f as v,B as y}from"./vendor.e45b1972.js";import{d as j}from"./dynamicLoadScript.32e4a333.js";import{_ as w}from"./notification.8e3fe923.js";const _={style:{"max-width":"50em",margin:"1em auto"}},x=a("span",{class:"commit"},[u(" (单位: "),a("strong",null,"秒"),u(") ")],-1),V=a("span",{class:"commit"},[u(" (单位: "),a("strong",null,"秒"),u(") ")],-1),I=a("span",{class:"commit"},[u(" (单位: "),a("strong",null,"M"),u("字节) ")],-1),S=a("span",{class:"commit"},"推荐采用md格式",-1),F=u("提交");var k=e({expose:[],props:{params:{type:Object,default:null}},setup(e){const u=e;let f={pdf:"pdf",md:"markdown",html:"html"},g=t(["特判程序","评测数据"]),b=t(u.params.problemId),h=t(u.params.title),v=t(u.params.source),y=t(u.params.author),j=t(u.params.docType),w=t(parseInt(u.params.timeLimit)),k=t(parseInt(u.params.timeLimitSpc)),U=t(parseInt(u.params.memoryLimit)),L=t(1==u.params.isSpj?"特判程序":"评测数据"),T=t(parseInt(u.params.judgeFiles)),P=t(u.params.score),D=c();function q(){let e=new Object;e.problemId=String(b.value),e.title=h.value,e.source=v.value,e.author=y.value,e.docType=j.value,e.timeLimit=String(w.value),e.timeLimitSpc=String(k.value),e.memoryLimit=String(U.value),e.isSpj=String("评测数据"==L.value?0:1),e.judgeFiles=String(T.value),e.score=String(P.value);let t=new Object;t.data=e,m.post("admin/problem/info",t),null==D||D.emit("go",{to:"uploadProblem",params:{docType:j.value,isSpj:String("评测数据"==L.value?0:1)}})}return(e,t)=>{const u=o("el-input"),m=o("el-form-item"),c=o("el-input-number"),D=o("el-option"),C=o("el-select"),E=o("el-form"),z=o("el-button");return n(),l("div",_,[a(E,{"label-width":"80px",style:{"margin-left":"auto"}},{default:d((()=>[a(m,{label:"题目ID"},{default:d((()=>[a(u,{modelValue:i(b),"onUpdate:modelValue":t[1]||(t[1]=e=>p(b)?b.value=e:b=e),style:{width:"300px"},disabled:!0},null,8,["modelValue"])])),_:1}),a(m,{label:"题目标题"},{default:d((()=>[a(u,{modelValue:i(h),"onUpdate:modelValue":t[2]||(t[2]=e=>p(h)?h.value=e:h=e),style:{width:"300px"}},null,8,["modelValue"])])),_:1}),a(m,{label:"题目时限"},{default:d((()=>[a(c,{modelValue:i(w),"onUpdate:modelValue":t[3]||(t[3]=e=>p(w)?w.value=e:w=e),"controls-position":"right",style:{width:"150px"}},null,8,["modelValue"]),x])),_:1}),a(m,{label:"特别时限"},{default:d((()=>[a(c,{modelValue:i(k),"onUpdate:modelValue":t[4]||(t[4]=e=>p(k)?k.value=e:k=e),"controls-position":"right",style:{width:"150px"}},null,8,["modelValue"]),V])),_:1}),a(m,{label:"内存限制"},{default:d((()=>[a(c,{modelValue:i(U),"onUpdate:modelValue":t[5]||(t[5]=e=>p(U)?U.value=e:U=e),"controls-position":"right",style:{width:"150px"}},null,8,["modelValue"]),I])),_:1}),a(m,{label:"分数"},{default:d((()=>[a(u,{modelValue:i(P),"onUpdate:modelValue":t[6]||(t[6]=e=>p(P)?P.value=e:P=e),style:{width:"300px"}},null,8,["modelValue"])])),_:1}),a(m,{label:"题目作者"},{default:d((()=>[a(u,{modelValue:i(y),"onUpdate:modelValue":t[7]||(t[7]=e=>p(y)?y.value=e:y=e),style:{width:"300px"}},null,8,["modelValue"])])),_:1}),a(m,{label:"题目来源"},{default:d((()=>[a(u,{modelValue:i(v),"onUpdate:modelValue":t[8]||(t[8]=e=>p(v)?v.value=e:v=e),style:{width:"300px"}},null,8,["modelValue"])])),_:1}),a(m,{label:"题面类型"},{default:d((()=>[a(C,{modelValue:i(j),"onUpdate:modelValue":t[9]||(t[9]=e=>p(j)?j.value=e:j=e)},{default:d((()=>[(n(!0),l(s,null,r(i(f),((e,t)=>(n(),l(D,{key:t,label:e,value:t},null,8,["label","value"])))),128))])),_:1},8,["modelValue"]),S])),_:1}),a(m,{label:"判题方式"},{default:d((()=>[a(C,{modelValue:i(L),"onUpdate:modelValue":t[10]||(t[10]=e=>p(L)?L.value=e:L=e)},{default:d((()=>[(n(!0),l(s,null,r(i(g),((e,t)=>(n(),l(D,{key:t,label:e,value:e},null,8,["label","value"])))),128))])),_:1},8,["modelValue"])])),_:1}),a(m,{label:"评测组数"},{default:d((()=>[a(c,{modelValue:i(T),"onUpdate:modelValue":t[11]||(t[11]=e=>p(T)?T.value=e:T=e),"controls-position":"right",style:{width:"150px"}},null,8,["modelValue"])])),_:1})])),_:1}),a(z,{onClick:q},{default:d((()=>[F])),_:1})])}}});const U=u("选择文件(PDF)"),L=u("提交");var T=e({expose:[],props:{problemId:{type:String,default:""}},setup(e){const p=e;let s=c(),r=t(),u=t(0);function f(e,t){u.value=0}function g(e){let t=new FormData;t.append("problemFile",e.file),t.append("problemId",String(p.problemId)),t.append("docType","pdf");const l={onUploadProgress:e=>{u.value=Number((e.loaded/e.total*100).toFixed(2))}};m.post("/admin/problem/doc",t,l)}function b(){null==s||s.emit("go",{to:"uploadData"})}return(e,t)=>{const p=o("el-button"),s=o("el-upload"),m=o("el-progress");return n(),l("div",null,[a(s,{id:"upload",class:"upload-demo",action:"#",style:{width:"200px"},multiple:!1,limit:1,"http-request":g,"on-remove":f,"show-file-list":!0,accept:".pdf","file-list":i(r)},{default:d((()=>[a(p,{type:"primary"},{default:d((()=>[U])),_:1})])),_:1},8,["file-list"]),a(m,{"stroke-width":16,percentage:i(u)},null,8,["percentage"]),a(p,{style:{"margin-top":"20px"},onClick:b},{default:d((()=>[L])),_:1})])}}});const P=u("选择文件(HTML)"),D=u("提交");var q=e({expose:[],props:{problemId:{type:String,default:""}},setup(e){const p=e;let s=c(),r=t(),u=t(0);function f(e,t){u.value=0}function g(e){let t=new FormData;t.append("problemFile",e.file),t.append("problemId",String(p.problemId)),t.append("docType","html");const l={onUploadProgress:e=>{u.value=Number((e.loaded/e.total*100).toFixed(2))}};m.post("/admin/problem/doc",t,l).then((e=>{}))}function b(){null==s||s.emit("go",{to:"uploadData"})}return(e,t)=>{const p=o("el-button"),s=o("el-upload"),m=o("el-progress");return n(),l("div",null,[a(s,{id:"upload",class:"upload-demo",action:"#",style:{width:"200px"},multiple:!1,limit:1,"http-request":g,"show-file-list":!0,accept:".html","on-remove":f,"file-list":i(r)},{default:d((()=>[a(p,{type:"primary"},{default:d((()=>[P])),_:1})])),_:1},8,["file-list"]),a(m,{"stroke-width":16,percentage:i(u)},null,8,["percentage"]),a(p,{style:{"margin-top":"20px"},onClick:b},{default:d((()=>[D])),_:1})])}}});const C={style:{height:"100%"}},E=a("div",{id:"docUpload"},null,-1),z=u("提交");var M=e({expose:[],props:{type:{type:String},problemId:{type:String},contestId:{type:String}},setup(e){const t=e;let i=f({editor:null}),p=c();function s(){var e=new URLSearchParams;e.append("problemId",t.problemId),e.append("docType","md"),e.append("problemContent",i.editor.getMarkdown()),m.post("/admin/problem/text",e).then((e=>{200==e.code&&w({title:"成功",message:"上传成功",type:"success"})})).catch((function(e){alert(e)})),null==p||p.emit("go",{to:"uploadData"})}function r(e){if(!e||0===e.length)throw new Error('argument "path" is required !');var t=document.getElementsByTagName("head")[0],l=document.createElement("link");l.href=e,l.rel="stylesheet",l.type="text/css",t.appendChild(l)}return g((async()=>{(async function(){r("/admin//editormd/css/editormd.css"),r("/admin//editormd/css/editormd.preview.min.css");const e=["https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js","https://cdnjs.gtimg.com/cdnjs/libs/zepto/1.1.4/zepto.min.js","https://cdn.jsdelivr.net/gh/yremp/editormd/editormd.js","https://cdn.jsdelivr.net/gh/yremp/editormd/lib/marked.min.js","https://cdn.jsdelivr.net/gh/yremp/editormd/lib/prettify.min.js","https://cdn.jsdelivr.net/gh/yremp/editormd/lib/flowchart.min.js","https://cdn.jsdelivr.net/gh/yremp/editormd/lib/underscore.min.js","https://cdn.jsdelivr.net/npm/pdfjs-dist@2.8.335/build/pdf.min.js"];return Promise.all(e.map((e=>j(e))))})().then((()=>{i.editor=editormd("docUpload",{width:"100%",height:"70vh",path:"/admin//editormd/lib/",codeFold:!0,saveHTMLToTextarea:!0,searchReplace:!0,taskList:!0,syncScrolling:"single",tex:!0,toolbarIcons:function(){return["undo","redo","|","bold","del","italic","quote","ucwords","uppercase","lowercase","|","h1","h2","h3","h4","h5","h6","|","list-ul","list-ol","hr","|","link","reference-link","code","preformatted-text","code-block","table","datetime","html-entities","pagebreak","|","goto-line","watch","preview","clear","search","|","help","info"]},onload:function(){}})}))})),(e,t)=>{const i=o("el-button");return n(),l("div",C,[E,a("div",null,[a(i,{plain:"",onClick:s},{default:d((()=>[z])),_:1})])])}}});const O=a("p",null,"上传ZIP文件.",-1),N=a("p",null,"(请确保你的测试文件名称为1-n, 并且以.in和.out为结尾)",-1),A=u("选择文件"),B=u("提交"),G=u("请保证评测数据组数为 ");var R=e({expose:[],props:{data:{type:Object,default:null}},setup(e){const p=e;let s=t(),r=new FormData,u=t(0);function c(e,t){u.value=0}function f(e){r.append("problemId",String(p.data.problemId)),r.append("judgeFile",e.file),r.append("judgeFiles",p.data.judgeFiles);const t={onUploadProgress:e=>{u.value=Number((e.loaded/e.total*100).toFixed(2))}};m.post("/admin/problem/data",r,t).then((e=>{}))}function g(){}return(e,t)=>{const r=o("el-button"),m=o("el-upload"),h=o("el-progress");return n(),l("div",null,[O,N,a(m,{id:"upload",class:"upload-demo",action:"#",style:{width:"200px"},multiple:!1,limit:1,"on-remove":c,"http-request":f,"show-file-list":!0,accept:".zip","file-list":i(s)},{default:d((()=>[a(r,{type:"primary"},{default:d((()=>[A])),_:1})])),_:1},8,["file-list"]),a(h,{"stroke-width":16,percentage:i(u)},null,8,["percentage"]),a(r,{style:{"margin-top":"20px"},onClick:g},{default:d((()=>[B])),_:1}),a("p",null,[G,a("strong",null,b(p.data.judgeFiles),1)])])}}});const H=a("div",null,[a("p",null,"提交特判程序")],-1),Z=a("p",null,"上传ZIP文件.",-1),J=a("p",null,"(请确保你的测试文件名称为1-n, 并且以.in和.out为结尾)",-1),K=u("选择文件"),Q=u("提交"),W=u("请保证评测数据组数为 "),X=a("div",{id:"editor"},null,-1),Y=u("提交");var $=e({expose:[],props:{data:{type:Object,default:null}},setup(e){const p=e;let s=t(),r=new FormData,u=t(0);function c(e,t){u.value=0}function h(e){r.append("problemId",String(p.data.problemId)),r.append("judgeFile",e.file),r.append("judgeFiles",p.data.judgeFiles);const t={onUploadProgress:e=>{u.value=Number((e.loaded/e.total*100).toFixed(2))}};m.post("/admin/problem/data",r,t).then((e=>{}))}function v(){}let y=async function(){return Promise.all(["http://cdn.bootcss.com/ace/1.2.4/ace.js","http://cdn.bootcss.com/ace/1.2.4/ext-language_tools.js","http://cdn.bootcss.com/ace/1.2.4/mode-c_cpp.js"].map((e=>j(e))))}();g((async()=>{await y,function(){let e="//input the spj source code\n";e+="#include <stdio.h>\n",e+="\n",e+="int main(int argc, char** argv) {\n",e+='    FILE* f_in = fopen(argv[1], "r"); //std data input\n',e+='    FILE* f_out = fopen(argv[2], "r"); //std data output\n',e+='    FILE* f_code = fopen(argv[3], "r"); //source code\n',e+='    FILE* u_out = fopen(argv[4], "r"); //user output\n\n',e+="    return 0;\n",e+="}\n",ace.require("ace/ext/language_tools"),_.editor=ace.edit("editor"),_.editor.setOptions({enableBasicAutocompletion:!0,enableSnippets:!0,enableLiveAutocompletion:!0}),_.editor.setTheme("ace/theme/eclipse"),_.editor.getSession().setMode("ace/mode/c_cpp"),_.editor.setFontSize(16),_.editor.setShowPrintMargin(!1);let t=_.editor.getValue();_.editor.find(t),_.editor.replace(""),_.editor.setValue(e)}()}));const _=f({editor:null});function x(){let e={data:{code:_.editor.getValue(),problemId:p.data.problemId}};m.post("admin/problem/spj",e),w({title:"成功",message:"上传成功",type:"success"})}return(e,t)=>{const r=o("el-button"),m=o("el-upload"),f=o("el-progress"),g=o("el-row"),y=o("el-col");return n(),l("div",null,[H,a("div",null,[Z,J,a(m,{id:"upload",class:"upload-demo",action:"#",style:{width:"200px"},multiple:!1,limit:1,"http-request":h,"on-remove":c,"show-file-list":!0,accept:".zip","file-list":i(s)},{default:d((()=>[a(r,{type:"primary"},{default:d((()=>[K])),_:1})])),_:1},8,["file-list"]),a(f,{"stroke-width":16,percentage:i(u)},null,8,["percentage"]),a(r,{style:{"margin-top":"20px"},onClick:v},{default:d((()=>[Q])),_:1}),a("p",null,[W,a("strong",null,b(p.data.judgeFiles),1)])]),a("div",null,[a(g,{gutter:20},{default:d((()=>[X])),_:1}),a(g,{gutter:20,class:"row"},{default:d((()=>[a(y,{span:8},{default:d((()=>[a(r,{type:"primary",size:"medium",plain:"",onClick:x},{default:d((()=>[Y])),_:1})])),_:1})])),_:1})])])}}}),ee=e({expose:[],setup(s){const r={pdf:T,md:M,html:q},u={0:R,1:$};let m=v().params,c=t(String(m.docType)),f=t("false"==String(m.isSpj)?"0":"1");const g=e({setup:()=>()=>h(r[c.value],{onGo:j})}),b=e({setup:()=>()=>h(u[f.value],{onGo:j})});function j({to:e,params:t}){t&&t.docType&&t.isSpj&&(c.value=t.docType,f.value=t.isSpj),w.value=e}t(!1);let w=t("basicInfo");return(e,t)=>{const s=o("el-tab-pane"),r=o("el-tabs");return n(),l("div",null,[a(r,{modelValue:i(w),"onUpdate:modelValue":t[1]||(t[1]=e=>p(w)?w.value=e:w=e),type:"border-card"},{default:d((()=>[a(s,{name:"basicInfo",label:"基本信息"},{default:d((()=>[a(k,{onGo:j,params:i(m)},null,8,["params"])])),_:1}),a(s,{name:"uploadProblem",label:"上传题面"},{default:d((()=>["uploadProblem"==i(w)?(n(),l(i(g),{key:0,problemId:i(m).problemId},null,8,["problemId"])):y("",!0)])),_:1}),a(s,{name:"uploadData",label:"评测数据"},{default:d((()=>[a(i(b),{data:i(m)},null,8,["data"])])),_:1})])),_:1},8,["modelValue"])])}}});export default ee;
