"""Work card, ported from ARKfolio's WorkCard.vue.

Takes a plain dict (one entry from content.works.WORKS) instead of a
Vue prop. `v-reveal` (scroll-in animation directive) has no ARKlight
equivalent yet -- omitted, noted rather than silently dropped.
"""

from arklight import Article, Container, Span, Text, Link


def work_card(work: dict):
    ribbon_class = "status-ribbon mature" if work.get("mature") else "status-ribbon"
    tags = work["tags"][:3]

    return Article(
        Container(
            Span(f"{work['kind']} \u00b7 {work['status']}", class_name=ribbon_class),
            class_name=f"cover {work['cover_class']}",
        ),
        Container(
            Text(work["tagline"], class_name="tagline"),
            Container(
                *[
                    Span(tag, class_name="badge mature" if tag == "Mature Content" else "badge")
                    for tag in tags
                ],
                class_name="tags",
            ),
            Text(work["summary_card"], class_name="desc"),
            Container(
                Link("Full synopsis \u2192", href=f"/works#{work['slug']}"),
                *[
                    Link(f"{link['label']} \u2197", href=link["url"], target="_blank")
                    for link in work["links"]
                ],
                class_name="work-links",
            ),
            class_name="work-body",
        ),
        class_name="work-card",
    )
