(window.webpackJsonp=window.webpackJsonp||[]).push([[12],{"7wo0":function(t,n,e){"use strict";e.r(n);var c=e("M0ag"),i=e("tyNb"),s=e("ey9i"),r=e("H+bZ"),a=e("ntpF"),o=e("fXoL"),b=e("1kSV"),l=e("3Pt+"),d=e("5eHb"),u=e("sYmb"),m=e("ofXK"),f=e("oZhZ");function g(t,n){if(1&t&&(o.Zb(0,"div",4),o.Rc(1,"\n    "),o.Ub(2,"label",5),o.Rc(3,"\n    "),o.Zb(4,"div",6),o.Rc(5,"\n      "),o.Ub(6,"input",7),o.Rc(7,"\n    "),o.Yb(),o.Rc(8,"\n  "),o.Yb()),2&t){const t=o.pc(2);o.Fb(2),o.wc("translate",t.setting.Name)}}function p(t,n){if(1&t&&(o.Zb(0,"div",4),o.Rc(1,"\n    "),o.Ub(2,"label",5),o.Rc(3,"\n    "),o.Zb(4,"div",6),o.Rc(5,"\n      "),o.Ub(6,"input",7),o.Rc(7,"\n    "),o.Yb(),o.Rc(8,"\n  "),o.Yb()),2&t){const t=o.pc(2);o.Fb(2),o.wc("translate",t.setting.Name)}}function v(t,n){if(1&t&&(o.Zb(0,"div",4),o.Rc(1,"\n    "),o.Ub(2,"label",5),o.Rc(3,"\n    "),o.Zb(4,"div",6),o.Rc(5,"\n      "),o.Ub(6,"input",8),o.Rc(7,"\n    "),o.Yb(),o.Rc(8,"\n  "),o.Yb()),2&t){const t=o.pc(2);o.Fb(2),o.wc("translate",t.setting.Name)}}function h(t,n){if(1&t&&(o.Zb(0,"div",4),o.Rc(1,"\n    "),o.Ub(2,"label",5),o.Rc(3,"\n    "),o.Zb(4,"div",6),o.Rc(5,"\n      "),o.Ub(6,"input",9),o.Rc(7,"\n    "),o.Yb(),o.Rc(8,"\n  "),o.Yb()),2&t){const t=o.pc(2);o.Fb(2),o.wc("translate",t.setting.Name)}}function R(t,n){if(1&t&&(o.Zb(0,"div",10),o.Rc(1,"\n    "),o.Ub(2,"input",11),o.Rc(3,"\n    "),o.Ub(4,"label",12),o.Rc(5,"\n  "),o.Yb()),2&t){const t=o.pc(2);o.Fb(2),o.wc("id",t.setting.Name),o.Fb(2),o.wc("for",t.setting.Name),o.wc("translate",t.setting.Name)}}function w(t,n){if(1&t&&(o.Zb(0,"div",1),o.Rc(1,"\n  "),o.Pc(2,g,9,1,"div",2),o.Rc(3,"\n  "),o.Pc(4,p,9,1,"div",2),o.Rc(5,"\n  "),o.Pc(6,v,9,1,"div",2),o.Rc(7,"\n  "),o.Pc(8,h,9,1,"div",2),o.Rc(9,"\n  "),o.Pc(10,R,6,3,"div",3),o.Rc(11,"\n"),o.Yb()),2&t){const t=o.pc();o.vc("formGroupName",t.setting.Name),o.Fb(2),o.vc("ngIf","str"===t.setting.DataType),o.Fb(2),o.vc("ngIf","path"===t.setting.DataType),o.Fb(2),o.vc("ngIf","int"===t.setting.DataType),o.Fb(2),o.vc("ngIf","hex"===t.setting.DataType),o.Fb(2),o.vc("ngIf","bool"===t.setting.DataType)}}new s.c("SettingComponent");let Z=(()=>{class t{constructor(t,n,e){this.formBuilder=t,this.fgd=n,this.translate=e}ngOnInit(){let t;t=this.formBuilder.group("hex"===this.setting.DataType?{current:["",l.t.compose([l.t.required,l.t.pattern("^[0-9A-Fa-f]+")])]}:"bool"===this.setting.DataType?{current:[]}:{current:["",l.t.required]}),this.fgd.form.addControl(this.setting.Name,t);const n=""!==this.setting.current_value?this.setting.current_value:this.setting.default_value;this.fgd.form.get(this.setting.Name).get("current").patchValue(n)}}return t.\u0275fac=function(n){return new(n||t)(o.Tb(l.e),o.Tb(l.i),o.Tb(u.d))},t.\u0275cmp=o.Nb({type:t,selectors:[["app-setting"]],inputs:{setting:"setting",advanced:"advanced"},features:[o.Eb([],[{provide:l.b,useExisting:l.i}])],decls:2,vars:1,consts:[[3,"formGroupName",4,"ngIf"],[3,"formGroupName"],["class","form-group row mt-2",4,"ngIf"],["class","row mt-2 custom-control custom-checkbox",4,"ngIf"],[1,"form-group","row","mt-2"],["for","current",1,"col-sm-6","col-form-label",3,"translate"],[1,"col-sm"],["type","text","formControlName","current",1,"w-100","form-control"],["type","number","formControlName","current",1,"w-50","form-control"],["type","text","formControlName","current",1,"w-50","form-control"],[1,"row","mt-2","custom-control","custom-checkbox"],["formControlName","current","type","checkbox",1,"custom-control-input","form-control",3,"id"],[1,"ml-3","custom-control-label",3,"for","translate"]],template:function(t,n){1&t&&(o.Pc(0,w,12,6,"div",0),o.Rc(1,"\n")),2&t&&o.vc("ngIf",!1===n.setting.Advanced||n.advanced===n.setting.Advanced)},directives:[m.n,l.o,l.j,f.a,u.a,l.c,f.d,l.n,l.g,l.r,l.a],styles:[".custom-control-input.is-valid[_ngcontent-%COMP%] ~ .custom-control-label[_ngcontent-%COMP%], was-validated[_ngcontent-%COMP%]   .custom-control-input[_ngcontent-%COMP%]:valid ~ .custom-control-label[_ngcontent-%COMP%]{color:#000}"]}),t})();const Y=["content"];function y(t,n){if(1&t&&(o.Xb(0),o.Rc(1,"\n                  "),o.Ub(2,"app-setting",24),o.Rc(3,"\n                "),o.Wb()),2&t){const t=n.$implicit,e=o.pc(4);o.Fb(2),o.vc("setting",t)("advanced",e.advanced)}}function k(t,n){if(1&t&&(o.Zb(0,"div",18),o.Rc(1,"\n            "),o.Ub(2,"div",19),o.Rc(3,"\n            "),o.Zb(4,"div",20),o.Rc(5,"\n              "),o.Zb(6,"div",21),o.Rc(7,"\n                "),o.Ub(8,"h5",22),o.Rc(9,"\n              "),o.Yb(),o.Rc(10,"\n              "),o.Zb(11,"div",23),o.Rc(12,"\n                "),o.Pc(13,y,4,2,"ng-container",12),o.Rc(14,"\n              "),o.Yb(),o.Rc(15,"\n            "),o.Yb(),o.Rc(16,"\n          "),o.Yb()),2&t){const t=o.pc().$implicit;o.Fb(2),o.xc("translate","setting.header.",t._Theme,""),o.Fb(6),o.xc("translate","setting.subtitle.",t._Theme,""),o.Fb(5),o.vc("ngForOf",t.ListOfSettings)}}function F(t,n){if(1&t&&(o.Zb(0,"div"),o.Rc(1,"\n          "),o.Pc(2,k,17,3,"div",17),o.Rc(3,"\n        "),o.Yb()),2&t){const t=n.$implicit,e=o.pc(2);o.Fb(2),o.vc("ngIf",e.hasBasicSettings(t.ListOfSettings))}}function S(t,n){if(1&t){const t=o.ac();o.Zb(0,"form",9),o.Rc(1,"\n    "),o.Zb(2,"div",10),o.Rc(3,"\n      "),o.Zb(4,"div",11),o.Rc(5,"\n        "),o.Pc(6,F,4,1,"div",12),o.Rc(7,"\n      "),o.Yb(),o.Rc(8,"\n      "),o.Zb(9,"div",13),o.Rc(10,"\n        "),o.Zb(11,"button",14),o.lc("click",(function(n){return o.Ic(t),o.pc().updateSettings()})),o.Yb(),o.Rc(12,"\n      "),o.Yb(),o.Rc(13,"\n    "),o.Yb(),o.Rc(14,"\n\n    "),o.Zb(15,"div",10),o.Rc(16,"\n      "),o.Ub(17,"div",15),o.Rc(18,"\n      "),o.Zb(19,"div",13),o.Rc(20,"\n        "),o.Zb(21,"button",16),o.lc("click",(function(n){return o.Ic(t),o.pc().updateSettings()})),o.Yb(),o.Rc(22,"\n      "),o.Yb(),o.Rc(23,"\n    "),o.Yb(),o.Rc(24,"\n  "),o.Yb()}if(2&t){const t=o.pc();o.vc("formGroup",t.form),o.Fb(6),o.vc("ngForOf",t.settings),o.Fb(5),o.vc("disabled",!t.form.valid),o.Fb(10),o.vc("disabled",!t.form.valid)}}function N(t,n){1&t&&(o.Rc(0,"\n  "),o.Zb(1,"div",25),o.Rc(2,"\n    "),o.Ub(3,"h4",26),o.Rc(4,"\n    "),o.Zb(5,"button",27),o.lc("click",(function(t){return n.$implicit.dismiss("Cross click")})),o.Rc(6,"\n      "),o.Zb(7,"span",28),o.Rc(8,"\xd7"),o.Yb(),o.Rc(9,"\n    "),o.Yb(),o.Rc(10,"\n  "),o.Yb(),o.Rc(11,"\n  "),o.Ub(12,"div",29),o.Rc(13,"\n  "),o.Zb(14,"div",30),o.Rc(15,"\n    "),o.Zb(16,"button",31),o.lc("click",(function(t){return n.$implicit.dismiss("cancel")})),o.Yb(),o.Rc(17,"\n  "),o.Yb(),o.Rc(18,"\n"))}new s.c("SettingsComponent");const T=[{path:"",component:(()=>{class t{constructor(t,n,e,c,i,s){this.modalService=t,this.apiService=n,this.formBuilder=e,this.toastr=c,this.headerService=i,this.translate=s,this.advanced=!1}ngOnInit(){this.form=this.formBuilder.group({}),this.apiService.getSettings().subscribe(t=>{this.settings=t,this.settings.sort((t,n)=>t._Order-n._Order)})}advancedSettings(t){this.advanced=!!t.currentTarget.checked}updateSettings(){this.form.invalid?this.form.markAsTouched():(Object.keys(this.form.value).forEach(t=>{!0===this.form.value[t].current?this.form.value[t].current=1:!1===this.form.value[t].current&&(this.form.value[t].current=0)}),this.apiService.putSettings(this.form.value).subscribe(t=>{this.form.markAsPristine(),this.toastr.success(this.translate.instant("api.global.succes.update.title")),this.apiService.getSettings().subscribe(t=>{this.settings=t,this.settings.sort((t,n)=>t._Order-n._Order)}),this.apiService.getRestartNeeded().subscribe(t=>{t.RestartNeeded&&!0===t.RestartNeeded&&(this.headerService.setRestart(!0),this.open(this.content))})}))}open(t){this.modalService.open(t,{ariaLabelledBy:"modal-basic-title"}).result.then(t=>{},t=>{})}hasBasicSettings(t){return!!this.advanced||t.filter(t=>!1===t.Advanced).length>0}}return t.\u0275fac=function(n){return new(n||t)(o.Tb(b.e),o.Tb(r.a),o.Tb(l.e),o.Tb(d.b),o.Tb(a.a),o.Tb(u.d))},t.\u0275cmp=o.Nb({type:t,selectors:[["app-settings"]],viewQuery:function(t,n){var e;1&t&&o.Xc(Y,!0),2&t&&o.Ec(e=o.mc())&&(n.content=e.first)},decls:22,vars:2,consts:[[1,"h-100"],[1,"switch","switch-sm","mr-2","pr-2","float-right"],["type","checkbox","id","switch-advanced",1,"switch",3,"checked","click"],["for","switch-advanced","translate","setting.advanced.button",1,"mb-0"],["translate","setting.help.legend"],["href","https://github.com/pipiche38/Domoticz-Zigate-Wiki/blob/master/en-eng/PluginConf.json.md","translate","setting.help.link","target","_blank"],[1,"mt-3"],[3,"formGroup",4,"ngIf"],["content",""],[3,"formGroup"],[1,"row"],[1,"col-sm-11","card-columns"],[4,"ngFor","ngForOf"],[1,"col-sm-1"],["translate","setting.validate.button",1,"w-100","btn","btn-primary",3,"disabled","click"],[1,"col-sm"],["translate","setting.validate.button",1,"btn","btn-primary","w-100",3,"disabled","click"],["class","card",4,"ngIf"],[1,"card"],[1,"card-header",3,"translate"],[1,"card-body"],[1,"card-title"],[3,"translate"],[1,"card-text"],[3,"setting","advanced"],[1,"modal-header"],["id","modal-basic-title","translate","setting.reloadplugin.alert.title",1,"modal-title"],["type","button","aria-label","Close",1,"close",3,"click"],["aria-hidden","true"],["translate","setting.reloadplugin.alert.subject",1,"modal-body"],[1,"modal-footer"],["type","button","translate","setting.reloadplugin.alert.cancel",1,"btn","btn-outline-dark",3,"click"]],template:function(t,n){1&t&&(o.Zb(0,"fieldset",0),o.Rc(1,"\n  "),o.Zb(2,"div",1),o.Rc(3,"\n    "),o.Zb(4,"input",2),o.lc("click",(function(t){return n.advancedSettings(t)})),o.Yb(),o.Rc(5,"\n    "),o.Ub(6,"label",3),o.Rc(7,"\n  "),o.Yb(),o.Rc(8,"\n\n  "),o.Ub(9,"legend",4),o.Rc(10,"\n  "),o.Ub(11,"a",5),o.Rc(12,"\n"),o.Yb(),o.Rc(13,"\n"),o.Zb(14,"div",6),o.Rc(15,"\n  "),o.Pc(16,S,25,4,"form",7),o.Rc(17,"\n"),o.Yb(),o.Rc(18,"\n\n"),o.Pc(19,N,19,0,"ng-template",null,8,o.Qc),o.Rc(21,"\n")),2&t&&(o.Fb(4),o.vc("checked",n.advanced),o.Fb(12),o.vc("ngIf",n.settings))},directives:[u.a,m.n,l.v,l.o,l.i,f.b,m.m,Z],styles:[""]}),t})(),data:{title:Object(s.d)("settings")}}];let P=(()=>{class t{}return t.\u0275mod=o.Rb({type:t}),t.\u0275inj=o.Qb({factory:function(n){return new(n||t)},providers:[],imports:[[i.i.forChild(T)],i.i]}),t})();e.d(n,"SettingsModule",(function(){return U}));let U=(()=>{class t{}return t.\u0275mod=o.Rb({type:t}),t.\u0275inj=o.Qb({factory:function(n){return new(n||t)},imports:[[P,c.a]]}),t})()}}]);