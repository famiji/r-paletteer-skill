# paletteer 调色板目录 / Palettes Catalog

> 本文档包含 paletteer 中最常用调色板的完整目录，按源包组织，包含 HEX 色值、类型分类和适用场景。
>
> 共涵盖 10 个常用源包，约 150+ 个调色板的精确颜色数据。
>
> 如需查询全部 2893 个调色板（来自 79 个源包），请在 R 中安装 paletteer 并运行 `palettes_c_names`、`palettes_d_names`、`palettes_dynamic_names`。

---

## 类型说明 / Type Definitions

| 类型 | paletteer 函数 | 说明 | 典型用途 |
|------|---------------|------|---------|
| **连续型 (continuous)** | `paletteer_c()` | 可生成任意数量颜色，平滑过渡 | 热力图、密度图、等值线 |
| **离散型 (discrete)** | `paletteer_d()` | 固定颜色集合，不随请求数量变化 | 分组散点图、柱状图 |
| **动态型 (dynamic)** | `paletteer_dynamic()` | 颜色随请求数量变化 | 层级分类、可变分组 |

| 类别 | 说明 | 典型用途 |
|------|------|---------|
| **顺序型 (sequential)** | 单色调由浅到深 | 有序数值（低到高） |
| **发散型 (diverging)** | 两个极端色 + 中间色 | 偏离中心值（如温度偏差） |
| **定性型 (qualitative)** | 互不相似的类别色 | 无序分类 |

---

## RColorBrewer (35 palettes)

经典 ColorBrewer 调色板，广泛应用于科学可视化。CRAN 可直接安装。

### 顺序型 Sequential (18 palettes)

| 调色板 | 最大颜色数 | 色盲友好 | 印刷友好 | HEX 色值 |
|--------|-----------|---------|---------|---------|
| Blues | 9 | ✓ | ✓ | `#F7FBFF #DEEBF7 #C6DBEF #9ECAE1 #6BAED6 #4292C6 #2171B5 #08519C #08306B` |
| BuGn | 9 | ✓ | ✓ | `#F7FCFD #E5F5F9 #CCECE6 #99D8C9 #66C2A4 #41AE76 #238B45 #006D2C #00441B` |
| BuPu | 9 | ✓ | ✓ | `#F7FCFD #E0ECF4 #BFD3E6 #8C96C1 #8C6BB1 #88419D #810F7C #4D004B` |
| GnBu | 9 | ✓ | ✓ | `#F7FCF0 #E0F3DB #CCEBC5 #A8DDB5 #7BCCC4 #4EB3D3 #2B8CBE #08589E` |
| Greens | 9 | ✓ | ✓ | `#F7FCF5 #E5F5E0 #C7E9C0 #A1D99B #74C476 #41AB5D #238B45 #006D2C #00441B` |
| Greys | 9 | ✓ | ✓ | `#FFFFFF #F0F0F0 #D9D9D9 #BDBDBD #969696 #737373 #525252 #252525 #000000` |
| Oranges | 9 | ✓ | ✓ | `#FFF5EB #FEE6CE #FDD0A2 #FDAE6B #FD8D3C #F16913 #D94801 #A63603 #7F2704` |
| OrRd | 9 | ✓ | ✓ | `#FFF7EC #FEE8C8 #FDD49E #FDBB84 #FC8D59 #EF6548 #D7301F #B30000 #7F0000` |
| PuBu | 9 | ✓ | ✓ | `#F1EEF6 #D0D1E6 #A6BDDB #74A9CF #3690C0 #0570B0 #045A8D #023858` |
| PuBuGn | 9 | ✓ | ✓ | `#F1EEF6 #D4B9DA #C994C7 #DF65B0 #E7298A #CE1256 #980043 #67001F` |
| PuRd | 9 | ✓ | ✓ | `#F1EEF6 #D4B9DA #C994C7 #DF65B0 #E7298A #CE1256 #980043 #67001F` |
| Purples | 9 | ✓ | ✓ | `#FCFBFD #EF3B2C #D0D1E6 #A6BDDB #74A9CF #3690C0 #0570B0 #045A8D #023858` |
| RdPu | 9 | ✓ | ✓ | `#FFF7F3 #FDE0DD #FCC5C0 #FA9FB5 #F768A1 #DD3497 #AE017E #7A0177 #49006A` |
| Reds | 9 | ✓ | ✓ | `#FFF5F0 #FEE0D2 #FCBBA1 #FC9272 #FB6A4A #EF3B2C #CB181D #A50F15 #67000D` |
| YlGn | 9 | ✓ | ✓ | `#FFFFE5 #F7FCB9 #D9F0A3 #ADDD8E #78C679 #41AB5D #238443 #006837 #004529` |
| YlGnBu | 9 | ✓ | ✓ | `#FFFFD9 #EDF8B1 #C7E9B4 #7FCDBB #41B6C4 #1D91C0 #225EA8 #253494 #081D58` |
| YlOrBr | 9 | ✓ | ✓ | `#FFFFE5 #FFF7BC #FEE391 #FEC44F #FE9929 #EC7014 #CC4C02 #993404 #662506` |
| YlOrRd | 9 | ✓ | ✓ | `#FFFFCC #FFEDA0 #FED976 #FEB24C #FD8D3C #FC4E2A #E31A1C #BD0026 #800026` |

