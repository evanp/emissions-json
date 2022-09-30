# Emissions.json

A standards for publicly-visible emissions data on a Web site.

## Licence

Apache 2.0

## Document format

### Terminology

- "Actor": a country, state or province, city, or private company
- "Web site": a site on the world wide web

### Domain

The data file should be available at the domain for the main public web site for the actor.

The data file may be available at the "www" hostname for the domain.

### HTTPS

For validation, the data must be available via HTTPS.

### Relative location

The data should be at `/.well-known/emissions.json` in the domain.

Example: the company is "Big Company" and their main Web site is at `bigcompany.lol`.
Their emissions data should be available at `https://bigcompany.lol/.well-known/emissions.json`

### Data format

The file must be JSON.

The file must be UTF-8.

The file must represent a single JSON object with the following properties:

- **name**: Preferred name for the actor
- **type**: Type of actor. One of "country", "adm1" (state or province), "city", "company".
- **identifiers**: an object mapping identifier namespaces to identifiers for this actor.
  namespaces include "UNLOCODE", "ISO 3166", "GCoM", "LEI".
- **emissions**: an object mapping a year to an emissions object. Each year is a 4-digit number.
  The emissions object has the following fields:
  - **scope1**: scope 1 emissions
  - **scope2**: scope 2 emissions
  - **scope3**: scope 3 emissions