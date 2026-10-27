// Real-time updates over WebSockets.
const scheme = location.protocol === "https:" ? "wss" : "ws";

// 1) Project board / task page: refresh the #live area whenever someone changes the project.
const live = document.getElementById("live");
if (live) {
  const ws = new WebSocket(`${scheme}://${location.host}/ws/project/${live.dataset.project}/`);
  ws.onmessage = async () => {
    const res = await fetch(location.href, {headers: {"x-requested-with": "fetch"}});
    const doc = new DOMParser().parseFromString(await res.text(), "text/html");
    const fresh = doc.getElementById("live");
    if (fresh) live.innerHTML = fresh.innerHTML;
  };
}

// 2) Notifications: update the bell badge and show a toast.
if (document.body.dataset.auth === "1") {
  const ws = new WebSocket(`${scheme}://${location.host}/ws/notifications/`);
  ws.onmessage = e => {
    const n = JSON.parse(e.data);
    const badge = document.getElementById("notif-count");
    badge.textContent = n.unread; badge.hidden = false;
    const t = document.getElementById("toast");
    t.innerHTML = ""; const a = document.createElement("a");
    a.href = n.url || "/notifications/"; a.textContent = n.text; t.appendChild(a);
    t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 4000);
  };
}
