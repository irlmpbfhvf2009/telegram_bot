import{f as l}from"./bot-727a7e27.js";import{_ as r,o as v,a as _,b as p,c as f,d as t,t as u,e as g,f as h,p as y,g as m}from"./index-e1e726b3.mjs";import"./axios-f38a487f.js";const a=c=>(y("data-v-4e6c1cc6"),c=c(),m(),c),b={class:"wrap"},x=a(()=>t("div",{class:"align-items-center"},null,-1)),w=a(()=>t("a",{href:"javascript:void(0);"},[t("i",{class:"mt-2 fas fa-bars text-white fa-2x"})],-1)),S=a(()=>t("div",{class:"text-light fz30"},"Log日誌",-1)),j={class:"content d-flex justify-content-center"},k={class:"inbody"},B={style:{"overflow-y":"hidden"}},I={style:{"white-space":"nowrap"},width:"100%"},L=g('<div class="footer border border-dark border-2" data-v-4e6c1cc6><div class="container" data-v-4e6c1cc6><div class="row text-center" data-v-4e6c1cc6><div class="col-4" data-v-4e6c1cc6><i class="fas fa-user" data-v-4e6c1cc6></i><div data-v-4e6c1cc6>使用者</div></div><div class="col-4" data-v-4e6c1cc6><i class="fas fa-home" data-v-4e6c1cc6></i><div data-v-4e6c1cc6>主頁</div></div><div class="col-4" data-v-4e6c1cc6><i class="far fa-file-alt" data-v-4e6c1cc6></i><div data-v-4e6c1cc6>管理面板</div></div></div></div></div>',1),N={__name:"log",setup(c){v(()=>{i()});const s=_("");async function i(){const e=await l(),o=JSON.stringify(e.data),d=JSON.parse(o);console.log(d.log_list),s.value=d.log_list}async function n(){localStorage.clear(),h.push("/login")}return(e,o)=>(p(),f("div",b,[t("div",{class:"header"},[t("div",{class:"d-flex justify-content-around pt-4 py-3"},[x,w,S,t("button",{type:"button",class:"mt-1 btn btn-danger rounded-pill btnLogout",onClick:n},"登出")])]),t("div",j,[t("div",k,[t("div",B,[t("pre",I,u(s.value),1)])])]),L]))}},V=r(N,[["__scopeId","data-v-4e6c1cc6"]]);export{V as default};
