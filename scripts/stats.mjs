// Renders stats.svg: a year of contributions drawn as a constellation.
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

// Constellation: one star per week, height and size follow that week's count.
const X0 = 340, X1 = 965, Y0 = 40, Y1 = 190;
const max = Math.max(...weeks, 1);
const pts = weeks.map((v, i) => [X0 + (i / (weeks.length - 1)) * (X1 - X0), Y1 - Math.sqrt(v / max) * (Y1 - Y0), v]);
const line = "M" + pts.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" L");
const starPath = (x, y, s) => `M${x} ${y - s} Q${x} ${y} ${x + s} ${y} Q${x} ${y} ${x} ${y + s} Q${x} ${y} ${x - s} ${y} Q${x} ${y} ${x} ${y - s}Z`;
const starsSvg = pts.map(([x, y, v], i) => v
  ? `<path class="st" style="animation-delay:${(0.4 + i * 0.03).toFixed(2)}s, ${(-(i % 7) * 0.4).toFixed(1)}s" d="${starPath(+x.toFixed(1), +y.toFixed(1), +(3 + (v / max) * 7).toFixed(1))}"/>`
  : `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="1.2" fill="#6b5aa6"/>`).join("");

const fmt = (n) => n.toLocaleString("en-US");
const rows = [
  ["contributions this year", fmt(cal.totalContributions)],
  ["current streak", `${current} days`],
  ["longest streak", `${longest} days`],
  ["best day", `${best.contributionCount} on ${best.date.slice(5).replace("-", "/")}`],
  ["prs · commits", `${u.contributionsCollection.totalPullRequestContributions} · ${fmt(u.contributionsCollection.totalCommitContributions)}`],
];
const stats = rows.map(([k, v], i) => `
    <g class="row" style="animation-delay:${(i * 0.12).toFixed(2)}s">
      <text x="32" y="${58 + i * 36}" class="k">${k}</text>
      <text x="300" y="${58 + i * 36}" class="v" text-anchor="end">${v}</text>
    </g>`).join("");

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 240" width="1000" height="240">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1030"/><stop offset=".6" stop-color="#2a1d5c"/><stop offset="1" stop-color="#4a3070"/></linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="c"><rect width="1000" height="240" rx="20"/></clipPath>
  </defs>
  <style>
    text { font-family: 'Hiragino Maru Gothic ProN', 'M PLUS Rounded 1c', 'Nunito', 'Yu Gothic', system-ui, sans-serif; }
    .k { font-size: 14px; fill: #a99bd6; }
    .v { font-size: 18px; font-weight: 800; fill: #ffd1dc; }
    .t { font-size: 12px; fill: #a99bd6; letter-spacing: 2px; }
    .row { opacity: 0; animation: in .5s ease-out forwards; }
    @keyframes in { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; transform: none; } }
    .ln { fill: none; stroke: #c8b6ff; stroke-opacity: .45; stroke-width: 1.2; stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 2.6s ease-out .3s forwards; }
    @keyframes draw { to { stroke-dashoffset: 0; } }
    .st { fill: #fff4d6; opacity: 0; animation: pop .4s ease-out forwards, tw 3s ease-in-out 3s infinite; }
    @keyframes pop { to { opacity: 1; } }
    @keyframes tw { 50% { opacity: .45; } }
  </style>
  <g clip-path="url(#c)">
    <rect width="1000" height="240" fill="url(#sky)"/>
    <circle cx="930" cy="60" r="90" fill="#fff4d6" opacity=".05"/>
    <line x1="322" y1="30" x2="322" y2="210" stroke="#ffb7c5" stroke-opacity=".25" stroke-dasharray="2 6" stroke-linecap="round"/>
    <path class="ln" pathLength="1" d="${line}"/>
    <g filter="url(#glow)">${starsSvg}</g>
    <text x="${X0}" y="222" class="t">52 weeks ago</text>
    <text x="${X1}" y="222" class="t" text-anchor="end">now ☾ best week ${max}</text>
    ${stats}
  </g>
  <rect x="1" y="1" width="998" height="238" rx="19" fill="none" stroke="#ffb7c5" stroke-opacity=".3" stroke-width="1.5"/>
</svg>
`;
writeFileSync(outfile, svg);
console.log(`wrote ${outfile}: ${cal.totalContributions} contributions, streak ${current}/${longest}`);