### 发散型 Diverging (9 palettes)

| 调色板 | 最大颜色数 | 色盲友好 | 印刷友好 | HEX 色值 |
|--------|-----------|---------|---------|---------|
| BrBG | 11 | ✓ | ✓ | `#543005 #8C510A #BF812C #DFC27D #F6E8C3 #F5F5F5 #C7EAE5 #80CDC1 #35978F #01665E #003C30` |
| PiYG | 11 | ✓ | ✗ | `#8E0152 #C51B7D #DE77AE #F1B6DA #FDE0EF #F7F7F7 #E6F5D0 #B8E186 #7FBC41 #4D9221 #276419` |
| PRGn | 11 | ✓ | ✗ | `#40004B #762A83 #9970AB #C2A5CF #E7D4E8 #F7F7F7 #D9F0D3 #A6DBA0 #5AAE61 #1B7837 #00441B` |
| PuOr | 11 | ✓ | ✓ | `#2D004B #542788 #8073AC #B2ABD2 #D8DAEB #F7F7F7 #FEE0B6 #FDB863 #E08214 #B35806 #7F3B08` |
| RdBu | 11 | ✓ | ✓ | `#67001F #B2182B #D6604D #F4A582 #FDDBC7 #F7F7F7 #D1E5F0 #92C5DE #4393C3 #2166AC #053061` |
| RdGy | 11 | ✓ | ✓ | `#67001F #B2182B #D6604D #F4A582 #FDDBC7 #FFFFFF #E0E0E0 #BABABA #878787 #4D4D4D #1A1A1A` |
| RdYlBu | 11 | ✓ | ✓ | `#A50026 #D73027 #F46D43 #FDAE61 #FEE090 #FFFFBF #E0F3F8 #ABD9E9 #4575B4 #313695` |
| RdYlGn | 11 | ✗ | ✗ | `#A50026 #D73027 #F46D43 #FDAE61 #FEE08B #FFFFBF #D9EF8B #A6D96A #66BD63 #1A9850 #006837` |
| Spectral | 11 | ✗ | ✗ | `#9E0142 #D53E4F #F46D43 #FDAE61 #FEE08B #FFFFBF #E6F598 #ABDDA4 #66C2A5 #3288BD #5E4FA2` |

### 定性型 Qualitative (8 palettes)

| 调色板 | 最大颜色数 | 色盲友好 | 印刷友好 | HEX 色值 |
|--------|-----------|---------|---------|---------|
| Accent | 8 | ✗ | ✗ | `#7FC97F #BEAED4 #FDC086 #FFFF99 #386CB0 #F0027F #BF5B17 #666666` |
| Dark2 | 8 | ✓ | ✓ | `#1B9E77 #D95F02 #7570B3 #E7298A #66A61E #E6AB02 #A6761D #666666` |
| Paired | 12 | ✗ | ✗ | `#A6CEE3 #1F78B4 #B2DF8A #33A02C #FB9A99 #E31A1C #FDBF6F #FF7F00 #CAB2D6 #6A3D9A #FFFF99 #B15928` |
| Pastel1 | 9 | ✗ | ✗ | `#FBB4AE #B3CDE3 #CCEBC5 #DECBE4 #FCCDE5 #F9AED1 #FED9A6 #FFFFCC #D9D9D9` |
| Pastel2 | 8 | ✗ | ✗ | `#B3E2CD #FDCDC1 #CBD5E8 #F4CAE4 #E6F5C9 #FFF2AE #F1E2CC #CCCCCC` |
| Set1 | 9 | ✗ | ✗ | `#E41A1C #377EB8 #4DAF4A #984EA3 #FF7F00 #FFFF33 #A65628 #F781BF #999999` |
| Set2 | 8 | ✗ | ✗ | `#66C2A5 #FC8D62 #8DA0CB #E78AC3 #A6D85A #FFD92F #E5C494 #B3B3B3` |
| Set3 | 12 | ✗ | ✗ | `#8DD3C7 #FFFFB3 #BEBADA #FB8072 #80B1D3 #FDB462 #B3DE69 #FCCDE5 #D9D9D9 #BC80BD #CCEBC5 #FFED6F` |

