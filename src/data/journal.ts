export interface JournalEntry {
  date: string
  title: string
  body: string
  tags: { thumb: 'epmc' | 'sbm' | 'stbf'; label: string }
}

// Newest first. Entries are drawn from the author's own posts on Royal Road.
/** Newest first. The RSS feed (scripts/build-feed.mjs) publishes only the first 20, in this order. */
export const journalEntries: JournalEntry[] = [
  {
    date: 'October 3, 2026',
    title: 'Arc 3 Is Done — A Short Break Before Arc 4',
    body: "Arc 3 of SBM, Duty in Their Absence, has wrapped. My health let me down for a few days, and life took an unexpected turn with some unavoidable matters, so the usual break between arcs came at the right time — though this one is short. Arc 4 starts next week. Whenever I step away I go back and reread what I've written. Sometimes it holds up; most of the time I wince and ask how to do it better. I do think I've improved as a writer, and chapters like 19 and 21 were a blast to write. What did you think of Arc 3, and of SBM so far? I read every comment.",
    tags: { thumb: 'sbm', label: 'SBM' },
  },
  {
    date: 'July 19, 2026',
    title: 'Unauthorised Copies on a Mirror Site',
    body: "I found all three stories copied and hosted in full on Novels2.com without my permission. I don't mind sites that index my work and send readers to the original — that helps people find stories. Hosting a complete copy is something else: it's unauthorised redistribution. If you'd like to support the work, please read it on Royal Road, Scribble Hub, or through Amazon KDP and the stores connected to it, and let other readers and writers know mirror sites like this exist. If you've been through a DMCA or copyright process before, I'd be grateful to hear how it went.",
    tags: { thumb: 'sbm', label: 'SBM · EPMC · STBF' },
  },
  {
    date: 'July 2026',
    title: 'One Month Into the Paperback',
    body: "The June 2026 paperback edition of Summoned by Mistake, I Decided to Learn How to Live has been out for a few weeks now. It's still a limited print run with lighter formatting, and the web novel isn't going anywhere — SBM was written as a web novel first, and it stays that way, paperback or not.",
    tags: { thumb: 'sbm', label: 'SBM' },
  },
  {
    date: 'June 30, 2026',
    title: 'Finishing Act 1 of STBF, and Why I Needed To',
    body: "STBF exists because I needed to answer a question the other two stories couldn't: can I actually finish something? EPMC runs on a light-novel schedule with no end in sight, and SBM is an ongoing web novel by design. So I wrote STBF short and focused on purpose — four acts, one volume, meant to close. Act 1 is done. Act 2 is on hold while I get further into EPMC Vol. 3, which is already deep into its first draft. Taking a break after finishing a chunk of work is basically tradition for me at this point.",
    tags: { thumb: 'stbf', label: 'STBF' },
  },
  {
    date: 'June 21, 2026',
    title: 'SBM Goes to Paperback',
    body: "SBM is now available as a paperback — the June 2026 edition, lightly formatted for print, with a PDF copy included via QR code for anyone who buys it. I wanted to get this out before summer ended. There's something about wanting a book to actually sit on a shelf that made this worth doing.",
    tags: { thumb: 'sbm', label: 'SBM' },
  },
  {
    date: 'June 14, 2026',
    title: 'Three Days of Debugging Later…',
    body: 'Sorry for the missed update — I was buried in getting an email delivery system working so readers can receive a PDF copy of either story. It took a lot longer than planned. Worth it, though. Next chapter is on the way shortly.',
    tags: { thumb: 'sbm', label: 'SBM · EPMC' },
  },
  {
    date: 'June 10, 2026',
    title: 'A Detour for the Community Magazine',
    body: 'Royal Road\'s community magazine was running with the theme "The Person You Pretend to Be," and it hit close enough to home that I couldn\'t not write something for it. That something became STBF — a new, separate story from EPMC and SBM, but built from the same instincts.',
    tags: { thumb: 'stbf', label: 'STBF' },
  },
  {
    date: 'May 2026',
    title: 'EPMC, Volume 2 Done',
    body: "Volume 2 — The Scientist's First Steps Into The World — is finished. This story started as something close to a tribute, shaped by Re:Zero and Mushoku Tensei, but it's become its own thing somewhere along the way, which is a strange and good feeling. Volume 3 is the plan next, likely landing around August or September. I also set up an X account if anyone wants updates between chapters.",
    tags: { thumb: 'epmc', label: 'EPMC' },
  },
  {
    date: 'Spring 2026',
    title: 'Arc 2, and Discovering the Story Alongside You',
    body: "Arc 2 — the bridge between Unwilling Summoning and everything after it — is done. What you're reading is genuinely an unedited first draft; I'm figuring the story out at close to the same pace as everyone reading it, mistakes included. Arc 3 starts with a ruins exploration segment. Free time gets shorter once summer ends, so the schedule may shift, but this story isn't ending abruptly.",
    tags: { thumb: 'sbm', label: 'SBM' },
  },
  {
    date: 'Early 2026',
    title: 'Why SBM Exists',
    body: "EPMC was never built to hold every idea I had, so this became the outlet — something simpler, and honestly more relaxing to write. Publishing into a quiet room with zero comments and zero engagement is hard, and I mean that literally. But one reader followed early on, and that alone was enough to make the whole thing feel worth continuing. The plan is somewhere around 50 chapters, subject to change, and I don't intend to leave it unfinished — even if it takes a while.",
    tags: { thumb: 'sbm', label: 'SBM' },
  },
  {
    date: '2025 – 2026',
    title: 'The Afterword I Never Rewrote',
    body: "EPMC started after a Mushoku Tensei watch session, when a friend flinched at how easily the protagonist was accepted as family despite talent standing in for love. That stuck with me, and it's the seed the whole story grew from — someone ordinary and scarred who still finds a way back to love, written as a kind of tribute after Re:Zero hit every emotional beat I hoped to someday earn myself. I know the early chapters run long and over-explain themselves. I'm working on that. A Kindle edition is still the plan, whenever time allows.",
    tags: { thumb: 'epmc', label: 'EPMC' },
  },
]
