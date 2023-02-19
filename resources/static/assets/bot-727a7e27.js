import { i as t } from "./axios-f38a487f.js";
function i() {
  return t({ url: "/getLogList", method: "get" });
}
function o() {
  return t({ url: "/getConfig", method: "get" });
}
function r() {
  return t({ url: "/editInviteFriends", method: "post" });
}
function d() {
  return t({ url: "/editFollowChannel", method: "post" });
}
function u(e) {
  return t({ url: "/editInviteFriendsAutoClearTime", method: "post", data: e });
}
function s(e) {
  return t({ url: "/editDeleteSeconds", method: "post", data: e });
}
function l(e) {
  return t({ url: "/editInviteFriendsQuantity", method: "post", data: e });
}
export { s as a, u as b, r as c, d, l as e, i as f, o as g };
