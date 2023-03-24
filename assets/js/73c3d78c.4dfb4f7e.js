"use strict";(self.webpackChunksynopsys_documentation=self.webpackChunksynopsys_documentation||[]).push([[153],{3905:(e,t,n)=>{n.d(t,{Zo:()=>c,kt:()=>f});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function s(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?s(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):s(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},s=Object.keys(e);for(r=0;r<s.length;r++)n=s[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);for(r=0;r<s.length;r++)n=s[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var i=r.createContext({}),u=function(e){var t=r.useContext(i),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},c=function(e){var t=u(e.components);return r.createElement(i.Provider,{value:t},e.children)},p="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},m=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,s=e.originalType,i=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),p=u(n),m=a,f=p["".concat(i,".").concat(m)]||p[m]||d[m]||s;return n?r.createElement(f,o(o({ref:t},c),{},{components:n})):r.createElement(f,o({ref:t},c))}));function f(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var s=n.length,o=new Array(s);o[0]=m;var l={};for(var i in t)hasOwnProperty.call(t,i)&&(l[i]=t[i]);l.originalType=e,l[p]="string"==typeof e?e:a,o[1]=l;for(var u=2;u<s;u++)o[u]=n[u];return r.createElement.apply(null,o)}return r.createElement.apply(null,n)}m.displayName="MDXCreateElement"},5162:(e,t,n)=>{n.d(t,{Z:()=>o});var r=n(7294),a=n(6010);const s={tabItem:"tabItem_Ymn6"};function o(e){let{children:t,hidden:n,className:o}=e;return r.createElement("div",{role:"tabpanel",className:(0,a.Z)(s.tabItem,o),hidden:n},t)}},4866:(e,t,n)=>{n.d(t,{Z:()=>k});var r=n(7462),a=n(7294),s=n(6010),o=n(2466),l=n(6550),i=n(1980),u=n(7392),c=n(12);function p(e){return function(e){return a.Children.map(e,(e=>{if((0,a.isValidElement)(e)&&"value"in e.props)return e;throw new Error(`Docusaurus error: Bad <Tabs> child <${"string"==typeof e.type?e.type:e.type.name}>: all children of the <Tabs> component should be <TabItem>, and every <TabItem> should have a unique "value" prop.`)}))}(e).map((e=>{let{props:{value:t,label:n,attributes:r,default:a}}=e;return{value:t,label:n,attributes:r,default:a}}))}function d(e){const{values:t,children:n}=e;return(0,a.useMemo)((()=>{const e=t??p(n);return function(e){const t=(0,u.l)(e,((e,t)=>e.value===t.value));if(t.length>0)throw new Error(`Docusaurus error: Duplicate values "${t.map((e=>e.value)).join(", ")}" found in <Tabs>. Every value needs to be unique.`)}(e),e}),[t,n])}function m(e){let{value:t,tabValues:n}=e;return n.some((e=>e.value===t))}function f(e){let{queryString:t=!1,groupId:n}=e;const r=(0,l.k6)(),s=function(e){let{queryString:t=!1,groupId:n}=e;if("string"==typeof t)return t;if(!1===t)return null;if(!0===t&&!n)throw new Error('Docusaurus error: The <Tabs> component groupId prop is required if queryString=true, because this value is used as the search param name. You can also provide an explicit value such as queryString="my-search-param".');return n??null}({queryString:t,groupId:n});return[(0,i._X)(s),(0,a.useCallback)((e=>{if(!s)return;const t=new URLSearchParams(r.location.search);t.set(s,e),r.replace({...r.location,search:t.toString()})}),[s,r])]}function b(e){const{defaultValue:t,queryString:n=!1,groupId:r}=e,s=d(e),[o,l]=(0,a.useState)((()=>function(e){let{defaultValue:t,tabValues:n}=e;if(0===n.length)throw new Error("Docusaurus error: the <Tabs> component requires at least one <TabItem> children component");if(t){if(!m({value:t,tabValues:n}))throw new Error(`Docusaurus error: The <Tabs> has a defaultValue "${t}" but none of its children has the corresponding value. Available values are: ${n.map((e=>e.value)).join(", ")}. If you intend to show no default tab, use defaultValue={null} instead.`);return t}const r=n.find((e=>e.default))??n[0];if(!r)throw new Error("Unexpected error: 0 tabValues");return r.value}({defaultValue:t,tabValues:s}))),[i,u]=f({queryString:n,groupId:r}),[p,b]=function(e){let{groupId:t}=e;const n=function(e){return e?`docusaurus.tab.${e}`:null}(t),[r,s]=(0,c.Nk)(n);return[r,(0,a.useCallback)((e=>{n&&s.set(e)}),[n,s])]}({groupId:r}),h=(()=>{const e=i??p;return m({value:e,tabValues:s})?e:null})();(0,a.useLayoutEffect)((()=>{h&&l(h)}),[h]);return{selectedValue:o,selectValue:(0,a.useCallback)((e=>{if(!m({value:e,tabValues:s}))throw new Error(`Can't select invalid tab value=${e}`);l(e),u(e),b(e)}),[u,b,s]),tabValues:s}}var h=n(2389);const y={tabList:"tabList__CuJ",tabItem:"tabItem_LNqP"};function w(e){let{className:t,block:n,selectedValue:l,selectValue:i,tabValues:u}=e;const c=[],{blockElementScrollPositionUntilNextRender:p}=(0,o.o5)(),d=e=>{const t=e.currentTarget,n=c.indexOf(t),r=u[n].value;r!==l&&(p(t),i(r))},m=e=>{let t=null;switch(e.key){case"Enter":d(e);break;case"ArrowRight":{const n=c.indexOf(e.currentTarget)+1;t=c[n]??c[0];break}case"ArrowLeft":{const n=c.indexOf(e.currentTarget)-1;t=c[n]??c[c.length-1];break}}t?.focus()};return a.createElement("ul",{role:"tablist","aria-orientation":"horizontal",className:(0,s.Z)("tabs",{"tabs--block":n},t)},u.map((e=>{let{value:t,label:n,attributes:o}=e;return a.createElement("li",(0,r.Z)({role:"tab",tabIndex:l===t?0:-1,"aria-selected":l===t,key:t,ref:e=>c.push(e),onKeyDown:m,onClick:d},o,{className:(0,s.Z)("tabs__item",y.tabItem,o?.className,{"tabs__item--active":l===t})}),n??t)})))}function g(e){let{lazy:t,children:n,selectedValue:r}=e;if(n=Array.isArray(n)?n:[n],t){const e=n.find((e=>e.props.value===r));return e?(0,a.cloneElement)(e,{className:"margin-top--md"}):null}return a.createElement("div",{className:"margin-top--md"},n.map(((e,t)=>(0,a.cloneElement)(e,{key:t,hidden:e.props.value!==r}))))}function v(e){const t=b(e);return a.createElement("div",{className:(0,s.Z)("tabs-container",y.tabList)},a.createElement(w,(0,r.Z)({},e,t)),a.createElement(g,(0,r.Z)({},e,t)))}function k(e){const t=(0,h.Z)();return a.createElement(v,(0,r.Z)({key:String(t)},e))}},7814:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>c,contentTitle:()=>i,default:()=>f,frontMatter:()=>l,metadata:()=>u,toc:()=>p});var r=n(7462),a=(n(7294),n(3905)),s=n(4866),o=n(5162);const l={sidebar_position:5,description:"Implement workflows using consumers"},i="Flows",u={unversionedId:"tutorials/basics/create-flows",id:"tutorials/basics/create-flows",title:"Flows",description:"Implement workflows using consumers",source:"@site/docs/tutorials/basics/create-flows.mdx",sourceDirName:"tutorials/basics",slug:"/tutorials/basics/create-flows",permalink:"/synopsys/docs/tutorials/basics/create-flows",draft:!1,editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/tutorials/basics/create-flows.mdx",tags:[],version:"current",sidebarPosition:5,frontMatter:{sidebar_position:5,description:"Implement workflows using consumers"},sidebar:"tutorialSidebar",previous:{title:"Consumers",permalink:"/synopsys/docs/tutorials/basics/create-consumer"},next:{title:"Plays",permalink:"/synopsys/docs/tutorials/basics/create-play"}},c={},p=[{value:"Definition",id:"definition",level:2},{value:"Create a flow",id:"create-a-flow",level:2}],d={toc:p},m="wrapper";function f(e){let{components:t,...n}=e;return(0,a.kt)(m,(0,r.Z)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"flows"},"Flows"),(0,a.kt)("p",null,(0,a.kt)("a",{parentName:"p",href:"/synopsys/docs/tutorials/basics/create-subscriber"},"Consumers")," can be useful to process messages in order, however, they have no concept of worflows or steps."),(0,a.kt)("p",null,"If a usecase requires a first consumer to process a message, then to publish another message which will be processed by another consumer, there is\nno way to capture the relation between the two consumers (until now)."),(0,a.kt)("p",null,"Flows can be used to express relation between consumers, and as such, can be used to declare multi-steps workflows with ",(0,a.kt)("strong",{parentName:"p"},"at least once delivery")," guarantee."),(0,a.kt)("h2",{id:"definition"},"Definition"),(0,a.kt)("admonition",{title:"What is a flow",type:"info"},(0,a.kt)("p",{parentName:"admonition"},"A flow is a set of steps consuming typed messages and returning typed results.\nA Directed Acyclic Graph can be inferred based on flow definition.\nEach time a flow step generates a result, it is published into the next step channel in order to trigger next step.")),(0,a.kt)("admonition",{title:"Auto-ack",type:"tip"},(0,a.kt)("p",{parentName:"admonition"},"Unlike classic consumers, flow steps handlers do NOT need to acknowledge messages. Messages are acknowledged\nautomatically, after step result is obtained, and message has been published successfully to next step only.")),(0,a.kt)("h2",{id:"create-a-flow"},"Create a flow"),(0,a.kt)(s.Z,{mdxType:"Tabs"},(0,a.kt)(o.Z,{value:"python",label:"Python SDK",default:!0,mdxType:"TabItem"},(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"from synopsys import create_flow, Step\nfrom .channels import MEASUREMENTS, STEP1, STEP2, COMPLETE, DEAD_LETTER\n\n\nFLOW = create_flow(\n    Step(\n        MEASUREMENTS,\n        handler=...,\n        success=STEP1,\n        failure=DEAD_LETTER,\n    ),\n    Step(\n        STEP1,\n        handler=...,\n        success=STEP2,\n        failure=DEAD_LETTER,\n    ),\n    Step(\n        STEP2,\n        handler=...,\n        success=COMPLETE,\n        failure=DEAD_LETTER,\n    ),\n    Step(\n        COMPLETE,\n        handler=...,\n        final=True,\n    )\n    Step(\n        DEAD_LETTER,\n        handler=...,\n        final=True,\n    ),\n)\n")),(0,a.kt)("admonition",{title:"Flow verifications",type:"tip"},(0,a.kt)("p",{parentName:"admonition"},"A flow must have exactly ",(0,a.kt)("inlineCode",{parentName:"p"},"1")," final step for each flow branch."),(0,a.kt)("p",{parentName:"admonition"},"This is verified at runtime when flow is defined. It this is not the case, an error is raised.")),(0,a.kt)("admonition",{title:"Handler signatures",type:"tip"},(0,a.kt)("p",{parentName:"admonition"},"Each handler must accept a single argument which is a ",(0,a.kt)("inlineCode",{parentName:"p"},"Message[DataT, ParamsT]")," when ",(0,a.kt)("inlineCode",{parentName:"p"},"DataT")," and ",(0,a.kt)("inlineCode",{parentName:"p"},"ParamsT")," are defined by the input channel.\nMoreover, if a step has a ",(0,a.kt)("inlineCode",{parentName:"p"},"success")," defined, handler must return a value according to ",(0,a.kt)("inlineCode",{parentName:"p"},"success")," channel schema."),(0,a.kt)("p",{parentName:"admonition"},"Bonus: ",(0,a.kt)("a",{parentName:"p",href:"https://mypy.readthedocs.io/en/stable/"},(0,a.kt)("inlineCode",{parentName:"a"},"mypy"))," can be used to type check flow definitions \ud83c\udf89")))))}f.isMDXComponent=!0}}]);