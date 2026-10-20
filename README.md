# AI automation demos

Small, working automations for the jobs that eat a small team's week. One problem per demo. Each one comes with an importable Make.com blueprint, fictional sample data, a diagram and a short walkthrough, so you can see exactly how it works and run it yourself.

Demos 01 to 08 are sample scenarios: the organisations are fictional and every file uses made-up data. Each blueprint is drafted and documented but has not yet been test-run in Make, and each README says what to check after import. New demos are added regularly.

## The series

| # | Demo | Problem it solves | Built for | Status |
|---|---|---|---|---|
| 00 | [Webinar sign-up and reminders](https://github.com/NimotallahiDurojaiye/webinar-reminder-automation) | Sign-ups forget the session and lose the link | Communities, trainers | Live, in use |
| 01 | [AI enquiry sorter](01-ai-enquiry-sorter/) | An online school gets about 200 contact-form messages a week, and they all land in one inbox | Schools, NGOs and small firms with one shared contact inbox | Sample scenario (AI) |
| 02 | [Fair CV shortlister](02-fair-cv-shortlister/) | A 40-person logistics firm hiring an Operations Coordinator receives 300 applications and has no time to read them all with care | HR teams, recruiters and small firms hiring without an HR department | Sample scenario (AI) |
| 03 | [Meeting notes to action list](03-meeting-notes-to-actions/) | A small team's weekly call produces rough notes or a transcript, and then nobody turns them into a list | Small NGOs and any team that runs a weekly call | Sample scenario (AI) |
| 04 | [Weekly research digest](04-weekly-research-digest/) | New papers on Islamic finance and sustainable finance appear across dozens of journals and preprint servers every week | Researchers, policy teams and PhD students who follow a fast-moving field | Sample scenario (AI) |
| 05 | [Shariah screening alert](05-shariah-screening-alert/) | A volunteer works out the AAOIFI ratios for every share on the club's watchlist by hand each month | Islamic investment clubs, Muslim investors and analysts who track a share watchlist | Sample scenario (AI) |
| 06 | [Receipt and invoice reader](06-receipt-reader/) | A small catering business photographs every supplier receipt and types it into a spreadsheet by hand | Small businesses, caterers and NGOs that log receipts in a spreadsheet | Sample scenario (AI) |
| 07 | [Donation thank-you and receipts](07-donation-thank-you/) | Donors to a small Muslim charity wait days for a thank-you and a receipt while a volunteer copies each gift into a spreadsheet by hand | Charities, mosques, schools | Sample scenario (No AI) |
| 08 | [Survey feedback analyser](08-survey-feedback-analyser/) | A teacher training academy collects 30 to 40 feedback forms a month, but nobody has time to read the open answers | Trainers, schools, HR | Sample scenario (AI) |

## How every demo is built

- **A human stays in charge.** AI sorts, drafts and summarises. A person approves anything that goes out or decides about someone.
- **Numbers come from code, not from AI.** Where a demo calculates something, such as a screening ratio, the formula does the maths and AI only explains the result.
- **No real personal data.** Every sample file is fictional.
- **Cheap to run.** Each demo states its Make.com operations and AI cost per run.

## Folder layout

```
NN-demo-name/
  README.md          problem, flow, setup, cost, limits
  blueprint.json     import into Make.com
  sample/            fictional input data
  docs/              diagram and screenshots
```

## Author

**Nimotallahi Abiodun Durojaiye** · business operations automation and AI for small organisations
[Portfolio](https://magenta-cactus-05d764.netlify.app) · [LinkedIn](https://www.linkedin.com/in/nimotallahi)

MIT licence.
