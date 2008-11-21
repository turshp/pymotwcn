#/usr/bin/python
#coding: utf-8
"""用 python-reportlab 将 rst 转换为中文 PDF
@see: http://wiki.woodpecker.org.cn/moin/UsageRstReportlabExPdf
"""

import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts
reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('song',  '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttf'))

import reportlab.lib.fonts
reportlab.lib.fonts.ps2tt = lambda psfn: ('song', 0, 0)
reportlab.lib.fonts.tt2ps = lambda fn,b,i: 'song'


## for CJK Wrap
import reportlab.platypus
def wrap(self, availWidth, availHeight):
    # work out widths array for breaking
    self.width = availWidth
    leftIndent = self.style.leftIndent
    first_line_width = availWidth - (leftIndent+self.style.firstLineIndent) - self.style.rightIndent
    later_widths = availWidth - leftIndent - self.style.rightIndent
    try:
        self.blPara = self.breakLinesCJK([first_line_width, later_widths])
    except:
        self.blPara = self.breakLines([first_line_width, later_widths])
    self.height = len(self.blPara.lines) * self.style.leading
    return (self.width, self.height)

reportlab.platypus.Paragraph.wrap = wrap