---

## viridis (8 palettes, all continuous)

所有 viridis 调色板均为连续型、感知均匀且色盲友好。CRAN 可直接安装。

| 调色板 | 类别 | 色盲友好 | 印刷友好 | 说明 | 采样 HEX (n=10) |
|--------|------|---------|---------|------|----------------|
| viridis | sequential | ✓ | ✓ | 默认：紫到黄 | `#440154 #482878 #3E4A89 #31688E #26828E #1F9E89 #35B779 #6ECE58 #B5DE2B #FDE725` |
| magma | sequential | ✓ | ✗ | 黑到奶油，经洋红 | `#000004 #1C1044 #4F127B #812581 #B5367A #E55064 #FB8761 #FEC287 #FCDFA6 #FCFDBF` |
| plasma | sequential | ✓ | ✗ | 深蓝到黄，经粉 | `#0D0887 #5302A3 #8B0AA5 #B83289 #DB5C68 #F48849 #FE7F4D #FDB22F #F7E406 #F0F921` |
| inferno | sequential | ✓ | ✗ | 黑到奶油，经橙红 | `#000004 #1B0C41 #4A0C6B #781C6D #A52C60 #CF4446 #ED6925 #FB9A06 #F7D13D #FCFFA4` |
| cividis | sequential | ✓ | ✓ | 蓝到黄，色盲优化 | `#00224E #123570 #3B496C #575D6D #707173 #8A8678 #A59C74 #C3B369 #E1CC55 #FFEA46` |
| mako | sequential | ✓ | ✗ | 深到亮绿，经蓝青 | `#0B0405 #2C214D #36488A #355F8D #2E758C #228788 #189786 #2BA77D #79C151 #D0E649` |
| rocket | sequential | ✓ | ✗ | 深蓝到红，经紫 | `#03051A #100D3D #2A115F #441570 #5C1872 #741A70 #8C1D6C #A82262 #C52F54 #E14A45` |
| turbo | diverging | ✗ | ✗ | 改进版彩虹 | `#30123B #4145AB #4675ED #39A2FC #1BCFD4 #24EBA0 #61FC6C #A4FC3B #D1E834 #F3C63A #FE9B2D #F36315 #D93806 #B11901 #7A0402` |

---

## wesanderson (22+ palettes, all discrete)

Wes Anderson 电影风格调色板，适合创意和艺术可视化。

| 调色板 | 最大颜色数 | HEX 色值 | 灵感来源 |
|--------|-----------|---------|---------|
| Royal1 | 4 | `#899DA4 #C93312 #FAEFD1 #DC863B` | The Royal Tenenbaums |
| Royal2 | 5 | `#9A8822 #F5CDB4 #F8AFA8 #FDDDA0 #74A089` | The Royal Tenenbaums |
| Zissou1 | 5 | `#3B9AB2 #78B7C5 #EBCC2A #E1AF00 #F21A00` | The Life Aquatic |
| GrandBudapest1 | 5 | `#F4B0AA #BEAED4 #DEC6BE #E5D7BD #87A3A6` | The Grand Budapest Hotel |
| GrandBudapest2 | 4 | `#E6A0C4 #C6CDF7 #D8A499 #7294D1` | The Grand Budapest Hotel |
| Moonrise1 | 5 | `#F3DF6C #FFABCA #83B7A2 #F7881D #C5B4D2` | Moonrise Kingdom |
| Moonrise2 | 5 | `#E1BD6D #EABE94 #0B775E #35274A #F2300F` | Moonrise Kingdom |
| Moonrise3 | 5 | `#C6BEA4 #968175 #C2A38A #95BDA6 #F2BFD4` | Moonrise Kingdom |
| Cavalcanti1 | 5 | `#D8B70A #02401B #A2A475 #81A88D #972D15` | Hotel Chevalier |
| Cavalcanti2 | 6 | `#D8B70A #CD406C #B48F2D #6FCC5C #52445B #AC8A67` | Hotel Chevalier |
| Chevalier1 | 4 | `#446455 #FDD262 #D3DDDC #C7B19C` | Hotel Chevalier |
| Chevalier2 | 5 | `#8F9F1A #F8B01D #C19828 #47596D #9A6E3D` | Hotel Chevalier |
| FantasticFox1 | 5 | `#DD8D29 #E2D200 #46ACC8 #E58601 #B40F20` | Fantastic Mr. Fox |
| Darjeeling1 | 5 | `#FF0000 #00A08A #F2AD00 #F98400 #5BBCD6` | The Darjeeling Limited |
| Darjeeling2 | 5 | `#ECCBAE #046C9A #D69C4E #ABDDDE #000000` | The Darjeeling Limited |
| Darjeeling3 | 5 | `#ADAF4A #8F9F1A #F8B01D #C19828 #47596D` | The Darjeeling Limited |
| Rushmore1 | 5 | `#E1BD6D #EABE94 #0B775E #35274A #F2300F` | Rushmore |
| BottleRocket1 | 7 | `#A42820 #5F5647 #9B110E #3F5151 #4E2A1E #550307 #0C1707` | Bottle Rocket |
| BottleRocket2 | 5 | `#FAD510 #CB2314 #273046 #354823 #1E1E1E` | Bottle Rocket |
| IsleofDogs1 | 6 | `#9986A5 #79402E #CCBA72 #0F0D0E #D9D0D3 #8D8680` | Isle of Dogs |
| IsleofDogs2 | 6 | `#EAD3BF #AA9486 #B6854D #39312F #1C1718 #9986A5` | Isle of Dogs |
| FrenchDispatch | 4 | `#90D4CC #BD3027 #B0AFA2 #7FC0C6` | The French Dispatch |
| AsteroidCity1 | 5 | `#0A9F9D #C8B943 #8C8C8C #8C2A22 #665C7C` | Asteroid City |
| AsteroidCity2 | 5 | `#FBA72A #D3D4D8 #CB7A5C #5785C1 #94A9C0` | Asteroid City |
| AsteroidCity3 | 5 | `#FFC408 #BE6E22 #5785C1 #94A9C0 #8DAB54` | Asteroid City |

