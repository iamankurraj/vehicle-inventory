
def format_inventory_response(rows, part, region):
    if not rows:
        return (
            f"<div class='inventory-response'>"
            f"No available stock found for {part}."
            f"</div>"
        )

    tiles_html = ""
    for provider, _, qty in rows:
        tiles_html += (
            "<div class='inventory-tile'>"
            f"<div class='provider'>{provider}</div>"
            f"<div class='qty'>{qty} units</div>"
            "</div>"
        )

    return (
        "<div class='inventory-response'>"
        f"<div class='title'>Inventory for {part.title()} in {region.title()}</div>"
        f"{tiles_html}"
        "</div>"
    )

def format_provider_response(providers, region):
    if not providers:
        return f"No providers found in {region}."

    tiles = "".join(
        f"""
        <div class="inventory-tile">
          <div class="provider">{p}</div>
        </div>
        """
        for p in providers
    )

    return f"""
    <div class="inventory-response">
      <div class="title">Providers in {region.title()}</div>
      {tiles}
    </div>
    """
