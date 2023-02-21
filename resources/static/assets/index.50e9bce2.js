var e=Object.defineProperty,a=Object.getOwnPropertySymbols,l=Object.prototype.hasOwnProperty,t=Object.prototype.propertyIsEnumerable,o=(a,l,t)=>l in a?e(a,l,{enumerable:!0,configurable:!0,writable:!0,value:t}):a[l]=t;import{T as r}from"./index.1ae80648.js";import{a as n,u as s,g as i,d as u}from"./table.b0327cd7.js";import{d,L as m,r as c,_ as p,a as b,o as h,c as f,w as g,b as y,e as v,F as D,f as w,g as _,t as C,h as T,i as V,j as x,k as j,l as k,m as F}from"./index.202de73a.js";const O=[{value:1,label:"运动"},{value:2,label:"健身"},{value:3,label:"跑酷"},{value:4,label:"街舞"}],S=[{value:1,label:"今天"},{value:2,label:"明天"},{value:3,label:"后天"}],q=d({components:{Layer:m},props:{layer:{type:Object,default:()=>({show:!1,title:"",showButton:!0})}},setup(e,a){const l=c(null),t=c(null);let o=c({name:""});return e.layer.row&&(o.value=JSON.parse(JSON.stringify(e.layer.row))),{form:o,rules:{name:[{required:!0,message:"请输入姓名",trigger:"blur"}],number:[{required:!0,message:"请输入数字",trigger:"blur"}],choose:[{required:!0,message:"请选择",trigger:"blur"}],radio:[{required:!0,message:"请选择",trigger:"blur"}]},layerDom:t,ruleForm:l,selectData:O,radioData:S}},methods:{submit(){this.ruleForm&&this.ruleForm.validate((e=>{if(!e)return!1;{let e=this.form;this.layer.row?this.updateForm(e):this.addForm(e)}}))},addForm(e){n(e).then((e=>{this.$message({type:"success",message:"新增成功"}),this.$emit("getTableData",!0),this.layerDom&&this.layerDom.close()}))},updateForm(e){s(e).then((e=>{this.$message({type:"success",message:"编辑成功"}),this.$emit("getTableData",!1),this.layerDom&&this.layerDom.close()}))}}});const N=d({name:"crudTable",components:{Table:r,Layer:p(q,[["render",function(e,a,l,t,o,r){const n=b("el-input"),s=b("el-form-item"),i=b("el-option"),u=b("el-select"),d=b("el-radio"),m=b("el-radio-group"),c=b("el-form"),p=b("Layer",!0);return h(),f(p,{layer:e.layer,onConfirm:e.submit,ref:"layerDom"},{default:g((()=>[y(c,{model:e.form,rules:e.rules,ref:"ruleForm","label-width":"120px",style:{"margin-right":"30px"}},{default:g((()=>[y(s,{label:"名称：",prop:"name"},{default:g((()=>[y(n,{modelValue:e.form.name,"onUpdate:modelValue":a[0]||(a[0]=a=>e.form.name=a),placeholder:"请输入名称"},null,8,["modelValue"])])),_:1}),y(s,{label:"数字：",prop:"number"},{default:g((()=>[y(n,{modelValue:e.form.number,"onUpdate:modelValue":a[1]||(a[1]=a=>e.form.number=a),oninput:"value=value.replace(/[^\\d]/g,'')",placeholder:"只能输入正整数"},null,8,["modelValue"])])),_:1}),y(s,{label:"选择器：",prop:"select"},{default:g((()=>[y(u,{modelValue:e.form.choose,"onUpdate:modelValue":a[2]||(a[2]=a=>e.form.choose=a),placeholder:"请选择",clearable:""},{default:g((()=>[(h(!0),v(D,null,w(e.selectData,(e=>(h(),f(i,{key:e.value,label:e.label,value:e.value},null,8,["label","value"])))),128))])),_:1},8,["modelValue"])])),_:1}),_(" "+C(e.form.radio)+" ",1),y(s,{label:"单选框：",prop:"radio"},{default:g((()=>[y(m,{modelValue:e.form.value,"onUpdate:modelValue":a[3]||(a[3]=a=>e.form.value=a)},{default:g((()=>[(h(!0),v(D,null,w(e.radioData,(e=>(h(),f(d,{key:e.value,label:e.value},{default:g((()=>[_(C(e.value),1)])),_:2},1032,["label"])))),128))])),_:1},8,["modelValue"])])),_:1})])),_:1},8,["model","rules"])])),_:1},8,["layer","onConfirm"])}]])},setup(){const e=T({input:""}),r=T({show:!1,title:"新增",showButton:!0}),n=T({index:1,size:20,total:0}),s=c(!0),d=c([]),m=c([]),p=r=>{s.value=!0,r&&(n.index=1);let u=((e,r)=>{for(var n in r||(r={}))l.call(r,n)&&o(e,n,r[n]);if(a)for(var n of a(r))t.call(r,n)&&o(e,n,r[n]);return e})({page:n.index,pageSize:n.size},e);console.log(u),i(u).then((e=>{console.log(e);let a=e.data.list;console.log(Array.isArray(a)),Array.isArray(a)&&a.forEach((e=>{const a=O.find((a=>a.value===e.choose));e.chooseName=a?a.label:e.choose;const l=S.find((a=>a.value===e.radio));l?e.radioName=l.label:e.radio})),d.value=e.data.list,n.total=Number(e.data.pager.total)})).catch((e=>{d.value=[],n.index=1,n.total=0})).finally((()=>{s.value=!1}))};return p(!0),{query:e,tableData:d,chooseData:m,loading:s,page:n,layer:r,handleSelectionChange:e=>{m.value=e},handleAdd:()=>{r.title="新增数据",r.show=!0,delete r.row},handleEdit:e=>{r.title="编辑数据",r.row=e,r.show=!0},handleDel:e=>{let a={ids:e.map((e=>e.id)).join(",")};u(a).then((e=>{F({type:"success",message:"删除成功"}),p(1===d.value.length)}))},getTableData:p}}}),A={class:"layout-container"},U={class:"layout-container-form flex space-between"},L={class:"layout-container-form-handle"},E={class:"layout-container-form-search"},G={class:"layout-container-table"};var $=p(N,[["render",function(e,a,l,t,o,r){const n=b("el-button"),s=b("el-popconfirm"),i=b("el-input"),u=b("el-table-column"),d=b("Table"),m=b("Layer"),c=V("loading");return h(),v("div",A,[x("div",U,[x("div",L,[y(n,{type:"primary",icon:"el-icon-circle-plus-outline",onClick:e.handleAdd},{default:g((()=>[_("新增")])),_:1},8,["onClick"]),y(s,{title:"批量删除",onConfirm:a[0]||(a[0]=a=>e.handleDel(e.chooseData))},{reference:g((()=>[y(n,{type:"danger",icon:"el-icon-delete",disabled:0===e.chooseData.length},{default:g((()=>[_("批量删除")])),_:1},8,["disabled"])])),_:1})]),x("div",E,[y(i,{modelValue:e.query.input,"onUpdate:modelValue":a[1]||(a[1]=a=>e.query.input=a),placeholder:"请输入关键词进行检索",onChange:a[2]||(a[2]=a=>e.getTableData(!0))},null,8,["modelValue"]),y(n,{type:"primary",icon:"el-icon-search",class:"search-btn",onClick:a[3]||(a[3]=a=>e.getTableData(!0))},{default:g((()=>[_("搜索")])),_:1})])]),x("div",G,[j((h(),f(d,{ref:"table",page:e.page,"onUpdate:page":a[4]||(a[4]=a=>e.page=a),showIndex:!0,showSelection:!0,data:e.tableData,onGetTableData:e.getTableData,onSelectionChange:e.handleSelectionChange},{default:g((()=>[y(u,{prop:"name",label:"名称",align:"center"}),y(u,{prop:"number",label:"数字",align:"center"}),y(u,{prop:"chooseName",label:"选择器",align:"center"}),y(u,{prop:"radioName",label:"单选框",align:"center"}),y(u,{label:"操作",align:"center",fixed:"right",width:"200"},{default:g((a=>[y(n,{onClick:l=>e.handleEdit(a.row)},{default:g((()=>[_("编辑")])),_:2},1032,["onClick"]),y(s,{title:"删除",onConfirm:l=>e.handleDel([a.row])},{reference:g((()=>[y(n,{type:"danger"},{default:g((()=>[_("删除")])),_:1})])),_:2},1032,["onConfirm"])])),_:1})])),_:1},8,["page","data","onGetTableData","onSelectionChange"])),[[c,e.loading]]),e.layer.show?(h(),f(m,{key:0,layer:e.layer,onGetTableData:e.getTableData},null,8,["layer","onGetTableData"])):k("",!0)])])}]]);export{$ as default};