/* Compatibility for previously cached dashboard HTML. Analytics is hosted privately in Umami. */
(() => {
 'use strict';
 const login=document.getElementById('login'),owner=document.getElementById('owner'),status=document.getElementById('status');
 if(login)login.hidden=true;
 if(owner)owner.hidden=true;
 if(status)status.textContent='统计已迁移至 Umami。请点击上方统计链接；无需填写邮箱。刷新此页可使用新版中文入口。';
 document.querySelectorAll('a[href="https://cloud.umami.is/analytics/us/websites"]').forEach(a=>{a.href='https://cloud.umami.is/analytics/us/websites/96e0ff79-f76f-4bcf-bf0c-1532d3550f36';a.textContent='查看全站访问统计';});
})();
