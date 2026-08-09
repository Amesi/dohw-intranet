"""Prototype — Blog article page, styled to match whichever listing variant sent us here.

Content is the real "Historic Steel Arch Bridge to Transform Momase
Connectivity" article, extracted from www.works.gov.pg/articles/view/
historic-steel-arch-bridge-to-transform-momase-connectivity (byline and
body copied as published, 11 May 2026).
"""

import frappe

MOCK_POST = {
    "title": "Historic Steel Arch Bridge to Transform Momase Connectivity",
    "excerpt": "The Hawaiin Bridge — PNG's first steel arch bridge, built without a centre pier — nears completion on the Coastal Highway linking Wewak to the Wutung border.",
    "category": "Project Updates",
    "author": "Brian Alois",
    "date": "11 May 2026",
    "read_time": "3 min read",
    "content": """
        <p>The Hawaiin Bridge, rising along the Coastal Highway that links Wewak to Aitape,
        Vanimo, and onward to the Indonesian border at Wutung, is set to become a landmark
        in Papua New Guinea's infrastructure development. At 66 metres long, dual-lane, and
        built without a centre pier, it is the first steel arch bridge ever constructed in
        Papua New Guinea, marking a significant leap in engineering technology for the
        nation.</p>
        <p>Funded entirely by the national government under the ConnectPNG Program, the
        project carries a price tag of K20.8 million. Construction is being led by Covec PNG
        Limited, with AG Investment Ltd engaged as a sub-contractor. The bridge is scheduled
        for completion on 6 July 2026, a date that will mark a new chapter in the country's
        road network.</p>
        <h2>More than a technical achievement</h2>
        <p>The Hawaiin Bridge is more than a technical achievement — it is a lifeline. The
        old structure has already been the site of accidents and fatalities, underscoring the
        urgency of finishing the project. Once completed, it will provide safer passage for
        thousands of travellers, reduce risks for commuters, and serve as a vital artery for
        trade and economic activity in the greater Sepik Region.</p>
        <p>The bridge's strategic location along the Coastal Highway means it will directly
        benefit communities from Wewak through Aitape and Vanimo, extending connectivity to
        the Wutung Border Post with Indonesia. This improved link is expected to boost
        cross-border commerce, tourism, and regional development, while also strengthening
        national unity by tying remote communities more closely into the country's economic
        mainstream.</p>
        <h2>A legacy project</h2>
        <p>The Hawaiin Bridge is not just another piece of infrastructure — it is a legacy
        project. By introducing steel arch technology to Papua New Guinea, it sets a
        precedent for future designs and demonstrates the government's commitment to
        modernising the nation's transport system. The absence of a centre pier allows
        smoother traffic flow and greater resilience against flooding, making it a model for
        future bridge construction across the country.</p>
        <p>As the July 2026 completion date approaches, anticipation is building. The Hawaiin
        Bridge will stand not only as a feat of engineering but also as a symbol of
        resilience and development — connecting communities, saving lives, and enabling
        prosperity for generations to come.</p>
    """,
}


def get_context(context):
    context.no_cache = 1
    context.show_sidebar = 0
    context.title = MOCK_POST["title"] + " — Prototype"
    context.variant = frappe.form_dict.get("variant", "a")
    context.post = MOCK_POST
    return context
