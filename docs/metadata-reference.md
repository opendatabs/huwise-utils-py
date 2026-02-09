# Metadata Reference

Valid values and reference information for domain-specific metadata fields.

!!! warning "Domain-Specific Values"
    The values listed on this page apply to the **data.bs.ch** domain. Other Huwise domains may have different values. Use the Automation API's metadata template endpoints to discover valid values for your domain:

    ```
    GET /api/automation/v1.0/datasets/{uid}/metadata/{template_name}/{field_name}/
    ```

    See the [Huwise Automation API docs](https://help.opendatasoft.com/apis/ods-automation-v1/#tag/Dataset-metadata) for details.

## DCAT-AP-CH License

Field: `dcat_ap_ch.license`

These codes follow the [opendata.swiss](https://opendata.swiss) standard for Swiss open data licensing.

| Code | Description |
|------|-------------|
| `terms_open` | Open use. |
| `terms_by` | Open use. Must provide the source. |
| `terms_by_ask` | Open use. Must provide the source. Use for commercial purposes requires permission of the data owner. |
| `terms_ask` | Open use. Use for commercial purposes requires permission of the data owner. |

## DCAT-AP-CH Rights

Field: `dcat_ap_ch.rights`

These rights statements follow the [opendata.swiss](https://opendata.swiss) standard. They describe which types of use are allowed and whether attribution is required.

| Code | Description |
|------|-------------|
| `NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired` | Non-commercial and commercial use allowed, no attribution required |
| `NonCommercialAllowed-CommercialAllowed-ReferenceRequired` | Non-commercial and commercial use allowed, attribution required |
| `NonCommercialAllowed-CommercialWithPermission-ReferenceNotRequired` | Non-commercial use allowed, commercial use requires permission, no attribution required |
| `NonCommercialAllowed-CommercialWithPermission-ReferenceRequired` | Non-commercial use allowed, commercial use requires permission, attribution required |
| `NonCommercialAllowed-CommercialNotAllowed-ReferenceNotRequired` | Non-commercial use allowed, commercial use not allowed, no attribution required |
| `NonCommercialAllowed-CommercialNotAllowed-ReferenceRequired` | Non-commercial use allowed, commercial use not allowed, attribution required |
| `NonCommercialNotAllowed-CommercialNotAllowed-ReferenceNotRequired` | Neither non-commercial nor commercial use allowed, no attribution required |
| `NonCommercialNotAllowed-CommercialNotAllowed-ReferenceRequired` | Neither non-commercial nor commercial use allowed, attribution required |
| `NonCommercialNotAllowed-CommercialAllowed-ReferenceNotRequired` | Non-commercial use not allowed, commercial use allowed, no attribution required |
| `NonCommercialNotAllowed-CommercialAllowed-ReferenceRequired` | Non-commercial use not allowed, commercial use allowed, attribution required |
| `NonCommercialNotAllowed-CommercialWithPermission-ReferenceNotRequired` | Non-commercial use not allowed, commercial use requires permission, no attribution required |
| `NonCommercialNotAllowed-CommercialWithPermission-ReferenceRequired` | Non-commercial use not allowed, commercial use requires permission, attribution required |

## Theme IDs

Field: `internal.theme_id`

!!! warning "Domain-Specific"
    Theme IDs are **platform-internal hashes** that are unique to each Huwise domain. The mapping below is only valid for `data.bs.ch`. Other domains will have completely different theme hash IDs.

### Discovering Themes for Your Domain

The repository includes a discovery script that pairs hash IDs with human-readable
names by cross-referencing the Automation API and the Explore API.

If your `.env` file contains `HUWISE_API_KEY` and `HUWISE_DOMAIN`, you can run it
without arguments:

```bash
uv run python scripts/discover_themes.py
```

Or pass the values explicitly:

```bash
uv run python scripts/discover_themes.py --domain your-domain.huwise.com --api-key YOUR_KEY
```

Add `--json` to get the output as JSON instead of a Python dict.

### Theme Mapping for `data.bs.ch`

The following mapping covers all 25 theme IDs found on `data.bs.ch`, resolved by
cross-referencing the Automation API, the Explore API, and the internal dataset
catalog (dataset `100055`).

| Theme ID | Theme Name |
|----------|------------|
| `20bb143` | Arbeit, Erwerb |
| `c813f26` | Bau- und Wohnungswesen |
| `3606293` | Bevölkerung |
| `c9a169b` | Bildung, Wissenschaft |
| `06af88d` | Energie |
| `b8b874a` | Finanzen |
| `cc7ea4s` | Gebäude |
| `7542721` | Geographie |
| `6173474` | Gesetzgebung |
| `e2e248a` | Gesundheit |
| `d847e7c` | Handel |
| `da0ff7d` | Industrie, Dienstleistungen |
| `ae41f5e` | Kriminalität, Strafrecht |
| `e9dc0c8` | Kultur, Medien, Informationsgesellschaft, Sport |
| `59506c3` | Land- und Forstwirtschaft |
| `3d7f80f` | Mobilität und Verkehr |
| `9b815ca` | Politik |
| `338b3e5` | Preise |
| `186e3a8` | Raum und Umwelt |
| `6e0eacc` | Soziale Sicherheit |
| `ca365da` | Statistische Grundlagen |
| `0a7844c` | Tourismus |
| `7b5b405` | Verwaltung |
| `0774467` | Volkswirtschaft |
| `60c7454` | Öffentliche Ordnung und Sicherheit |



## License IDs (`LICENSE_MAP`)

Field: `internal.license_id`

!!! warning "Domain-Specific"
    The `LICENSE_MAP` constant in the library is specific to **data.bs.ch**. Other domains will have different license IDs. Use the Automation API to discover available license IDs for your domain:

    ```
    GET /api/automation/v1.0/metadata_templates/internal/fields/license_id/suggest/
    ```

The following license mappings are known for `data.bs.ch`:

| License ID | License URL | Description |
|------------|-------------|-------------|
| `4bj8ceb` | <https://creativecommons.org/publicdomain/zero/1.0/> | CC0 1.0 |
| `cc_by` | <https://creativecommons.org/licenses/by/3.0/ch/> | CC BY 3.0 CH |
| `5sylls5` | <https://creativecommons.org/licenses/by/4.0/> | CC BY 4.0 |
| `t2kf10u` | See dataset | CC BY 3.0 CH + OpenStreetMap |
| `353v4r` | See dataset | CC BY 4.0 + OpenStreetMap |
| `vzo5u7j` | <https://www.gnu.org/licenses/gpl-3.0> | GNU GPL 3 |
| `r617wgj` | See dataset | Nutzungsbedingungen Geodaten Kanton BS |
| `ce0mv1b` | <https://opendata.swiss/de/terms-of-use/> | Open use with source attribution, commercial use requires permission |

## Geographic Reference Codes

Field: `default.geographic_reference`

Geographic reference codes follow the format `{country_iso}_{admin_level}_{territory_id}`.

### Format

```
{country}_{admin_level}_{territory_id}
```

- **Country**: ISO country code in lowercase (e.g. `ch` for Switzerland)
- **Admin level**: A two-digit number representing the administrative level
- **Territory ID**: Numeric identifier of the specific territory

### Example

`ch_40_12` means:

- `ch` = Switzerland
- `40` = Kanton (canton) level
- `12` = Territory ID 12 (Basel-Stadt)

### Admin Levels for Switzerland

The admin level digits are inspired by OpenStreetMap administrative levels. Smaller numbers represent larger administrative areas; larger numbers represent finer granularity.

| Admin Level | Description | Example |
|-------------|-------------|---------|
| `40` | Kanton (Canton) | `ch_40_12` (Basel-Stadt) |
| `60` | Bezirk (District) | `ch_60_1301` |
| `80` | Gemeinde (Municipality) | `ch_80_2701` (Basel) |
| `81` | Postal codes (4-digit) | `ch_81_4001` |
| `82` | Postal codes (6-digit) | `ch_82_400101` |

!!! note "Country-Specific"
    Admin level meanings vary by country -- these are an internal Huwise convention inspired by OpenStreetMap levels. The specific meanings of admin levels for countries other than Switzerland may differ.

### Looking Up Territory IDs

Territory IDs can be looked up in the Huwise Hub reference datasets:

- **Swiss municipalities**: <https://hub.huwise.com/explore/assets/georef-switzerland-gemeinde/>
- **Swiss cantons**: <https://hub.huwise.com/explore/assets/georef-switzerland-kanton/>

### Programmatic Discovery

Use the Automation API's field suggest endpoint to discover valid geographic reference codes:

```
GET /api/automation/v1.0/metadata_templates/default/fields/geographic_reference/suggest/?q=ch
```

For more details, see the [Huwise community article on territory codes](https://community.huwise.com/organize-data-68/mapping-of-territory-codes-681).
