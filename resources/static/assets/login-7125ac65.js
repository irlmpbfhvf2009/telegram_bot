import {
  _ as l,
  o as r,
  a as c,
  b as f,
  c as u,
  d as s,
  w as v,
  v as p,
  h as _,
  e as m,
} from "./index-e1e726b3.mjs";
import { g } from "./bot-727a7e27.js";
import "./axios-f38a487f.js";
const w = "/static/assets/user-bd070cfb.png";
const x = { class: "wrap" },
  y = m(
    '<div class="d-flex justify-content-center" data-v-386fa203><div class="fw-bold fs-3 mt-5 text-white" data-v-386fa203>welcome</div></div><div class="d-flex justify-content-center" data-v-386fa203><div class="fw-bold fs-3 mt-2 text-white" data-v-386fa203>你好!歡迎使用!</div></div><div class="d-flex justify-content-center" data-v-386fa203><img src="' +
      w +
      '" alt="" class="user" data-v-386fa203></div>',
    3
  ),
  b = { class: "d-flex justify-content-center mt-3" },
  h = { class: "d-flex justify-content-center mt-3" },
  j = {
    __name: "login",
    setup(B) {
      r(() => {
        i();
      });
      const d = c(""),
        a = c("");
      async function i() {
        const e = await g();
        d.password = e.data.password;
      }
      async function o(e) {
        ({ password: a.value }.password == 12356
          ? (console.log("登入成功"),
            localStorage.setItem("password", "True"),
            router.push("/log"))
          : console.log("登入失敗"));
      }
      return (e, t) => (
        f(),
        u("div", x, [
          y,
          s("div", b, [
            v(
              s(
                "input",
                {
                  type: "text",
                  class: "inputsize rounded-2 fw-light text-center fs-2",
                  placeholder: "請輸入密碼",
                  "onUpdate:modelValue": t[0] || (t[0] = (n) => (a.value = n)),
                },
                null,
                512
              ),
              [[p, a.value]]
            ),
          ]),
          s("div", h, [
            s(
              "button",
              {
                type: "button",
                class: "enterBtn btn btn-outline-success btn-lg ms-2",
                onKeyup: t[1] || (t[1] = _((n) => o(e.item), ["enter"])),
                onClick: o,
              },
              "登入",
              32
            ),
          ]),
        ])
      );
    },
  },
  D = l(j, [["__scopeId", "data-v-386fa203"]]);
export { D as default };