---

## nord (8 palettes, all discrete)

北欧风格调色板，冷色调为主。

| 调色板 | 最大颜色数 | HEX 色值 | 说明 |
|--------|-----------|---------|------|
| polarnight | 4 | `#2E3440 #3B4252 #434C5E #4C566A` | 极夜深蓝灰 |
| snowstorm | 3 | `#D8DEE9 #E5E9F0 #ECEFF4` | 暴风雪浅灰白 |
| frost | 4 | `#8FBCBB #88C0D0 #81A1C1 #5E81AC` | 冰霜蓝青 |
| aurora | 5 | `#BF616A #D08770 #EBCB8B #A3BE8C #B48EAD` | 极光暖色 |
| nord | 16 | `#2E3440 #3B4252 #434C5E #4C566A #D8DEE9 #E5E9F0 #ECEFF4 #8FBCBB #88C0D0 #81A1C1 #5E81AC #BF616A #D08770 #EBCB8B #A3BE8C #B48EAD` | 完整 16 色 |
| lumina | 15 | `#4C566A #4C566A #5E81AC #8FBCBB #88C0D0 #81A1C1 #81A1C1 #D8DEE9 #D8DEE9 #E5E9F0 #E5E9F0 #ECEFF4 #ECEFF4 #88C0D0 #81A1C1` | 亮色变体 |
| silver_mine | 11 | `#D8DEE9 #E5E9F0 #ECEFF4 #D08770 #EBCB8B #A3BE8C #B48EAD #8FBCBB #88C0D0 #81A1C1 #5E81AC` | 银矿混合 |
| victory_bonds | 5 | `#BF616A #D08770 #EBCB8B #A3BE8C #B48EAD` | 同 aurora |

---

## scico (14+ palettes, all continuous)

基于 Fabio Crameri 科学色彩图的调色板，**全部感知均匀且色盲友好**。适合学术出版物。

