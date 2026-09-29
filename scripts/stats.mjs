// Renders assets/stats.svg: a year of contributions drawn as an oscilloscope trace.
// Usage: GITHUB_TOKEN=... node scripts/stats.mjs <login> <outfile>
import { writeFileSync } from "node:fs";

const [login = "GA16-24", outfile = "dist/stats.svg"] = process.argv.slice(2);
const query = `query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC) { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}`;

const res = await fetch("https://api.github.com/graphql", {
  method: "POST",
  headers: { Authorization: `bearer ${process.env.GITHUB_TOKEN}`, "Content-Type": "application/json" },
  body: JSON.stringify({ query, variables: { login } }),
});
const { data, errors } = await res.json();
if (errors) throw new Error(JSON.stringify(errors));

const u = data.user;
const cal = u.contributionsCollection.contributionCalendar;
const days = cal.weeks.flatMap((w) => w.contributionDays);
const weeks = cal.weeks.map((w) => w.contributionDays.reduce((s, d) => s + d.contributionCount, 0));

let longest = 0, run = 0;
for (const d of days) { run = d.contributionCount ? run + 1 : 0; longest = Math.max(longest, run); }
// Today may still be empty, so the current streak can start from yesterday.
let current = 0;
for (let i = days.length - 1; i >= 0; i--) {
  if (days[i].contributionCount) current++;
  else if (i !== days.length - 1) break;
}
const best = days.reduce((a, d) => (d.contributionCount > a.contributionCount ? d : a), days[0]);

// Trace
const X0 = 330, X1 = 970, Y0 = 44, Y1 = 196;
const max = Math.max(...weeks, 1);
const pts = weeks.map((v, i) => [X0 + (i / (weeks.length - 1)) * (X1 - X0), Y1 - (v / max) * (Y1 - Y0)]);
let d = `M${pts[0][0].toFixed(1)},${pts[0][1].toFixed(1)}`;
for (let i = 1; i < pts.length; i++) {
  const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], mx = (x0 + x1) / 2;
  d += ` C${mx.toFixed(1)},${y0.toFixed(1)} ${mx.toFixed(1)},${y1.toFixed(1)} ${x1.toFixed(1)},${y1.toFixed(1)}`;
}
const area = `${d} L${X1},${Y1} L${X0},${Y1} Z`;
const [lx, ly] = pts[pts.length - 1];

const grid = [];
for (let x = X0; x <= X1; x += 64) grid.push(`<line x1="${x}" y1="${Y0 - 14}" x2="${x}" y2="${Y1}"/>`);
for (let y = Y0 - 14; y <= Y1; y += 38) grid.push(`<line x1="${X0}" y1="${y}" x2="${X1}" y2="${y}"/>`);

const fmt = (n) => n.toLocaleString("en-US");
const rows = [
  ["CONTRIBUTIONS / YR", fmt(cal.totalContributions)],
  ["CURRENT STREAK", `${current}d`],
  ["LONGEST STREAK", `${longest}d`],
  ["PEAK DAY", `${best.contributionCount} · ${best.date.slice(5)}`],
  ["PRS · COMMITS", `${u.contributionsCollection.totalPullRequestContributions} · ${fmt(u.contributionsCollection.totalCommitContributions)}`],
];
const stats = rows.map(([k, v], i) => `
    <g class="row" style="animation-delay:${(i * 0.15).toFixed(2)}s">
      <text x="30" y="${56 + i * 36}" class="k">${k}</text>
      <text x="290" y="${56 + i * 36}" class="v" text-anchor="end">${v}</text>
    </g>`).join("");

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 240" width="1000" height="240">
  <defs>
    <filter id="glow" x="-10%" y="-30%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="fill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#39ff88" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#39ff88" stop-opacity="0"/>
    </linearGradient>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity="0.3"/></pattern>
    <radialGradient id="bg" cx="65%" cy="50%" r="80%"><stop offset="0" stop-color="#0c1a10"/><stop offset="1" stop-color="#040806"/></radialGradient>
    <clipPath id="c"><rect width="1000" height="240" rx="16"/></clipPath>
  </defs>
  <style>
    text { font-family: 'JetBrains Mono', 'SF Mono', ui-monospace, Menlo, Consolas, monospace; }
    .k { font-size: 11px; fill: #2f8a50; letter-spacing: 2px; }
    .v { font-size: 18px; font-weight: 700; fill: #39ff88; }
    .t { font-size: 11px; fill: #2f8a50; letter-spacing: 2px; }
    .grid line { stroke: #12301a; stroke-width: 1; }
    .row { opacity: 0; animation: in .4s ease-out forwards; }
    @keyframes in { from { opacity: 0; transform: translateX(-8px); } to { opacity: 1; transform: none; } }
    .trace { fill: none; stroke: #39ff88; stroke-width: 2.2; stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 2.4s ease-out .3s forwards; }
    .area { opacity: 0; animation: show .8s ease-out 2.2s forwards; }
    @keyframes draw { to { stroke-dashoffset: 0; } }
    @keyframes show { to { opacity: 1; } }
    .head { fill: #d8ffe6; opacity: 0; animation: show .1s 2.6s forwards, pulse 1.4s 2.7s ease-in-out infinite; }
    @keyframes pulse { 50% { r: 7; } }
  </style>
  <g clip-path="url(#c)">
    <rect width="1000" height="240" fill="url(#bg)"/>
    <line x1="310" y1="24" x2="310" y2="216" stroke="#1d4a28"/>
    <g class="grid">${grid.join("")}</g>
    <path class="area" d="${area}" fill="url(#fill)"/>
    <path class="trace" pathLength="1" d="${d}" filter="url(#glow)"/>
    <circle class="head" cx="${lx.toFixed(1)}" cy="${ly.toFixed(1)}" r="4" filter="url(#glow)"/>
    <text x="${X0}" y="220" class="t">52 WEEKS AGO</text>
    <text x="${X1}" y="220" class="t" text-anchor="end">NOW · PEAK ${max}/WK</text>
    ${stats}
    <rect width="1000" height="240" fill="url(#scan)"/>
  </g>
  <rect x="1" y="1" width="998" height="238" rx="15" fill="none" stroke="#1d4a28" stroke-width="2"/>
</svg>
`;
writeFileSync(outfile, svg);
console.log(`wrote ${outfile}: ${cal.totalContributions} contributions, streak ${current}/${longest}`);
