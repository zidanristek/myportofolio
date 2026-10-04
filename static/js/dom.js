// Django escapes every {{ variable }} on its own. A card built in JavaScript
// reaches the page through innerHTML instead, where a title carrying a tag
// would run as markup, so the escaping has to be done by hand. Two pages now
// build cards that way, which is why this lives here rather than in either of
// their inline scripts.
function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}