| 调色板 | 类别 | 印刷友好 | 说明 | 采样 HEX (n=10) |
|--------|------|---------|------|----------------|
| batlow | sequential | ✗ | 默认 scico 调色板，青到黄 | `#00121A #0A2837 #0F3B53 #10506A #136578 #1D7B81 #338F84 #56A282 #80B37C #B0C168` |
| batlowK | sequential | ✓ | batlow 深色变体 | `#0D0887 #3B049A #6304A7 #8B0AA5 #B52A8B #CC4778 #E16462 #F1844B #F8A835 #FBD324` |
| batlowW | sequential | ✓ | batlow 浅色变体 | `#9D9D9D #9F7E96 #A3648C #A94D83 #B13A7C #B82E72 #BD3264 #BB3D58 #B34E4D #A66145` |
| berlin | diverging | ✗ | 蓝到红发散 | `#9EB0FF #5AA3DA #2D7597 #194155 #11181D #270C01 #501802 #8A3F2A #C37469 #FFACAC` |
| broc | diverging | ✗ | 蓝到绿发散 | `#002447 #0F3D73 #1C5A8F #2B7CA9 #5BA7BD #A2D6BB #7FC075 #4E9B33 #28700C #004B00` |
| cork | diverging | ✗ | 蓝到棕发散 | `#002447 #194069 #335D7E #4E7B8D #6D9B96 #B8B8B8 #B0986B #9C7A41 #7D5E22 #574400` |
| davos | sequential | ✗ | 深到浅蓝 | `#001227 #0B2A40 #174059 #22576D #2D6E80 #488A98 #7AAFC2 #A8C6D8 #C8DEE9 #EAF2F8` |
| hawaii | sequential | ✗ | 紫到青，暖冷交替 | `#3B0F70 #8C2981 #C9399C #F060A4 #FA9C8C #FDC955 #F9F871 #A0E89D #42B8A0 #2A6E8E` |
| lapaz | diverging | ✗ | 深蓝到奶油 | `#190C64 #272A7D #354893 #43669F #5C7DA0 #90A198 #C7B59C #E5C9B3 #F7DFD3 #FEF2F2` |
| nuuk | sequential | ✗ | 深到浅青 | `#02151B #0C3142 #1A4D61 #2A697B #46859C #72A6C0 #9EC4DB #C2D8E8 #DDE7EE #F2F5F7` |
| oslo | sequential | ✓ | 黑到白灰度 | `#000000 #0B0D0F #1A1E23 #2D3138 #454A52 #646A73 #898F98 #AEB3BB #D2D6DC #FFFFFF` |
| roma | diverging | ✗ | 红到绿发散 | `#7C0A02 #B83A20 #E76B2E #F8A146 #F8C770 #C9B582 #9AAB62 #6B8E4D #3D6E3C #0F4D2C` |
| tokyo | sequential | ✗ | 深紫到浅 | `#040A0C #1C1D2E #362C44 #52405A #705670 #907287 #B0919F #CFB3B8 #E2D5D2 #F2EDED` |
| vik | diverging | ✗ | 蓝到橙发散 | `#00429D #2E59A8 #4771B2 #5D8ABD #7AA3C7 #A6BCE0 #D5D5DD #F5C7A9 #E58A33 #C04E00` |

> scico 共有 39 个调色板，以上列出最常用的 14 个。完整列表请运行 `scico::scico_palette_show()`。

---

## ggsci (9 palettes, all discrete)

科学期刊风格调色板，适合学术出版物和论文。

| 调色板 | 最大颜色数 | HEX 色值 | 灵感来源 |
|--------|-----------|---------|---------|
| npg | 10 | `#E64B35 #4DBBD5 #00A087 #3C5488 #F39B7F #8491B4 #91D1C2 #DC0000 #7E6148 #B09C85` | Nature Publishing Group |
| aaas | 10 | `#3B4992 #EE0000 #008B45 #631879 #008280 #BB0021 #5F559B #A20056 #808180 #1B1919` | Science (AAAS) |
| lancet | 9 | `#00468B #ED0000 #42B540 #0099B4 #925E9F #FDAF91 #AD002A #ADB6B6 #1B1919` | The Lancet |
| jco | 10 | `#0073C2 #EFC000 #868686 #CD534C #7AA6DC #00A1D5 #384E55 #CD534C #8F7700 #7AA6DC` | J. Clinical Oncology |
| ucscgb | 26 | `#FF0000 #FF9900 #FFCC00 #00FF00 #6699FF ...` | UCSC Genome Browser |
| d3 | 20 | `#1F77B4 #FF7F0E #2CA02C #D62728 #9467BD #8C564B #E377C2 #7F7F7F #BCBD22 #17BECF ...` | D3.js category20 |
| locuszoom | 7 | `#D43F3A #EEA236 #5CB85C #46B8DA #357EBD #9632B1 #B8B8B8` | LocusZoom (GWAS) |
| igv | 51 | `#5050FF #CE3D32 #749B58 #F0B828 #888888 #009E73 ...` | IGV |
| nejm | 8 | `#BC3C29 #0072B5 #E18727 #20854E #787D7D #6F99AD #FFDC91 #EE4C97` | NEJM |

---

## ghibli (8 palettes, all discrete)

吉卜力工作室电影风格调色板。

