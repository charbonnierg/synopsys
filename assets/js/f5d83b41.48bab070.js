"use strict";(self.webpackChunksynopsys_documentation=self.webpackChunksynopsys_documentation||[]).push([[6036],{3905:(e,t,r)=>{r.d(t,{Zo:()=>p,kt:()=>f});var n=r(7294);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var l=n.createContext({}),c=function(e){var t=n.useContext(l),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},p=function(e){var t=c(e.components);return n.createElement(l.Provider,{value:t},e.children)},u="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},y=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,l=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),u=c(r),y=a,f=u["".concat(l,".").concat(y)]||u[y]||d[y]||o;return r?n.createElement(f,i(i({ref:t},p),{},{components:r})):n.createElement(f,i({ref:t},p))}));function f(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=y;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s[u]="string"==typeof e?e:a,i[1]=s;for(var c=2;c<o;c++)i[c]=r[c];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}y.displayName="MDXCreateElement"},9535:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>m,frontMatter:()=>o,metadata:()=>s,toc:()=>c});var n=r(7462),a=(r(7294),r(3905));const o={sidebar_position:6,description:"Declare group of actors which sould run together"},i="Plays",s={unversionedId:"tutorials/basics/create-play",id:"tutorials/basics/create-play",title:"Plays",description:"Declare group of actors which sould run together",source:"@site/docs/tutorials/basics/create-play.mdx",sourceDirName:"tutorials/basics",slug:"/tutorials/basics/create-play",permalink:"/synopsys/docs/tutorials/basics/create-play",draft:!1,editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/tutorials/basics/create-play.mdx",tags:[],version:"current",sidebarPosition:6,frontMatter:{sidebar_position:6,description:"Declare group of actors which sould run together"},sidebar:"tutorialSidebar",previous:{title:"Flows",permalink:"/synopsys/docs/tutorials/basics/create-flows"},next:{title:"Run plays",permalink:"/synopsys/docs/tutorials/basics/run-play"}},l={},c=[{value:"Definition",id:"definition",level:2},{value:"Create a play",id:"create-a-play",level:2}],p=e=>function(t){return console.warn("Component "+e+" was not imported, exported, or provided by MDXProvider as global scope"),(0,a.kt)("div",t)},u=p("Tabs"),d=p("TabItem"),y={toc:c},f="wrapper";function m(e){let{components:t,...r}=e;return(0,a.kt)(f,(0,n.Z)({},y,r,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"plays"},"Plays"),(0,a.kt)("p",null,"We've seen how to create and run different actors individually, but we have not introduced yet how to wire those actors together in order to build an application."),(0,a.kt)("h2",{id:"definition"},"Definition"),(0,a.kt)("admonition",{title:"What's a play ?",type:"info"},(0,a.kt)("p",{parentName:"admonition"},"A play is an asynchronous task manager designed for running actors in background.")),(0,a.kt)("p",null,"A play is used to express the different components of an application. It is responsible for:"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"starting actors on play startup"),(0,a.kt)("li",{parentName:"ul"},"starting new actors once play is started"),(0,a.kt)("li",{parentName:"ul"},"stopping actors while play is started"),(0,a.kt)("li",{parentName:"ul"},"stopping actors on play shutdown")),(0,a.kt)("h2",{id:"create-a-play"},"Create a play"),(0,a.kt)(u,{mdxType:"Tabs"},(0,a.kt)(d,{value:"python",label:"Python SDK",default:!0,mdxType:"TabItem"},(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},'from synopsys import Play\nfrom .actors import MEASUREMENTS_PROCESSOR, LOCATIONS_SERVICE, MEASUREMENTS_CONSUMER\n\n# highlight-start\nPlay(\n    name="test-app",\n    version="0.1.0",\n    actors=[\n        MEASUREMENTS_PROCESSOR,\n        LOCATIONS_SERVICE,\n        MEASUREMENTS_CONSUMER,\n    ],\n)\n# highlight-end\n')))))}m.isMDXComponent=!0}}]);