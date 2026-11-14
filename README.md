# Saudi + Arabic + Sports IPTV Playlist

A merged M3U playlist built from the three public iptv-org lists below.

## Use this playlist

**Direct M3U URL (for IPTV apps):**

https://raw.githubusercontent.com/HeshamB7/Saudi-Arabic-Sports-IPTV/main/playlist.m3u

## Included sources

1. Saudi Arabia: https://iptv-org.github.io/iptv/countries/sa.m3u
2. Sports category: https://iptv-org.github.io/iptv/categories/sports.m3u
3. Arab world: https://iptv-org.github.io/iptv/regions/arab.m3u

## Duplicate handling

Channels are processed in this order: Saudi, Sports, then Arab. Duplicate channel names are normalized (including common quality suffixes such as HD/FHD/4K) and only the first matching entry is kept. Stream URLs are also checked for duplicates.

The first successful build contained 942 unique channel entries:
- 55 added from the Saudi list
- 501 added from the sports list
- 386 added from the Arab-world list

The sports source is iptv-org's full sports category, so it may include sports channels from outside the Arab world too.

## Automatic updates

GitHub Actions rebuilds playlist.m3u every 6 hours and whenever the merger script or workflow is changed.

## Notes

This repository only combines publicly listed stream links; it does not host video streams. Availability and legality of individual streams depend on their original providers and location. Paid subscription channels are not made free by this playlist.