| 调色板 | 最大颜色数 | HEX 色值 | 灵感来源 |
|--------|-----------|---------|---------|
| MarnieLight1 | 10 | `#28231D #5E2D20 #884A39 #B07A56 #D6B371 #D7C79B #C9D7C0 #A9C8B9 #5C8B9D #2E526B` | 回忆中的玛妮 |
| MarnieLight2 | 10 | `#27251F #4E3D2C #884A39 #B07A56 #BA9463 #C3A478 #C9D7C0 #A9C8B9 #5C8B9D #2E526B` | 回忆中的玛妮 |
| PonyoLight | 10 | `#35373B #405663 #5783B3 #80A6CC #AACBE4 #DDEDF7 #D4E0D4 #D6BE9A #C28352 #8B4A2A` | 悬崖上的金鱼姬 |
| LaputaLight | 10 | `#221E1F #4E3B39 #815752 #9D7C65 #9A9277 #828A77 #637366 #54667D #3F5477 #2A3B59` | 天空之城 |
| SpiritedLight | 9 | `#2F3B3B #536C68 #8C9E87 #C6CDAF #A89F7E #8E5E2E #693D24 #4F2E1D #42302B` | 千与千寻 |
| YesterdayLight | 9 | `#403D2A #818559 #A6A97A #C5C9A0 #D4D7BA #E3E4CE #DCCE8F #C7A758 #A87E32` | 来自红花坂 |
| KikiLight | 10 | `#7B5247 #9F6C46 #B88953 #D6A86B #E8C879 #F2DD80 #C6C26B #8EA66B #5D7A6B #445566` | 魔女宅急便 |
| TotoroLight | 9 | `#1E2A2D #465660 #778C84 #94AB86 #C5B87C #C28352 #884A2A #552418 #2A1206` | 龙猫 |

---

## MetBrewer (26 palettes, all discrete)

大都会艺术博物馆藏品启发的调色板。

| 调色板 | 最大颜色数 | HEX 色值 | 灵感来源 |
|--------|-----------|---------|---------|
| Archambault | 10 | `#88A0DC #381A61 #7C4B73 #ED968C #AB3329 #E78429 #F9D14A #FFE38F #9DB7A5 #2A403A` | John Archambault |
| Austria | 6 | `#A40000 #16317D #007E2D #FFCD12 #B86092 #721B3E` | Gustav Klimt |
| Cassatt1 | 12 | `#B1615C #D88782 #E3AAA8 #C3D4DA #7BA0B4 #5481B0 #2E5A87 #0B2D56 #B6C2C5 #8A9B9F #5D7074 #42585C` | Mary Cassatt |
| Cassatt2 | 11 | `#2D223C #574571 #90719F #B695BC #DEC5DA #C1D1AA #7FA074 #466C4B #2C4B27 #0E2810 #B10101` | Mary Cassatt |
| Cross | 7 | `#C969A1 #CE4441 #EE8577 #F6B85B #9FAE5F #3E5641 #1F1F1F` | Charles Demuth |
| Degas | 11 | `#591D02 #8B541E #C7913B #DBC372 #5D7D74 #4D6A8C #6082A1 #84A0BF #B1BFD8 #B1BFD8 #D5C9C9` | Edgar Degas |
| Hiroshige | 7 | `#E76254 #EF8A47 #F7AA58 #FFD06F #FFE6B7 #AADCE0 #72BCD5` | 歌川広重 |
| Hokusai1 | 7 | `#6D2F20 #B75347 #DF7E66 #E09351 #EDC775 #94B594 #224B5E` | 葛飾北斎 |
| Hokusai2 | 8 | `#ABC9C8 #72AEB6 #4692B0 #2F70A1 #134B73 #0A3351 #0F1E2D #0C2A3F` | 葛飾北斎 |
| Hokusai3 | 7 | `#D8D97A #95C36E #74C8C3 #5A97C1 #295384 #0A2E57 #082241` | 葛飾北斎 |
| Ingres | 10 | `#041077 #1E3FA9 #1859B9 #3D89D5 #7BB6E8 #A6CDEA #DAE8F3 #F5CFA9 #E8B07A #C68C52` | Ingres |
| Isfahan1 | 6 | `#4E3D2C #845D29 #D8B847 #B8821B #75A9C0 #38667B` | Isfahan |
| Kandinsky | 10 | `#3B7C70 #CE9642 #3B3A3E #898E9F #A2CCEE #C8AC7D #75B4A0 #B05C5A #5E5D57 #D77B5C` | Kandinsky |
| Klimt | 8 | `#DF9ED4 #C93F55 #EACC62 #469D76 #3C4B99 #924099 #B25E51 #59A6D6` | Gustav Klimt |
| Laffique | 6 | `#C5343A #E39E54 #94B054 #247A3C #7B4E7C #3B3364` | Laffique |
| Monet | 11 | `#4E6D58 #749E89 #ABCCBE #E3CACF #C375A2 #9F4F80 #6D2C5B #3F0F30 #786996 #9894B1 #B6B2CE` | Claude Monet |
| Moreau | 10 | `#421600 #792504 #BC7524 #8DADCA #527BAF #36347F #959ECD #5E176F #0A0405 #8F7466` | Gustave Moreau |
| Nattier | 9 | `#52271C #944839 #C08E39 #E8B7E6 #B85390 #5C4A9C #466B8D #27355B #1E1B1E` | Nattier |
| O_Keeffe1 | 8 | `#6B200C #973D21 #DA6C42 #EE956A #FBC2A9 #F6F2EE #BAD6F9 #7FA5DA #4D72A9` | Georgia O'Keeffe |
| O_Keeffe2 | 8 | `#FBE3C2 #F2C88F #ECB27D #E69C6B #D37750 #A8543B #6E3B22 #3B2315` | Georgia O'Keeffe |
| Pissarro | 12 | `#134263 #1E5470 #4A7595 #559FA3 #8DBBA8 #A9C7A8 #D3D5A3 #ECE7A8 #D6BD82 #B68E66 #8E6741 #5E4220` | Pissarro |
| Redon | 9 | `#5B859E #1E395F #75884B #1E5A46 #DF8D71 #AF4F2F #D4B847 #9C5B22 #55220C` | Odilon Redon |
| Renoir | 10 | `#17154F #2F357C #6C5D9E #9D9CD5 #B0799A #F6B3B0 #E48171 #BF5F4A #808A87 #475B41` | Renoir |
| Robert | 5 | `#11341A #375624 #6B8939 #94A93A #D6CC2E` | Hubert Robert |
| Signac | 9 | `#E7345C #FF9500 #F7C200 #74CC66 #009CE0 #9E009E #5E5E5E #00575C #2E575C` | Paul Signac |
| Tam | 8 | `#8B2515 #CB443B #E69E55 #F2BC73 #828A37 #565D44 #343E33 #1B241E` | Wu Guanzhong |
| Troy | 10 | `#421401 #6c1d0e #8b3a2b #c27668 #7ba0b4 #44728c #2a475d #072B44 #d8a88a #e8d2c5` | de Troy |
| Tura | 8 | `#5E1B0E #802018 #A84027 #C36831 #DE9C44 #F4D65B #F9E9A4 #C5BFA0` | Cosimo Tura |
| Veronese | 8 | `#67322E #9E5E32 #A57E50 #C9A66B #E3D38C #4E7B4C #36636E #2E3F66` | Veronese |

