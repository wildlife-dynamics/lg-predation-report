"""
Generate the LG Predation Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: lg_predation_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "lg_predation_report_technical_guide.pdf"

# ── Colour palette ────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=24, leading=30, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=12, leading=16, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=14, leading=18, textColor=GREEN_DARK,
                  spaceBefore=16, spaceAfter=5, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=11, leading=15, textColor=GREEN_MID,
                  spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=9.5, leading=13, textColor=SLATE,
                  spaceBefore=7, spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=13, textColor=SLATE,
                  spaceAfter=2, leftIndent=14, firstLineIndent=-10)
CELL     = _style("Cell", fontSize=8.5, leading=12, textColor=SLATE,
                  spaceAfter=0, spaceBefore=0)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):       return Paragraph(text, style)
def h1(text):                  return Paragraph(text, H1)
def h2(text):                  return Paragraph(text, H2)
def h3(text):                  return Paragraph(text, H3)
def sp(n=6):                   return Spacer(1, n)
def bullet(text):              return Paragraph(f"• {text}", BULLET)
def note(text):                return Paragraph(f"<b>Note:</b> {text}", NOTE)
def c(text):                   return Paragraph(text, CELL)


def make_table(data, col_widths):
    """Build a table where every cell value is already a Paragraph (use c())."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  GREEN_DARK),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",           (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "LG Predation Report — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="LG Predation Report — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("Lion Guardians Predation Report", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Livestock Predation Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"), hr(),
        p(
            "The <b>LG Predation Report</b> workflow analyses livestock depredation "
            "incidents recorded by <b>Lion Guardians</b> field teams in the Amboseli "
            "ecosystem. It ingests a local tabular predation CSV file, cleans and "
            "normalises the data, and produces a comprehensive set of maps, charts, "
            "summary tables, a Word report, and an interactive dashboard."
        ),
        p(
            "The workflow produces two spatial maps (livestock predation points and a "
            "predation density grid), eight charts (pie charts, heatmaps, multi-bar and "
            "multi-line time series), and four summary CSV tables per group. "
            "A Word report is assembled from a cover page and a per-period section."
        ),
        note(
            "All per-group outputs are produced by iterating over a user-chosen "
            "grouper: <b>Livestock Species</b> (<code>species_killed</code>) or "
            "<b>Ranch</b> (<code>ranch</code>). Groupers may be left blank to produce "
            "a single combined view."
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 Input Data Source"),
        p(
            "Unlike EarthRanger-connected workflows, the predation report ingests a "
            "<b>local tabular file</b> uploaded by the user at run time via "
            "<code>load_local_tabular_file</code>. The file must use "
            "<code>latin-1</code> encoding and contain the raw field-data columns "
            "exported from the Lion Guardians predation form. GPS coordinates must be "
            "present as UTM Easting and Northing in <b>UTM Zone 37S (EPSG:32737)</b> "
            "under the columns <code>GPS X (UTM)</code> and <code>GPS Y (UTM)</code>."
        ),

        sp(4), h2("2.2 Groupers"),
        p(
            "Two grouper fields are available via <code>set_groupers</code>. "
            "The RJSF form labels these with user-friendly names:"
        ),
        make_table(
            [
                [c("Grouper field"),   c("Form label"),      c("Typical use")],
                [c("species_killed"),  c("Livestock Species"), c("One output per livestock species killed")],
                [c("ranch"),           c("Ranch"),            c("One output per group ranch")],
            ],
            [3.8*cm, 4.2*cm, 8.5*cm],
        ),

        sp(6), h2("2.3 Static Geodata Files"),
        p("Three boundary datasets are downloaded from Dropbox and cached locally:"),
        make_table(
            [
                [c("Dataset"),                c("File"),                           c("Purpose")],
                [c("Group Ranch Boundaries"),  c("lg_group_ranch_boundaries.gpkg"),  c("Community ranch polygons in Amboseli")],
                [c("Conflict Hotspot Areas"),  c("lg_conflict_hotspots.gpkg"),       c("Known human–lion conflict hotspot features")],
                [c("Protected Areas"),         c("lg_protected_areas.gpkg"),         c("National parks and reserves")],
            ],
            [4*cm, 5.2*cm, 7.3*cm],
        ),
        sp(4),
        p(
            "All three files use <code>overwrite_existing: false</code> (3 retries, "
            "no unzip). After loading, each is reprojected to <b>EPSG:4326</b> and "
            "annotated with its geometry type before layer creation."
        ),

        sp(4), h2("2.4 Word Document Templates"),
        make_table(
            [
                [c("Template file"),             c("Purpose")],
                [c("predation_cover_page.docx"), c("Report cover page — period, preparer")],
                [c("custom_patrol_template.docx"), c("Main report section — maps, charts, and summary tables")],
            ],
            [5.5*cm, 11*cm],
        ),
        sp(4),
        p(
            "Both templates are downloaded from Dropbox at run time with "
            "<code>overwrite_existing: false</code> and 3 retries."
        ),

        sp(6), h2("2.5 Base Map Tile Layers"),
        make_table(
            [
                [c("Layer"),                   c("Opacity"), c("Max zoom")],
                [c("ArcGIS World Hillshade"),   c("100 %"),   c("20")],
                [c("ArcGIS World Street Map"),  c("15 %"),    c("20")],
            ],
            [10*cm, 2.5*cm, 4*cm],
        ),
        sp(4),
        p(
            "The hillshade provides full-opacity terrain context. "
            "The street map is overlaid at 15 % to show roads and settlement names "
            "without obscuring predation point data."
        ),
    ]

    # ── 3. Data Ingestion Pipeline ────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Column Mapping"),
        p(
            "<code>map_columns</code> renames raw form field headers to clean "
            "snake_case equivalents and drops reporting columns not needed for analysis. "
            "Dropped columns:"
        ),
        bullet("Month, Year — superseded by the parsed <code>date</code> column"),
        bullet("Verified by Biologist, General Comments, Observations — narrative fields"),
        bullet("Unknown / Other, Specific Area — low-signal or redundant fields"),
        p("Renamed columns:"),
        make_table(
            [
                [c("Original column"),                                        c("Renamed to")],
                [c("FID"),                                                    c("id")],
                [c("Date today (MM/DD/YYYY)"),                                c("date")],
                [c("Species killed"),                                         c("species_killed")],
                [c("total killed"),                                           c("total_killed")],
                [c("Species Injured"),                                        c("species_injured")],
                [c("total injured"),                                          c("total_injured")],
                [c("Was the prey livestock (Yes/No)"),                        c("is_livestock")],
                [c("Depredation from Boma or Bush?"),                         c("boma_or_bush")],
                [c("If bush, were livestock lost?"),                          c("livestock_lost_in_bush")],
                [c("If bush &amp; not lost, were livestock with herder?"),     c("livestock_not_lost_in_bush_herder_present")],
                [c("Group Ranch (MGR, EGR, OGR, Other, Unknown)"),            c("ranch")],
                [c("Community hunt"),                                         c("community_hunt")],
                [c("Mock hunt"),                                              c("mock_hunt")],
                [c("Scared by herders- not with spears"),                     c("scared_by_herders")],
            ],
            [9*cm, 7.5*cm],
        ),
        sp(4),
        p(
            "<code>raise_if_not_found: false</code> prevents hard failures when "
            "optional columns are absent from a given export."
        ),

        sp(4), h2("3.2 Temporal Index"),
        p(
            "<code>add_temporal_index</code> parses the <code>date</code> column as a "
            "datetime (format: <code>mixed</code>, cast enabled) and sets it as the "
            "temporal index, keyed to the configured groupers. This index drives "
            "time-series aggregation and per-group splitting downstream."
        ),

        sp(4), h2("3.3 Missing Value Replacement"),
        p(
            "<code>replace_missing_with_label</code> fills null values in six categorical "
            "columns with the label <b>\"Unknown\"</b>:"
        ),
        bullet("species_killed, is_livestock, livestock_lost_in_bush"),
        bullet("species_injured, livestock_not_lost_in_bush_herder_present, ranch, boma_or_bush"),

        sp(4), h2("3.4 Integer Conversion"),
        p(
            "<code>convert_to_int</code> coerces five count columns to integer, "
            "replacing any non-numeric values with <b>0</b> "
            "(<code>errors: coerce, fill_value: 0, inplace: true</code>):"
        ),
        bullet("total_killed, total_injured — head count of animals killed or injured"),
        bullet("community_hunt, mock_hunt, scared_by_herders — boolean-encoded incident flags"),

        sp(4), h2("3.5 Value Normalisation"),
        p(
            "A series of <code>map_column_values</code> tasks standardises inconsistent "
            "free-text entries across five columns. Key normalisation rules:"
        ),
        make_table(
            [
                [c("Column"),          c("Examples normalised")],
                [c("species_killed"),  c("'cow' → 'Cow'; 'Bull' → 'Cow'; 'Cow (calf)' → 'Cow'; 'Giraffe (foal)' → 'Giraffe'")],
                [c("species_injured"), c("'cow' → 'Cow'; 'shoat' → 'Shoat'; 'Sheep-kid' → 'Sheep'")],
                [c("is_livestock"),    c("'YES'/'Yes' → 'Yes'; 'NO'/'No' → 'No'; 'No prey, but lion disciplined' → 'No'")],
                [c("boma_or_bush"),    c("'bush' → 'Bush'; 'BOMA' → 'Boma'")],
                [c("livestock_lost_in_bush / livestock_not_lost_in_bush_herder_present"),
                 c("'yes'/'YES'/'Yes' → 'Yes'; 'no'/'NO'/'No' → 'No'; 'unknown'/'Unknown'/'UNKNOWN' → 'Unknown'")],
                [c("ranch"),           c("'EGR'/'MGR'/'OGR'; 'KUKU'/'Other-KUKU'/'Kuku Group ranch' → 'Kuku'; "
                                        "'Other - TZ'/'Tanzania' → 'Tanzania'; 'unknown'/'UNKNOWN' → 'Unknown'")],
            ],
            [4*cm, 12.5*cm],
        ),

        sp(4), h2("3.6 Geometry Conversion"),
        p(
            "<code>utm_to_4326</code> converts tabular UTM coordinates to a GeoDataFrame "
            "with WGS 84 point geometry. Source projection: <b>EPSG:32737</b> "
            "(UTM Zone 37S — appropriate for the Amboseli region). "
            "Source columns <code>GPS X (UTM)</code> and <code>GPS Y (UTM)</code> are "
            "then dropped by a subsequent <code>map_columns</code> call. "
            "Rows with a null <code>None</code> column artefact are also removed."
        ),

        sp(4), h2("3.7 Livestock Filtering"),
        p(
            "Two sequential filter steps isolate only livestock predation records:"
        ),
        bullet(
            "<b>filter_row_values</b> retains rows where <code>species_killed</code> "
            "is one of: Cow, Goat, Shoat, Donkey, Sheep, Bull, Dog."
        ),
        bullet(
            "<b>exclude_row_values</b> removes any remaining wild-species rows "
            "(Zebra, Wildebeest, Eland, Giraffe, Hyena - spotted, Oryx, Ostrich, "
            "Porcupine, Thompson's Gazelle, Grant's Gazelle, Lesser kudu, Buffalo, Gazelle). "
            "This double-step ensures clean separation even when form data is inconsistent."
        ),
        p(
            "Additionally, <code>custom_map_column</code> converts the text "
            "<code>is_livestock</code> column to boolean "
            "(<code>True</code> / <code>False</code>) for downstream logical filtering."
        ),

        sp(4), h2("3.8 Color Mapping"),
        p(
            "Three colour dictionaries are defined using pastel tones for visual clarity "
            "in maps and charts. <code>get_color_map</code> builds legend-compatible "
            "colour maps; <code>map_color_column_value</code> writes per-row hex colour "
            "values into new columns:"
        ),
        make_table(
            [
                [c("New column"),             c("Source column"),  c("Colour scheme")],
                [c("species_killed_colors"),  c("species_killed"), c("Pastel coral/peach/yellow tones per species")],
                [c("ranch_colors"),           c("ranch"),          c("Pastel coral → lavender → grey per ranch")],
                [c("boma_or_bush_colors"),    c("boma_or_bush"),   c("Pastel sky blue (Boma) / mint green (Bush) / grey (Unknown)")],
            ],
            [4.5*cm, 3.5*cm, 8.5*cm],
        ),
        sp(4),
        note(
            "Color columns are written <i>before</i> <code>split_groups</code> so "
            "every per-group partition inherits the full colour vocabulary, preventing "
            "palette inconsistencies when a group contains only a subset of species or ranches."
        ),
    ]

    # ── 4. Static Map Layers ──────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Static Map Layers"), hr(),
        p(
            "Four static layers are built once and composited onto every group-level "
            "map to provide spatial context."
        ),

        h2("4.1 Layer Styles"),
        make_table(
            [
                [c("Layer"),                 c("Colour (RGB)"),             c("Opacity"), c("Filled"), c("Notes")],
                [c("Group Ranch Boundaries"), c("(169, 169, 169) grey"),     c("55 %"),    c("No"),
                 c("Outline only, line width 4.5")],
                [c("Conflict Hotspots"),      c("(220, 20, 60) crimson"),    c("75 %"),    c("Yes"),
                 c("Point radius 2.55, line width 1.95")],
                [c("Protected Areas"),        c("(77, 102, 0) dark green"),  c("35 %"),    c("Yes"),
                 c("Line width 1.95")],
                [c("Hotspot Text Labels"),    c("(20, 20, 20) near-black"),  c("—"),       c("—"),
                 c("Arial, 1 000 m base, 40–75 px clamp, centroid-anchored, billboard")],
            ],
            [3.8*cm, 3.8*cm, 2*cm, 1.8*cm, 5.1*cm],
        ),
        sp(4),
        p(
            "The group ranch layer is outline-only (not filled) so predation points "
            "overlaid on top remain fully visible. Protected areas are filled at low "
            "opacity to show extent without obscuring the data layer."
        ),
    ]

    # ── 5. Spatial Analysis ───────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Spatial Analysis &amp; Map Outputs"), hr(),

        h2("5.1 Geometry Cleaning"),
        p(
            "Before any spatial layer is created, two cleaning steps are applied "
            "per group:"
        ),
        bullet(
            "<b>exclude_geom_outliers</b> (z-threshold: 3) removes points whose "
            "coordinates are statistical outliers relative to the group centroid. "
            "This catches GPS errors or data entry mistakes without requiring manual review."
        ),
        bullet(
            "<b>drop_null_geometry</b> removes records where the geometry column is "
            "null — rows where GPS coordinates were missing or unparseable."
        ),

        sp(4), h2("5.2 Livestock Predation Event Map"),
        p(
            "<code>create_scatterplot_layer</code> renders each cleaned predation "
            "incident as a scatter point, coloured by <code>species_killed_colors</code>. "
            "The legend groups points by livestock species."
        ),
        make_table(
            [
                [c("Property"),     c("Value")],
                [c("Fill colour"),  c("species_killed_colors (per-row hex column)")],
                [c("Line colour"),  c("species_killed_colors")],
                [c("Radius"),       c("4 px (screen space)")],
                [c("Opacity"),      c("75 %")],
                [c("Stroked"),      c("Yes")],
            ],
            [4.5*cm, 12*cm],
        ),
        sp(4),
        p(
            "The scatter layer is combined with the group ranch and protected area "
            "static layers via <code>combine_deckgl_map_layers</code>. "
            "The map zoom and centre are calculated from the full Amboseli group ranch "
            "boundary extent (<code>view_state_deck_gdf</code>), keeping a consistent "
            "spatial frame across all groups regardless of where incidents occur. "
            "The map is persisted as HTML (suffix: <code>livestock_predation_map</code>) "
            "and converted to PNG at 2× scale with a 40 s tile-load wait."
        ),

        sp(4), h2("5.3 Predation Density Grid Map"),
        p(
            "<code>generate_density_grid</code> builds a 2 000 m hexagonal or square "
            "grid over the cleaned predation points (<code>geometry_type: point</code>) "
            "and counts the number of incidents per cell."
        ),
        p(
            "The density values are then:"
        ),
        bullet(
            "<b>Sorted ascending</b> (<code>sort_values</code>) to ensure correct "
            "classification boundaries."
        ),
        bullet(
            "<b>Classified</b> into 5 equal-interval bins "
            "(<code>apply_classification</code>, scheme: <code>equal_interval</code>, "
            "k: 5) with range labels."
        ),
        bullet(
            "<b>Coloured</b> with a sequential yellow-to-dark-red palette "
            "(<code>apply_color_map</code>): "
            "#FFF7BC → #FD8D3C → #F03B20 → #BD0026 → #99000D."
        ),
        p(
            "The classified grid is rendered as a GeoJSON polygon layer "
            "(<code>create_geojson_layer</code>) at 55 % opacity with a thin black "
            "outline. It is combined with the group ranch and protected area static layers, "
            "aligned to the same Amboseli view state as the event map, and persisted as "
            "HTML (suffix: <code>density_grid_map</code>) and PNG."
        ),
    ]

    # ── 6. Summary Tables ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Summary Tables"), hr(),
        p(
            "Four CSV summary tables are generated per group via <code>mapvalues</code> "
            "iteration over <code>split_events_by_group</code>. All tables are persisted "
            "to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."
        ),

        h2("6.1 Total Livestock Killed by Ranch"),
        p(
            "<code>crosstab_summary</code> produces a pivot table with "
            "<code>species_killed</code> as rows, <code>ranch</code> as columns, "
            "and <code>total_killed</code> summed as the value. "
            "<code>margins: true</code> adds row and column totals labelled "
            "\"Total\". Output filename prefix: <code>total_livestock_killed_by_ranch</code>."
        ),

        sp(4), h2("6.2 Location of Attack"),
        p(
            "<code>aggregate_by</code> counts incidents grouped by <code>boma_or_bush</code>, "
            "appending a percentage column (<code>add_percent: true</code>). "
            "Results are sorted ascending. "
            "This shows the proportion of attacks occurring inside bomas (corrals) "
            "versus in the bush. Output filename prefix: <code>location_of_attack</code>."
        ),

        sp(4), h2("6.3 Herder Effectiveness"),
        p(
            "The custom task <code>herder_effectiveness</code> analyses livestock loss "
            "outcomes relative to whether animals were accompanied by herders. "
            "It combines the <code>boma_or_bush</code>, <code>livestock_lost_in_bush</code>, "
            "and <code>livestock_not_lost_in_bush_herder_present</code> columns to "
            "compute effectiveness metrics. "
            "Output filename prefix: <code>herder_effectiveness</code>."
        ),

        sp(4), h2("6.4 Livestock Species by Ranch Matrix"),
        p(
            "<code>species_by_ranch_matrix</code> builds a matrix of livestock species "
            "killed per ranch (<code>livestock_only: true, normalize: false</code>). "
            "This raw count matrix complements the crosstab by providing a clean "
            "species × ranch summary without row/column totals. "
            "Output filename prefix: <code>species_ranch_matrix</code>."
        ),
    ]

    # ── 7. Charts ─────────────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Charts"), hr(),
        p(
            "Eight chart types are produced per group. All charts are persisted as "
            "HTML and converted to PNG at 2× scale."
        ),

        h2("7.1 Pie Charts"),
        make_table(
            [
                [c("Chart"),                        c("Value column"),  c("Label column"),   c("Colour column"),          c("Filename suffix")],
                [c("Total livestock killed by species"), c("total_killed"), c("species_killed"), c("species_killed_colors"), c("livestock_killed_pie_chart")],
                [c("Total livestock killed by ranch"),   c("total_killed"), c("ranch"),          c("ranch_colors"),          c("livestock_killed_by_ranch_pie_chart")],
            ],
            [5.5*cm, 2.8*cm, 2.8*cm, 3.5*cm, 4.4*cm],
        ),
        sp(4),
        p(
            "Both pie charts display <code>textinfo: percent+label+value</code> "
            "with a font size of 15. Legends are shown."
        ),

        sp(4), h2("7.2 Heatmaps"),
        make_table(
            [
                [c("Chart"),                          c("X-axis"),       c("Y-axis"),       c("Value"),      c("Filename suffix")],
                [c("Species by ranch"),               c("species_killed"), c("ranch"),       c("total_killed (sum)"), c("species_by_ranch_heatmap")],
                [c("Species by time frequency"),      c("date (binned by time_frequency)"), c("species_killed"), c("total_killed (sum)"), c("species_by_time_heatmap")],
            ],
            [4*cm, 4*cm, 3*cm, 3.5*cm, 4.5*cm],
        ),
        sp(4),
        p(
            "Both heatmaps use <code>draw_custom_heatmap</code> with the "
            "<b>YlOrRd</b> colorscale, values shown (<code>show_values: true</code>), "
            "no normalisation, and no custom axis ordering. "
            "The time heatmap bins the date axis at the user-selected time frequency."
        ),

        sp(4), h2("7.3 Multi-bar Time Series"),
        p(
            "<code>draw_custom_multi_bar_time_series</code> creates a faceted bar chart "
            "with one sub-plot per group value, showing kills over time:"
        ),
        make_table(
            [
                [c("Chart"),                    c("Group column"),   c("Filename suffix")],
                [c("Killed by ranch"),          c("ranch"),          c("livestock_species_killed_ranch_multibar")],
                [c("Killed by species"),        c("species_killed"), c("livestock_species_killed_multibar")],
            ],
            [5*cm, 4*cm, 7.5*cm],
        ),
        sp(4),
        p(
            "Common parameters: x-axis = <code>date</code>, y-axis = <code>total_killed</code>, "
            "aggregation = <code>sum</code>, time frequency from user selection, "
            "2 columns, independent y-axes (<code>shared_yaxes: false</code>), "
            "row height 400 px, bar colour <code>#6495ed</code> (cornflower blue), "
            "PNG export at 1 280 × 2 000 px."
        ),

        sp(4), h2("7.4 Multi-line Time Series"),
        p(
            "<code>draw_custom_multi_line_time_series</code> plots all group values "
            "on a single chart as overlapping lines, useful for direct comparison:"
        ),
        make_table(
            [
                [c("Chart"),                    c("Group column"),   c("Colour column"),        c("Legend title"), c("Filename suffix")],
                [c("Killed by ranch"),          c("ranch"),          c("ranch_colors"),          c("Ranch"),        c("livestock_killed_over_time_by_ranch_chart")],
                [c("Killed by species"),        c("species_killed"), c("species_killed_colors"), c("Species"),      c("livestock_killed_over_time_by_species_chart")],
            ],
            [3.5*cm, 3*cm, 3.5*cm, 2.5*cm, 5*cm],
        ),
        sp(4),
        p(
            "Common parameters: x-axis = <code>date</code>, y-axis = <code>total_killed</code>, "
            "aggregation = <code>sum</code>, solid linear lines, no fill, "
            "ascending order, <code>hovermode: x unified</code>, "
            "gridlines on both axes (<code>#e5e5e5</code>), "
            "light grey plot background (<code>#f5f5f5</code>)."
        ),
    ]

    # ── 8. Word Report ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Word Report (.docx)"), hr(),

        h2("8.1 Cover Page"),
        p(
            "<code>create_guardians_ctx_cover</code> builds the cover context "
            "(report period from <code>time_range</code>, preparer: <i>Ecoscope</i>). "
            "<code>create_context_page_lg</code> renders it into "
            "<code>context_page.docx</code> using the "
            "<code>predation_cover_page.docx</code> template."
        ),

        sp(4), h2("8.2 Main Report Section"),
        p(
            "<code>generate_predation_report</code> renders the main report content "
            "from the <code>custom_patrol_template.docx</code> template, writing output "
            "to the results directory."
        ),

        sp(4), h2("8.3 Document Merge"),
        p(
            "<code>merge_cl_files</code> concatenates the cover page "
            "(<code>context_page.docx</code>) and the main report section "
            "into a single Word file saved to the results directory."
        ),
    ]

    # ── 9. Interactive Dashboard ───────────────────────────────────────────────
    story += [
        sp(4), h1("9. Interactive Dashboard"), hr(),
        p(
            "<code>gather_dashboard</code> assembles the predation dashboard from "
            "eight widget groups:"
        ),
        make_table(
            [
                [c("Widget title"),                     c("Type"),   c("Source task")],
                [c("Predation points"),                 c("Map"),    c("persist_livestock_html → create_predation_widgets")],
                [c("Predation Density"),                c("Map"),    c("persist_grid_html → create_density_widgets")],
                [c("Total livestock killed by species"), c("Plot"),  c("persist_total_livestock_pie → total_livestock_pie_chart_widget")],
                [c("Total livestock killed by ranch"),   c("Plot"),  c("persist_ranch_livestock_pie → ranch_pie_chart_widget")],
                [c("Livestock species killed by ranch"),  c("Plot"), c("persist_species_ranch_heatmap → species_heatmap_widget")],
                [c("Livestock species killed by time"),   c("Plot"), c("persist_species_time_heatmap → time_heatmap_widget")],
                [c("Livestock species killed by ranch"),  c("Plot"), c("persist_ranch_killed_multiline → ranch_line_widget")],
                [c("Livestock species killed by species"), c("Plot"), c("persist_species_killed_multiline → species_line_widget")],
            ],
            [6*cm, 2*cm, 8.5*cm],
        ),
        sp(4),
        note(
            "All widget tasks use <code>skipif: [never]</code> so the dashboard always "
            "assembles, even when some groups have no data."
        ),
    ]

    # ── 10. Output Files ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Output Files"), hr(),
        p(
            "All files are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."
        ),
        make_table(
            [
                [c("File / pattern"),                                    c("Format"),  c("Content")],
                [c("<group>_livestock_predation_map.html"),              c("HTML"),    c("Interactive livestock predation event scatter map")],
                [c("<group>_density_grid_map.html"),                     c("HTML"),    c("Interactive predation density grid map")],
                [c("<group>_livestock_predation_map.png"),               c("PNG"),     c("2× screenshot of the predation event map")],
                [c("<group>_density_grid_map.png"),                      c("PNG"),     c("2× screenshot of the density grid map")],
                [c("<group>_livestock_killed_pie_chart.png"),            c("PNG"),     c("2× screenshot of species pie chart")],
                [c("<group>_livestock_killed_by_ranch_pie_chart.png"),   c("PNG"),     c("2× screenshot of ranch pie chart")],
                [c("<group>_species_by_ranch_heatmap.png"),              c("PNG"),     c("2× screenshot of species × ranch heatmap")],
                [c("<group>_species_by_time_heatmap.png"),               c("PNG"),     c("2× screenshot of species × time heatmap")],
                [c("<group>_livestock_species_killed_ranch_multibar.png"), c("PNG"),   c("2× screenshot of kills by ranch multi-bar chart (1280×2000)")],
                [c("<group>_livestock_species_killed_multibar.png"),     c("PNG"),     c("2× screenshot of kills by species multi-bar chart (1280×2000)")],
                [c("<group>_livestock_killed_over_time_by_ranch_chart.png"), c("PNG"), c("2× screenshot of kills by ranch multi-line chart")],
                [c("<group>_livestock_killed_over_time_by_species_chart.png"), c("PNG"), c("2× screenshot of kills by species multi-line chart")],
                [c("<group>_total_livestock_killed_by_ranch.csv"),       c("CSV"),     c("Species × ranch crosstab of total kills with margins")],
                [c("<group>_location_of_attack.csv"),                    c("CSV"),     c("Boma vs bush attack counts and percentages")],
                [c("<group>_herder_effectiveness.csv"),                  c("CSV"),     c("Livestock loss outcomes relative to herder presence")],
                [c("<group>_species_ranch_matrix.csv"),                  c("CSV"),     c("Livestock species × ranch kill count matrix")],
                [c("context_page.docx"),                                 c("Word"),    c("Rendered report cover page")],
                [c("<merged_report>.docx"),                              c("Word"),    c("Final combined Word report (cover + main section)")],
            ],
            [6.5*cm, 1.8*cm, 8.2*cm],
        ),
    ]

    # ── 11. Workflow Execution Logic ──────────────────────────────────────────
    story += [
        sp(4), h1("11. Workflow Execution Logic"), hr(),

        h2("11.1 Skip Conditions"),
        p(
            "Two default skip conditions apply to every task "
            "(<code>task-instance-defaults</code>):"
        ),
        bullet(
            "<b>any_is_empty_df</b> — skips the task (and all dependants) when "
            "any input DataFrame is empty, handling periods or species groups with no "
            "recorded incidents gracefully."
        ),
        bullet(
            "<b>any_dependency_skipped</b> — propagates skips downstream automatically."
        ),
        p(
            "Widget tasks override this with <code>skipif: [never]</code> to ensure "
            "the dashboard always assembles. Pie chart and heatmap tasks also carry "
            "explicit <code>skipif</code> guards for the same reason."
        ),

        sp(4), h2("11.2 Data Flow Summary"),
        make_table(
            [
                [c("Stage"),              c("Tasks")],
                [c("Setup"),              c("Workflow details, time range, groupers (empty by default), time frequency, base maps")],
                [c("Geodata download"),   c("3 boundary files + 2 Word templates from Dropbox")],
                [c("Static layers"),      c("Ranch boundaries, conflict hotspots, protected areas, hotspot text labels")],
                [c("Data ingest"),        c("Load local CSV → column mapping → temporal index → missing label replacement")],
                [c("Cleaning"),           c("Integer conversion → value normalisation (5 columns) → UTM to WGS84 → drop GPS columns")],
                [c("Livestock filter"),   c("is_livestock boolean mapping → filter to livestock species → exclude wild species")],
                [c("Colour mapping"),     c("Species, ranch, boma_or_bush colour columns → split groups")],
                [c("Summary tables"),     c("Crosstab (species × ranch), location of attack, herder effectiveness, species-ranch matrix → CSV persist")],
                [c("Charts branch"),      c("2 pie charts + 2 heatmaps + 2 multi-bar + 2 multi-line → HTML → PNG → widgets")],
                [c("Event map branch"),   c("Outlier removal → drop null geoms → scatter layer → combine layers → zoom → draw map → HTML → PNG → widget")],
                [c("Density branch"),     c("Density grid → sort → classify → colormap → GeoJSON layer → combine layers → draw map → HTML → PNG → widget")],
                [c("Report assembly"),    c("Cover page context → context_page.docx + generate_predation_report → merge_cl_files")],
                [c("Dashboard"),          c("gather_dashboard combines 8 widget groups")],
            ],
            [4.5*cm, 12*cm],
        ),
    ]

    # ── 12. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("12. Software Versions"), hr(),
        make_table(
            [
                [c("Package"),                               c("Version"),    c("Role")],
                [c("ecoscope-workflows-core"),               c("0.22.17.*"),  c("Core task library and workflow engine")],
                [c("ecoscope-workflows-ext-ecoscope"),       c("0.22.17.*"),  c("Spatial analysis tasks (density grid, relocations, geometry ops)")],
                [c("ecoscope-workflows-ext-custom"),         c("0.0.46.*"),   c("Utility tasks (column mapping, value mapping, screenshots, UTM conversion)")],
                [c("ecoscope-workflows-ext-ste"),            c("0.0.20.*"),   c("Summary and aggregation tasks (crosstab, aggregate_by, sort, classify)")],
                [c("ecoscope-workflows-ext-mnc"),            c("0.0.9.*"),    c("Additional utility tasks")],
                [c("ecoscope-workflows-ext-big-life"),       c("0.0.11.*"),   c("Big Life Foundation domain tasks")],
                [c("ecoscope-workflows-ext-lion-guardians"), c("0.0.6.*"),    c("Lion Guardians report rendering tasks (herder_effectiveness, species_by_ranch_matrix, generate_predation_report)")],
                [c("ecoscope-workflows-ext-mep"),            c("0.0.19.*"),   c("MEP domain tasks (dashboard assembly)")],
            ],
            [6*cm, 2.5*cm, 8*cm],
        ),
        sp(4),
        p(
            "Packages are distributed via the <code>prefix.dev</code> conda channel "
            "and pinned to patch-compatible versions (<code>.*</code> suffix). "
            "The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
