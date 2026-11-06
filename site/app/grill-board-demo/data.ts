// Sample content for the demo Grill Board (prototype, S-009).
// Every card is a made-up, non-engineering example (DDR-000V). None of it is the
// owner's real queue, and nothing here is read from or written to any record.

export type Grade = "P1" | "P2" | "P3" | "P4" | "V1" | "V2" | "V3" | "V4";
export type Scale = "Blueprint" | "Landmark" | "Spec" | "Task";
export type Lane = "pending" | "stale";

export interface Topic {
  key: string;
  label: string;
  frame: string;
  goal: string;
}

export interface Option {
  key: string;
  label: string;
  hint: string;
  recommended?: boolean;
}

export interface Card {
  id: string;
  topic: string;
  lane: Lane;
  p: Grade;
  v: Grade;
  scale: Scale;
  kind: string;
  rev: number;
  flag?: "block" | "risk";
  flagText?: string;
  draft?: boolean;
  short: string;
  title: string;
  pWhy: string;
  vWhy: string;
  q: string;
  why: string;
  rec: string;
  /** The record a confirmed answer would be written into on the real board. */
  owner: string;
  concerns: { name: string; note: string }[];
  wiki: string[];
  changes: string;
  impact: string;
  history: string;
  historyCount: string;
  options: Option[];
}

export const TOPICS: Topic[] = [
  {
    key: "reunion",
    label: "Family reunion",
    frame: "where everyone gathers, what they eat, and who keeps the guest list",
    goal: "One July weekend most of the family can reach and afford.",
  },
  {
    key: "bakery",
    label: "Corner bakery",
    frame: "when the shop opens, who works, and what customers are told",
    goal: "Holiday hours the staff can cover and customers can trust.",
  },
  {
    key: "garden",
    label: "Community garden",
    frame: "how the season's money is spent and who tends the beds",
    goal: "A spring budget and a watering rota volunteers keep.",
  },
];