---

## nationalparkcolors (24 palettes, all discrete)

美国国家公园启发的调色板，适合自然主题可视化。

| 调色板 | 最大颜色数 | HEX 色值 | 灵感来源 |
|--------|-----------|---------|---------|
| Arches | 7 | `#E69F00 #9E0142 #88CCEE #332288 #FEE08B #D53E4F #ABDDA4` | Arches NP |
| ArcticGates | 7 | `#109782 #65BC8D #82C6A3 #B5C99A #E8D892 #DCB360 #C4622D` | Arctic Gates |
| BlueRidgePkwy | 6 | `#004B8D #5D8CAE #94B4C3 #ABCD9E #84A96F #486B3A` | Blue Ridge Parkway |
| BryceCanyon | 6 | `#FAEFD1 #DC9445 #3E5C71 #2B2622 #9F5235 #F1B855` | Bryce Canyon NP |
| CraterLake | 7 | `#7DCCD3 #4272A6 #1E283B #3777B4 #82B4C2 #C16A4D #9F3F1E` | Crater Lake NP |
| Denali | 6 | `#73979D #6A8E94 #5B702F #3B5C36 #90A35F #C1B65E` | Denali NP |
| Everglades | 7 | `#91D5DE #2E8B9B #7DC8B5 #5C8A65 #9D9263 #B4A26B #6E5E3B` | Everglades NP |
| GeneralGrant | 6 | `#F7B500 #F0DA8E #D6C2AA #B07A4B #5B4E3C #3B3A36` | General Grant |
| Glacier | 7 | `#01353D #057D88 #46B0AF #E0C91C #8CC0AE #B36A45 #31180D` | Glacier NP |
| GrandCanyon | 7 | `#FAEFD1 #DC9445 #5C77A0 #3E5C71 #9F5235 #F1B855 #2B2622` | Grand Canyon NP |
| GrandTeton | 6 | `#F4E3C7 #73979D #94B59C #AF6E4D #A05E3A #644E3A` | Grand Teton NP |
| Hawaii | 7 | `#D67B40 #5B8C5A #F7C39D #94B6A1 #8E6C8A #CDB0D3 #3E3D3F` | Hawaii Volcanoes NP |
| IguazuFalls | 6 | `#756141 #A68E6A #D3B98E #C99A4C #88A04E #3B5233` | Iguazu Falls |
| KingsCanyon | 6 | `#85B3A2 #55988A #285D61 #46411C #766A35 #A4943A` | Kings Canyon NP |
| MammothCave | 6 | `#3D593F #87975C #E0CC79 #C2973D #77541E #2D1B10` | Mammoth Cave NP |
| MtMckinley | 7 | `#C9B589 #73979D #6A8E94 #5B702F #3B5C36 #90A35F #C1B65E` | Mt. McKinley |
| MtRainier | 7 | `#466D8E #8AB2C5 #F6E2B3 #D59988 #A07661 #5B3D33 #2D1B10` | Mt. Rainier NP |
| Olympic | 7 | `#1F4E5B #4F8C9C #82B5BD #C6C7B5 #87A26F #516D57 #364040` | Olympic NP |
| Redwoods | 7 | `#360F2B #864C78 #A18659 #D6B85C #B0C186 #3D6B54 #2A3A26` | Redwoods NP |
| Saguaro | 6 | `#137177 #188977 #2FA386 #F2C57A #DFA347 #B25E1D` | Saguaro NP |
| SmokyMtns | 6 | `#3A4D1C #6A8E3C #C9C870 #E6C86E #DC8E5A #A85F3A` | Great Smoky Mtns |
| Yellowstone | 7 | `#52796F #84A98C #CAD2C5 #F9C74F #F8961E #F3722C #F94144` | Yellowstone NP |
| Zion | 7 | `#8B232C #66411A #CC9B4C #EBCC6F #99AE8E #5B6E54 #2C3332` | Zion NP |

