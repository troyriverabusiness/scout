# Scout

AI pipeline for discovering, scoring, and reaching out to early-stage startups. Built as a personal tool for VC sourcing and community outreach — not a demo project.

---

## What it does

Scrapes startup data from YC batches, EU-Startups, ProductHunt, and GitHub trending. Extracts structured profiles from unstructured text using an LLM. Scores each startup against multiple investment thesis vectors using FAISS similarity search. Generates personalized outreach to founders or deal submissions to VC funds. Logs everything to a deal flow database.

The output is a weekly briefing: new startups ranked by thesis fit, with outreach queued automatically for the top matches.

---

## Stack

| Layer | Tools |
|---|---|
| Scraping | Firecrawl, BeautifulSoup |
| Extraction | OpenAI Responses API, Instructor (structured outputs) |
| Embeddings | `multilingual-e5-base` via sentence-transformers |
| Vector search | FAISS (IndexFlatIP, cosine similarity) |
| Storage | Supabase (structured data + object storage) |
| Automation | n8n (self-hosted on AWS EC2) |
| Outreach | Smartlead / Resend |
| Observability | Langfuse (tracing, evals, LLM-as-judge) |
| API | FastAPI |
| Infra | AWS EC2, Docker, Caddy |

---

## How the scoring works

Each startup description is embedded and compared against thesis vectors I defined manually — things like "B2B SaaS for SMEs in DACH", "vertical AI for industrial workflows", "developer tooling". The cosine similarity score tells you how well a startup fits a specific fund's mandate, not just a generic quality score.

This means the same startup gets a different score depending on which fund you're evaluating it for.

---

## Evals

Langfuse tracks every LLM call across the pipeline. Three things are evaluated:

1. **Extraction accuracy** — does the structured output match the source text
2. **Thesis scoring consistency** — does re-running the same startup produce stable scores
3. **Outreach quality** — LLM-as-judge rates whether the generated email is specific, relevant, and not generic

Real reply rates from sent outreach are fed back as ground truth for outreach eval.

---

## What I learned

Building this forced me to go deeper than most embedding tutorials. Multilingual retrieval across DE/EN startup descriptions without translation, getting structured JSON out of messy scraped text reliably, and building an eval framework that catches regressions when I change a prompt — none of that is obvious from documentation alone.

The Langfuse integration specifically changed how I think about LLM pipelines. Having traces, costs, and scores in one place makes it possible to improve systematically rather than by gut feel.

The project also taught me that the hardest part of an AI pipeline is usually the data layer, not the model.

---

## Status

Running weekly for personal use. Powers deal flow tracking for Blau Tech (Munich, 1000+ members) and VC scout outreach.

---

## Contact

Troy — [Blau Tech](https://blautech.de) · [LinkedIn](https://linkedin.com/in/yourhandle)