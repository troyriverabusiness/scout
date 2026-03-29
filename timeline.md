# Scout — Build Roadmap

AI pipeline for discovering, scoring, and reaching out to early-stage startups.
Built across 4 weeks, designed to be a live tool from day one.

---

## Status

- [x] Week 1 — Data pipeline
- [ ] Week 2 — Scoring engine
- [ ] Week 3 — Outreach automation
- [ ] Week 4 — Evals and observability
- [ ] Later — Production features

---

## Week 1 — Data pipeline

Goal: clean structured startup profiles in Supabase, extraction traced in Langfuse.

### Day 1 — Setup

- [ ] Create Supabase project, add `startups` table with all columns
- [ ] Create Langfuse account, grab API keys
- [ ] Set up project with `uv`, install deps: `firecrawl-py openai instructor langfuse supabase fastapi sentence-transformers faiss-cpu`
- [ ] Add `.env` file: `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `FIRECRAWL_API_KEY`

```sql
create table startups (
  id uuid primary key default gen_random_uuid(),
  name text,
  location text,
  founded text,
  sector text,
  stage text,
  one_liner text,
  description text,
  founders jsonb,
  traction_signals jsonb,
  tags jsonb,
  website text,
  source_url text unique,
  fingerprint text unique,
  thesis_score float,
  fund_scores jsonb,
  best_fund_match text,
  created_at timestamp default now()
);
```

### Day 2 — Scraping

- [ ] Scrape YC W25 batch directory — single page, get all company slugs
- [ ] Scrape individual YC company pages for richer text
- [ ] Add deduplication check before every Firecrawl call — check `source_url` in Supabase first
- [ ] Add content fingerprint using `hashlib.md5(name + one_liner)` to catch same company from multiple sources
- [ ] Target: 50+ raw markdown texts ready for extraction

Sources to start with:
- `ycombinator.com/companies?batch=W25` — primary source, clean and structured
- `munich-startup.de/en/startups/` — DACH-focused, directly relevant to Munich VC mandate
- Add more sources later once pipeline is proven

### Day 3 — Extraction with Instructor

- [ ] Define `StartupProfile` Pydantic model: `name`, `location`, `sector`, `stage`, `one_liner`, `description`, `founders`, `traction_signals`, `tags`, `website`
- [ ] Set up Instructor wrapping the OpenAI client — `instructor.from_openai(OpenAI())`
- [ ] Write extraction function using `gpt-4o-mini` — cheap enough to run at volume
- [ ] Cap input at 4000 tokens per scrape — beyond that is usually boilerplate
- [ ] Handle extraction failures gracefully — return `None`, log, continue

### Day 4 — Langfuse tracing

- [ ] Wrap extraction function with `@observe()` decorator
- [ ] Add `extraction_success` score: 1 if profile returned, 0 if failed
- [ ] Add `completeness` score: ratio of non-null fields populated (0.0–1.0)
- [ ] Open Langfuse dashboard, review first 20 traces manually

### Day 5 — LLM-as-judge eval

- [ ] Write `judge_extraction()` function — second LLM call scoring faithfulness to source text
- [ ] Score from 0.0 to 1.0: accurate extraction vs hallucinated fields
- [ ] Attach score to trace with `langfuse_context.score_current_trace(name="extraction_quality", value=...)`
- [ ] Run on 20 startups, establish baseline extraction quality score

### Day 6–7 — Bulk run and cleanup

- [ ] Run full pipeline across all collected URLs
- [ ] Fix edge cases found during eval — missing fields, wrong sector classifications
- [ ] Eyeball 20 rows in Supabase, confirm data quality looks right
- [ ] Write a short note of what broke and how you fixed it

**End of Week 1:** 100+ startups in Supabase, Langfuse showing extraction success rate and quality scores across all traces.

---

## Week 2 — Scoring engine

Goal: every startup scored against fund-specific thesis vectors. Deal flow view in Supabase.

### Day 1 — Thesis vectors

- [ ] Write thesis descriptions for 4 Munich-relevant funds as natural language strings
  - UVC Partners — B2B SaaS, DACH, seed to Series A
  - Unternehmertum Venture Capital — deep tech, TUM spin-offs, hardware, industrial AI
  - Bayern Kapital — Bavarian startups, seed, life sciences, software, clean tech
  - Speedinvest — pan-European, pre-seed, fintech, marketplace, AI
- [ ] Be specific — vague thesis vectors produce noisy scores. Include geography, stage, sector, and check size where known.

### Day 2 — FAISS index

- [ ] Install `sentence-transformers` and `faiss-cpu`
- [ ] Load `intfloat/multilingual-e5-base` — cross-lingual, handles German startup descriptions
- [ ] Embed thesis vectors with `"query: "` prefix (e5 model requirement)
- [ ] Build `IndexFlatIP` — exact cosine similarity, right choice for <1000 vectors
- [ ] Save index to disk with `faiss.write_index()` so you don't rebuild on every run
- [ ] Save fund name mapping alongside index as a `.pkl` file

### Day 3 — Startup scoring

- [ ] Write `score_startup()` function — embed `one_liner + description + tags` with `"passage: "` prefix
- [ ] Search against thesis index, return dict of `{fund_name: score}` for all funds
- [ ] Scores are cosine similarity 0.0–1.0. Anything above 0.75 is a strong match.
- [ ] Run batch scoring across all startups currently in Supabase
- [ ] Store `thesis_score` (best score), `fund_scores` (full breakdown), `best_fund_match` (fund name) per startup

### Day 4 — Live scoring on ingest

- [ ] Add scoring step directly into `scrape_and_extract()` pipeline
- [ ] Every new startup gets scored at ingest time, not as a separate batch job
- [ ] Log `thesis_fit` score to Langfuse trace — now you can correlate source quality with thesis fit
- [ ] Add threshold filter: only log a Langfuse score if thesis fit > 0.6 to reduce noise

### Day 5 — Tune thresholds

- [ ] Query Supabase: `select name, sector, best_fund_match, thesis_score order by thesis_score desc`
- [ ] Review top 20 and bottom 20 — do the high scorers actually match the thesis?
- [ ] Adjust thesis vector text if wrong sectors are scoring too high
- [ ] Settle on a threshold (likely 0.72–0.80) above which a startup enters your active deal flow

### Day 6–7 — FastAPI endpoint

- [ ] Create `/score` endpoint — accepts a URL, runs full scrape → extract → score pipeline on demand
- [ ] Create `/startups` endpoint — returns ranked startups filtered by fund and minimum score
- [ ] Create `/startups/{id}` endpoint — returns full profile including fund score breakdown
- [ ] Run locally with `uvicorn`, confirm endpoints return correct data

**End of Week 2:** Every startup has a per-fund thesis score. You can query "top 10 startups for Unternehmertum this week" and get a meaningful ranked list.

---

## Week 3 — Outreach automation

Goal: personalized outreach emails drafted and queued automatically for high-scoring startups.

### Day 1 — Outreach generator

- [ ] Write `generate_outreach()` function — takes startup profile + target (founder or VC fund) and returns a personalized email draft
- [ ] Prompt must inject: founder name, company name, one-liner, specific signal from traction or description, and your context (Blau Tech community, 1000+ members, Munich)
- [ ] Two templates: one for founder outreach (Blau Tech partnership), one for VC deal submission (Scout sourcing)
- [ ] Test on 10 startups manually — check that emails sound human, not templated

### Day 2 — Outreach quality eval

- [ ] Add LLM-as-judge for outreach: score whether the email is specific, relevant, and not generic
- [ ] Score on three dimensions: specificity (0–1), relevance (0–1), tone (0–1)
- [ ] Log all three to Langfuse as separate scores on the outreach trace
- [ ] Review lowest-scoring emails — usually where the profile was incomplete, fix at extraction layer

### Day 3 — n8n workflow

- [ ] Build n8n workflow: trigger on new Supabase row where `thesis_score > 0.75` and `outreach_sent = false`
- [ ] Workflow: fetch startup profile → call `/generate_outreach` FastAPI endpoint → write draft to Supabase `outreach_drafts` table
- [ ] Add manual review step before anything is sent — you read the draft first
- [ ] Add `outreach_status` column to startups table: `draft`, `approved`, `sent`, `replied`

```sql
create table outreach_drafts (
  id uuid primary key default gen_random_uuid(),
  startup_id uuid references startups(id),
  target text,
  subject text,
  body text,
  status text default 'draft',
  reply_received boolean default false,
  created_at timestamp default now()
);
```

### Day 4 — Send real outreach

- [ ] Connect Resend or Smartlead to n8n for sending approved drafts
- [ ] Send first 10 real outreach emails to founders for Blau Tech partnership
- [ ] Track opens and replies manually at first — you don't need a full CRM yet
- [ ] Every reply is ground truth for your outreach quality eval — log it back to Langfuse

### Day 5–7 — Iteration

- [ ] Review reply rates from first batch
- [ ] Identify which startup profiles produced the best and worst emails
- [ ] Trace back to extraction quality — bad outreach usually means incomplete profile
- [ ] Adjust outreach prompt based on what is and isn't getting responses

**End of Week 3:** Automated pipeline from URL → scored startup → drafted outreach. You have sent real emails and have initial reply rate data as ground truth.

---

## Week 4 — Evals and observability

Goal: measurable eval metrics across the full pipeline. Langfuse dashboard tells you when something regresses.

### Day 1 — Langfuse dataset

- [ ] Upload all extracted startups as a Langfuse dataset — these become your benchmark
- [ ] Each dataset item: input = source URL, expected output = verified profile fields
- [ ] Manually verify ground truth for 20 items — check the YC page yourself and confirm what was extracted

### Day 2 — Experiment tracking

- [ ] Name your current extraction prompt `extraction-v1` in Langfuse Prompts
- [ ] Write an improved version `extraction-v2` — try adding few-shot examples
- [ ] Run both versions against the dataset
- [ ] Compare `extraction_quality` scores between v1 and v2 in the dashboard
- [ ] Keep the version with higher average score

### Day 3 — Pipeline health metrics

- [ ] Define the metrics you care about and where acceptable thresholds are:
  - Extraction success rate > 90%
  - Completeness score > 0.75
  - Extraction quality (LLM-judge) > 0.80
  - Thesis scoring latency < 2 seconds
  - Outreach quality score > 0.70
- [ ] Add Langfuse alerts if scores drop below threshold on a new batch run

### Day 4 — Weekly briefing

- [ ] Write a script that queries Supabase for new startups added in the last 7 days, sorted by thesis score
- [ ] Format as a simple markdown or HTML digest
- [ ] Send to yourself via Resend every Monday morning via n8n schedule trigger
- [ ] This is the artifact that makes Scout feel like a real tool, not a project

### Day 5–7 — README and write-up

- [ ] Update README with actual benchmark numbers from Langfuse
- [ ] Write a short LinkedIn post: what you built, what you learned, one surprising finding
- [ ] Record a 2-minute Loom demo: pipeline running, Langfuse dashboard, Supabase deal flow view
- [ ] Push to GitHub, link in your portfolio

**End of Week 4:** Full observable pipeline with benchmark metrics. Live weekly briefing running. Portfolio-ready with real numbers.

---

## Later — when it is running in production

These are features to add once the core pipeline is stable and you have real data flowing through it. No order — add whatever is most useful at the time.

### Scoring improvements

- [ ] UMAP visualization — project all startup embeddings into 2D, see how they cluster by sector and geography. Reveals blind spots in your sourcing.
- [ ] Fine-tune scoring on labeled data — after manually reviewing 100+ startups, train a classifier on your own accept/reject decisions
- [ ] Competitor clustering — find startups that are semantically similar to each other. Useful for market maps.
- [ ] Signal weighting — weight traction signals higher than description text in the embedding. A startup with revenue mentioned should score differently to one without.

### Sourcing improvements

- [ ] Sifted scraper — European tech focus, good Series A coverage
- [ ] Tech.eu weekly funding roundups — scrape the weekly digest, extract all mentioned startups at once
- [ ] GitHub trending — catch dev tools and open-source startups before they raise
- [ ] Twitter/X lists — monitor VC partner accounts for portfolio announcements
- [ ] LinkedIn company search — filtered by founded date and location, requires proxies or manual export

### Outreach improvements

- [ ] Reply rate tracking — connect inbox to n8n, auto-update `outreach_status` when a reply arrives
- [ ] Follow-up sequences — if no reply in 5 days, send a shorter follow-up
- [ ] Personalization signals — pull founder's latest LinkedIn post or tweet as a personalization hook
- [ ] A/B testing — send two subject line variants to similar startups, track which gets more opens

### Deal flow features

- [ ] Per-fund deal submission formatter — each fund has a specific format they prefer for warm intros
- [ ] Weekly digest per fund — "here are 5 startups that fit your thesis this week" sent to fund partners
- [ ] Status tracking — move startups through stages: sourced → reviewed → contacted → meeting → passed
- [ ] Investor fit matrix — for a given startup, rank all funds by thesis fit score

### Infrastructure

- [ ] Semantic cache — cache LLM responses by input embedding similarity. If two very similar startup texts have been extracted before, return the cached result instead of calling the LLM again. Reduces cost at scale.
- [ ] Async pipeline — use `asyncio` to run multiple scrape + extract jobs in parallel instead of sequentially. 10x speed improvement.
- [ ] n8n schedule — run full pipeline automatically every Monday morning, not manually
- [ ] Monitoring alerts — Slack notification if extraction success rate drops below 85% on any batch run

---

## Stack reference

| Layer | Tool | Purpose |
|---|---|---|
| Scraping | Firecrawl | Clean markdown from any URL |
| Extraction | OpenAI gpt-4o-mini + Instructor | Structured startup profiles |
| Embeddings | multilingual-e5-base | Cross-lingual semantic vectors |
| Vector search | FAISS IndexFlatIP | Thesis similarity scoring |
| Storage | Supabase | Startup profiles and deal flow |
| Automation | n8n self-hosted | Scrape triggers and outreach sequences |
| Outreach | Resend / Smartlead | Email sending |
| Observability | Langfuse | Traces, scores, evals, prompt versioning |
| API | FastAPI | Score and query endpoints |
| Infra | AWS EC2 + Docker + Caddy | Self-hosted backend |

---

## Key thresholds to tune

| Metric | Starting value | What it controls |
|---|---|---|
| Thesis fit score | > 0.75 | Enters active deal flow |
| Extraction quality | > 0.80 | Trusted enough to use for outreach |
| Completeness score | > 0.70 | Enough fields to generate good email |
| Outreach quality | > 0.70 | Approved for sending queue |