---

## 完整包列表 / Complete Package List

paletteer 共聚合 **79 个源包**，包含 **2893 个调色板**。以下列出所有源包及其在 paletteer 中的调色板类型分布：

| 源包 | CRAN | 调色板类型 | 说明 |
|------|------|-----------|------|
| RColorBrewer | ✓ | discrete | 经典 ColorBrewer (35) |
| viridis | ✓ | continuous | 感知均匀色彩图 (8) |
| wesanderson | ✓ | discrete | Wes Anderson 电影 (22+) |
| nord | ✓ | discrete | 北欧风格 (8) |
| rcartocolor | ✓ | discrete | CARTO 地图配色 (22) |
| scico | ✓ | continuous | 科学色彩图 (39) |
| ggsci | ✓ | discrete | 期刊配色 (9) |
| ghibli | ✓ | discrete | 吉卜力电影 (8+) |
| MetBrewer | ✓ | discrete | 大都会艺术 (26+) |
| nationalparkcolors | ✗ | discrete | 国家公园 (24) |
| PrettyCols | ✓ | discrete, continuous | 美学调色板 |
| ggprism | ✓ | discrete | GraphPad Prism 风格 |
| ggthemes | ✓ | discrete, dynamic | Tableau/Excel/Economist |
| khroma | ✓ | discrete, continuous | 考古学感知均匀 |
| pals | ✓ | discrete, continuous | 综合 50+ 调色板 |
| colorBlindness | ✓ | discrete, continuous | 色盲安全 |
| cartography | ✓ | dynamic | 主题制图 |
| harrypotter | ✓ | discrete | 哈利波特电影 |
| tvthemes | ✓ | discrete | 电视剧配色 |
| nbapalettes | ✓ | discrete | NBA 球队 |
| NatParksPalettes | ✓ | discrete | 国家公园扩展版 |
| dutchmasters | ✗ | discrete | 荷兰黄金时代绘画 |
| vangogh | ✓ | discrete | 梵高绘画 |
| calecopal | ✗ | discrete | 加州植物 |
| soilpalettes | ✗ | discrete | 土壤剖面 |
| fishualize | ✓ | discrete | 鱼类物种 |
| feathers | ✗ | discrete | 鸟类羽毛 |
| tayloRswift | ✗ | discrete | Taylor Swift 专辑 |
| beyonce | ✗ | discrete | Beyonce |
| vapoRwave | ✗ | discrete, continuous | 蒸汽波美学 |
| NineteenEightyR | ✗ | discrete | 80年代复古 |
| PNWColors | ✗ | discrete | 太平洋西北 |
| LaCroixColoR | ✗ | discrete | LaCroix 气泡水 |
| MoMAColors | ✗ | discrete | MoMA 展览 |
| awtools | ✗ | discrete | 现代简约 |
| trekcolors | ✓ | discrete | 星际迷航 |
| unikn | ✓ | discrete | 康斯坦茨大学品牌 |
| tidyquant | ✓ | discrete | 金融可视化 |
| rockthemes | ✗ | discrete | 摇滚乐队 |
| Polychrome | ✓ | discrete | 高色彩数量定性 |
| Rdune | ✓ | discrete | 沙丘 |
| Redmonder | ✓ | discrete | 微软 Redmond |
| amerika | ✓ | discrete | 美国政党 |
| yarrr | ✓ | discrete | 海盗主题 |

> 其余约 35 个包可通过 R 中 `paletteer::paletteer_packages` 查看完整列表。
