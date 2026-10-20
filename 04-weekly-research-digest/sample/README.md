# Sample data

- `crossref-results-2026-10-20.csv`: a trimmed copy of a real response from the public Crossref REST API, retrieved on 20 October 2026 with the same query the blueprint uses (`query.bibliographic=islamic finance sukuk green sukuk`, publication dates 13 to 20 October 2026, types journal-article, posted-content and book-chapter, 20 rows). Titles, journals, DOIs, first-author family names and dates are bibliographic metadata as Crossref returned them. Abstracts are cut to the first 300 characters for testing only; read the full paper at its DOI.
- `sent-dois-log.csv`: an example of the `Sent_DOIs` tab. The `seed` row keeps the first run working. The second row shows a DOI logged by an earlier test run, which the next run will skip.

Inclusion here says nothing about the quality of a paper. It only shows what Crossref returned for the search.
