# GameDB-N64
Nintendo 64, part of [GameDB](https://github.com/niemasd/GameDB).

## Structured Downloads
* **[`N64.data.json`](https://github.com/niemasd/GameDB-N64/releases/latest/download/N64.data.json):** All data, structured in the JSON format
* **[`N64.data.tsv`](https://github.com/niemasd/GameDB-N64/releases/latest/download/N64.data.tsv):** All data, structured in the TSV format
* **[`N64.release_dates.pdf`](https://github.com/niemasd/GameDB-N64/releases/latest/download/N64.release_dates.pdf):** Histogram of release dates, stratified by region
* **[`N64.titles.json`](https://github.com/niemasd/GameDB-N64/releases/latest/download/N64.titles.json):** Mapping of serial numbers to game titles, structured in the JSON format

# Notes

## Uniquely Identifying Games

The game folders in [`games`](games) have the structure `NUS-NXXY-RRR`, where `XXY` is the game code (also known as game ID), and `RRR` is the region code. The game code is stored directly within the ROM and can be used to uniquely identify the game:

* The first 2 characters of the game code (`XX` in my notation above) are the **Cartridge ID**, which is at offsets `0x3C` through `0x3D` (inclusive) of the [ROM header](https://en64.shoutwiki.com/wiki/ROM#Cartridge_ROM_Header)
* The 3rd character of the game code (`Y` in my notation above) is the **Country Code**, which is at offset `0x3E` of the [ROM header](https://en64.shoutwiki.com/wiki/ROM#Cartridge_ROM_Header)

Note that the [ROM header documentation](https://en64.shoutwiki.com/wiki/ROM#Cartridge_ROM_Header) assumes big-endian byte ordering, whereas some ROMs are little-endian. Before attempting to parse the game code from a ROM header, you first need to check the ROM's endianness, and if it is little-endian, you need to convert to big-endian. See the [GameID N64 identification code](https://github.com/niemasd/GameID/blob/9cbbcf62b0123ede7ff6e835a0c7374f6d2ad6b8/GameID.py#L351-L382) for implementation details.

# Sources
* [GameFAQs](https://gamefaqs.gamespot.com/)
* [Micro-64](http://micro-64.com/database/masterlist.shtml)
* [MobyGames](https://www.mobygames.com/)
* [Nintendo64EVER](https://www.nintendo64ever.com/)
* [Wikipedia](https://www.wikipedia.org/)