export const CARDS: Card[] = [
  {
    id: "GB-S01",
    topic: "reunion",
    lane: "pending",
    p: "P2",
    v: "V1",
    scale: "Spec",
    kind: "Unblock / direct work",
    rev: 2,
    flag: "block",
    flagText: "Holds up the venue deposit",
    short: "Pick the venue for the July family reunion",
    title: "Pick the venue for the July family reunion (the lakeside hall holds the date until Friday)",
    pWhy: "The lakeside hall holds July 18 only until Friday; after that the weekend opens to other bookings.",
    vWhy: "Food, rooms and travel all wait on where the reunion is.",
    q: "Which venue should host the reunion on July 18: the lakeside hall (fits 80, $900, kitchen on site), Aunt Rosa's farm (free, room for everyone outdoors, no shelter if it rains), or the community center (fits 60, $350, ten minutes from the hotel)?",
    why: "About 70 people said they will come. The venue decides who can travel easily, what the food can be, and how much each household chips in.",
    rec: "Book the lakeside hall: it fits everyone, has a kitchen and a rain plan, and the deposit is refundable until June 1.",
    owner: "Reunion plan · Venue",
    concerns: [
      { name: "Reunion plan · Venue", note: "where the chosen venue, its deposit and its rain plan are written." },
      { name: "Guest list", note: "the 70 people who said yes, with who needs a ride." },
    ],
    wiki: ["Reunion plan", "Guest list", "Budget sheet"],
    changes: "The reunion plan names the venue, its cost and its refund date; the budget sheet gains the deposit.",
    impact: "Food and rooms can be booked next. With the lakeside hall, each household's share is about $25 before food.",
    history: "Revision 2. Revision 1 left out the community center; you asked for a cheaper option near the hotel.",
    historyCount: "1 earlier revision",
    options: [
      { key: "hall", label: "Book the lakeside hall", hint: "$900, fits 80, kitchen and indoor space if it rains.", recommended: true },
      { key: "farm", label: "Use Aunt Rosa's farm", hint: "Free and roomy; needs a rented tent as a rain plan." },
      { key: "center", label: "Book the community center", hint: "$350 and close to the hotel; tight for 70 people." },
    ],
  },
  {
    id: "GB-S02",
    topic: "reunion",
    lane: "pending",
    p: "P3",
    v: "V2",
    scale: "Spec",
    kind: "Explore / settle decisions",
    rev: 1,
    short: "Choose a catering supplier for the reunion lunch",
    title: "Choose a catering supplier for the reunion lunch (three quotes in hand)",
    pWhy: "Caterers want three weeks' notice and the reunion is seven weeks out.",
    vWhy: "Settles the biggest cost after the venue.",
    q: "Which caterer should serve lunch for about 70 people: Rossi's Kitchen ($14 a head, buffet, they bring tables), Green Leaf ($18 a head, plated, strong vegetarian menu), or a family potluck (about $4 a head for shared basics)?",
    why: "Food is the largest cost after the venue, and four guests eat no meat. A buffet keeps the line moving; a potluck saves money but puts the work on a few cooks.",
    rec: "Rossi's Kitchen buffet with two vegetarian trays added; it fits the budget and lets the cooks in the family enjoy the day.",
    owner: "Reunion plan · Food",
    concerns: [
      { name: "Reunion plan · Food", note: "where the caterer, menu and head count are written." },
      { name: "Budget sheet", note: "the per-household share that the food cost changes." },
    ],
    wiki: ["Reunion plan", "Budget sheet"],
    changes: "The reunion plan names the caterer and menu; the budget sheet gains the food line.",
    impact: "The per-household share is known and can go out with the invitations.",
    history: "First time asked.",
    historyCount: "no earlier revisions",
    options: [
      { key: "rossi", label: "Rossi's Kitchen buffet, plus vegetarian trays", hint: "About $1,050 in all; tables included.", recommended: true },
      { key: "greenleaf", label: "Green Leaf, plated", hint: "About $1,260; the most choice for vegetarian guests." },
      { key: "potluck", label: "Family potluck", hint: "About $280; needs a sign-up sheet and a few lead cooks." },
    ],
  },
  {
    id: "GB-S03",
    topic: "reunion",
    lane: "stale",
    p: "P3",
    v: "V3",
    scale: "Task",
    kind: "Review existing work",
    rev: 3,
    short: "Re-answer: who sends the save-the-date cards",
    title: "Re-answer: who sends the save-the-date cards, now that the person you chose has moved abroad",
    pWhy: "Cards should go out six weeks ahead, which is next week.",
    vWhy: "A small job, but it decides who keeps the address list.",
    q: "Your last answer gave the cards to Marcus, but he has moved abroad. Should cousin Dana take over the cards and the address list, or should the save-the-date go out as a group text and email instead?",
    why: "The list grew from 40 to 52 households. Whoever sends the cards also keeps the address list, so this decides who answers “did my invitation get lost?”",
    rec: "Dana takes the cards and the list; she already keeps the family birthday calendar.",
    owner: "Reunion plan · Invitations",
    concerns: [{ name: "Reunion plan · Invitations", note: "who sends the cards and when." }],
    wiki: ["Reunion plan", "Guest list"],
    changes: "The reunion plan names the new sender; the guest list gains its new keeper.",
    impact: "Cards go out next week; one person answers address questions.",
    history: "Revision 3 came back to you because the person named in your answer moved abroad.",
    historyCount: "2 earlier revisions",
    options: [
      { key: "dana", label: "Dana sends the cards and keeps the list", hint: "Printed cards, posted next week.", recommended: true },
      { key: "digital", label: "Send a group text and email instead", hint: "Free and instant; a few older relatives may miss it." },
    ],
  },
  {
    id: "GB-S04",
    topic: "bakery",
    lane: "pending",
    p: "P1",
    v: "V1",
    scale: "Landmark",
    kind: "Unblock / direct work",
    rev: 2,
    flag: "risk",
    flagText: "Conflicts with the window sign",
    short: "Set the bakery's holiday hours for late December",
    title: "Set the bakery's holiday hours for December 20 to January 2",
    pWhy: "The window sign already promises normal hours, and customers plan around it within days.",
    vWhy: "One answer sets two weeks of takings and staff time.",
    q: "What should the bakery's hours be from December 20 to January 2: normal hours except closed on the 25th and the 1st; shorter hours (7 am to 1 pm) for the whole fortnight; or closed December 24 to 26 and normal hours otherwise?",
    why: "Holiday orders are a third of December's takings, but two of the four staff are away the week of the 25th. The sign in the window says “open as usual”, which two of the three choices would contradict.",
    rec: "Shorter hours for the fortnight, and change the window sign today; two people can cover 7 to 1.",
    owner: "Shop handbook · Opening hours",
    concerns: [
      { name: "Shop handbook · Opening hours", note: "the hours staff and customers are told." },
      { name: "Staff rota · December", note: "who is away the week of the 25th." },
    ],
    wiki: ["Shop handbook", "Staff rota"],
    changes: "The shop handbook records the holiday hours; the window sign and the shop's page are updated to match.",
    impact: "Staff know their shifts; customers see one set of hours everywhere.",
    history: "Revision 2. Revision 1 did not mention the window sign; you asked what customers had already been told.",
    historyCount: "1 earlier revision",
    options: [
      { key: "short", label: "Shorter hours, 7 am to 1 pm, all fortnight", hint: "Two staff can cover; the sign changes today.", recommended: true },
      { key: "normal", label: "Normal hours, closed the 25th and the 1st", hint: "Matches the sign; needs a temporary helper." },
      { key: "closed", label: "Closed December 24 to 26, normal otherwise", hint: "A clean break; misses the busiest pickup day." },
    ],
  },
  {
    id: "GB-S05",
    topic: "bakery",
    lane: "pending",
    p: "P2",
    v: "V2",
    scale: "Task",
    kind: "Explore / settle decisions",
    rev: 1,
    short: "Pick who opens the shop on Saturdays in January",
    title: "Pick who opens the shop on Saturdays in January",
    pWhy: "The January rota goes up on December 15.",
    vWhy: "Sets a month of early starts and one person's extra hours.",
    q: "Who should open on Saturdays in January: Priya every week (she asked for more hours), Priya and Tom taking turns, or the owner opening with Priya closing?",
    why: "Opening on Saturday means a 5 am start for the bread. A fixed opener learns the routine; taking turns spreads the early mornings.",
    rec: "Priya and Tom take turns, two Saturdays each, with the owner as backup.",
    owner: "Staff rota · January",
    concerns: [{ name: "Staff rota · January", note: "the Saturday shifts and who covers if someone is ill." }],
    wiki: ["Staff rota"],
    changes: "The January rota names the Saturday openers and the backup.",
    impact: "Everyone knows their Saturdays a month ahead.",
    history: "First time asked.",
    historyCount: "no earlier revisions",
    options: [
      { key: "turns", label: "Priya and Tom take turns", hint: "Two Saturdays each; the owner is backup.", recommended: true },
      { key: "priya", label: "Priya opens every Saturday", hint: "She gets the extra hours she asked for." },
      { key: "owner", label: "The owner opens, Priya closes", hint: "Keeps staff hours the same as December." },
    ],
  },
  {
    id: "GB-S06",
    topic: "bakery",
    lane: "pending",
    p: "P4",
    v: "V3",
    scale: "Task",
    kind: "Review existing work",
    rev: 1,
    draft: true,
    short: "Approve the wording of the holiday notice",
    title: "Approve the wording of the holiday notice for the door and the shop's page",
    pWhy: "Needed only once the holiday hours are settled.",
    vWhy: "A clear note saves a run of “are you open?” calls.",
    q: "Is this the right notice: “We're taking a short break to be with family. Fresh bread is back on the 27th. Thank you for a lovely year!”",
    why: "Customers read the notice more than the hours list. A warm, clear note avoids confusion and keeps regulars ordering ahead.",
    rec: "Approve it with one line added about ordering holiday loaves by the 22nd.",
    owner: "Shop handbook · Notices",
    concerns: [{ name: "Shop handbook · Notices", note: "the wording posted on the door and online." }],
    wiki: ["Shop handbook"],
    changes: "The notice is printed for the door and posted on the shop's page.",
    impact: "Customers see the same message in the shop and online.",
    history: "First time asked.",
    historyCount: "no earlier revisions",
    options: [
      { key: "preorder", label: "Approve, with a line about ordering by the 22nd", hint: "Brings holiday orders in early.", recommended: true },
      { key: "asis", label: "Approve as written", hint: "Short and warm; no ordering reminder." },
    ],
  },
  {
    id: "GB-S07",
    topic: "garden",
    lane: "pending",
    p: "P2",
    v: "V1",
    scale: "Landmark",
    kind: "Explore / settle decisions",
    rev: 1,
    short: "Split the community garden's spring budget",
    title: "Split the community garden's $2,400 spring budget",
    pWhy: "Seed orders close at the end of the month.",
    vWhy: "Decides whether the beds stay watered for years, not just this season.",
    q: "How should the garden's $2,400 for spring be split: most of it on a new water tank ($1,500) with the rest on seeds and tools; evenly across water, soil, seeds and tools; or $800 kept aside for a summer children's workshop?",
    why: "Last summer the beds went dry twice when the town shut the tap off. A tank fixes that for years, but leaves little for the extras that bring in new members.",
    rec: "Buy the tank and keep $300 for seeds; ask the town for workshop money in May.",
    owner: "Garden budget · Spring",
    concerns: [
      { name: "Garden budget · Spring", note: "where each line of the $2,400 is written." },
      { name: "Members' meeting notes", note: "the dry spells last summer and the workshop idea." },
    ],
    wiki: ["Garden budget", "Meeting notes"],
    changes: "The spring budget gains its lines; the tank order goes to the supplier.",
    impact: "The beds have water through the summer; the workshop needs a grant.",
    history: "First time asked.",
    historyCount: "no earlier revisions",
    options: [
      { key: "tank", label: "Water tank first, the rest on seeds and tools", hint: "$1,500 tank, $600 tools, $300 seeds.", recommended: true },
      { key: "even", label: "Split evenly four ways", hint: "$600 each; no tank this year." },
      { key: "workshop", label: "Keep $800 for a children's workshop", hint: "A smaller tank or none; more new members." },
    ],
  },
  {
    id: "GB-S08",
    topic: "garden",
    lane: "pending",
    p: "P3",
    v: "V2",
    scale: "Task",
    kind: "Unblock / direct work",
    rev: 1,
    flag: "risk",
    flagText: "Two volunteers on the same morning",
    short: "Fix the volunteer watering schedule for April",
    title: "Fix the volunteer watering schedule for April",
    pWhy: "Seedlings go in on April 5.",
    vWhy: "A missed watering in the first two weeks can lose a whole bed.",
    q: "Sam and Lee are both down for Tuesday mornings and nobody has Thursdays. Should Sam move to Thursdays, should both keep Tuesdays while the group asks for a new Thursday volunteer, or should watering move to every other day?",
    why: "New seedlings need water every day for two weeks. A gap on Thursdays means one dry day a week at the worst time.",
    rec: "Move Sam to Thursdays; he said either day suits him.",
    owner: "Volunteer schedule · April",
    concerns: [{ name: "Volunteer schedule · April", note: "who waters which mornings." }],
    wiki: ["Volunteer schedule"],
    changes: "The April schedule moves Sam to Thursdays; Lee keeps Tuesdays.",
    impact: "Every morning has one volunteer; nobody waters twice.",
    history: "First time asked.",
    historyCount: "no earlier revisions",
    options: [
      { key: "move", label: "Move Sam to Thursdays", hint: "Every day covered; Sam already agreed.", recommended: true },
      { key: "ask", label: "Keep both on Tuesdays and ask for a new volunteer", hint: "Thursdays stay open until someone signs up." },
      { key: "alternate", label: "Water every other day", hint: "Fewer shifts; risky for new seedlings." },
    ],
  },
];
