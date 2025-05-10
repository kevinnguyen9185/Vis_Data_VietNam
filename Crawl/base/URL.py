# USER = 'bwt90798@zslsz.com'
USER = 'hunggs.no7.aws1@gmail.com'
PASSWORD = 'password1'

URL_CAFE = {
    "CLOSE": "https://s.cafef.vn/Lich-su-giao-dich-SYMBOL-1.chn#data",
    "CLOSE_FUND": "https://s.cafef.vn/Lich-su-giao-dich-SYMBOL-5.chn#data",
    "CLOSE_DETAIL":"https://s.cafef.vn/Lich-su-giao-dich-SYMBOL-2.chn#data",
    "FINANCIAL":"https://s.cafef.vn/bao-cao-tai-chinh/SYMBOL/IncSta/TIME/ket-qua-hoat-dong-kinh-doanh-cong-ty-co-phan-nhua-an-phat-xanh.chn",
    "DIVIDEND":"https://s.cafef.vn/hose/SYMBOL-cong-ty-co-phan-nhua-an-phat-xanh.chn",
    "VOLUME_NOW":"https://s.cafef.vn/hose/SYMBOL-cong-ty-co-phan-nhua-an-phat-xanh.chn",
    "VOLUME_EVENT":"https://s.cafef.vn/Ajax/Events_RelatedNews_New.aspx?symbol=*&floorID=0&configID=4&PageIndex=1&PageSize=1000&Type=2",
    "LIST_DELIST":"https://s.cafef.vn/du-lieu-doanh-nghiep.chn",
}

URL_STOCK_BIZ = {
  "CLOSE":"https://www.stockbiz.vn/Stocks/SYMBOL/LookupQuote.aspx?Date="
}

URL_TVSI = {
  "CLOSE":"https://finance.tvsi.com.vn/Enterprises/LichsugiaSymbolPart2?symbol=SYMBOL&currentPage=PAGE&duration=d&startDate=DATE_START&endDate=DATE_END",
  "BALANCE_SHEET_QUARTER":"https://finance.tvsi.com.vn/Enterprises/BangCanDoiKeToan?symbol=SYMBOL&YearView=YEAR&period=2&donvi=1",
  "INCOME_STATEMENT_QUARTER":"https://finance.tvsi.com.vn/Enterprises/BaoCaoKetQuaKd?symbol=SYMBOL&YearView=YEAR&period=2&donvi=1",
  "BALANCE_SHEET_YEAR":"https://finance.tvsi.com.vn/Enterprises/BangCanDoiKeToan?symbol=SYMBOL&YearView=YEAR&period=1&donvi=1",
  "INCOME_STATEMENT_YEAR":"https://finance.tvsi.com.vn/Enterprises/BaoCaoKetQuaKd?symbol=SYMBOL&YearView=YEAR&period=1&donvi=1",
  # "CASH_FLOWS_INDIRECT":"https://finance.tvsi.com.vn/Enterprises/LuuChuyenTienTegiantiep?symbol=AAA&YearView=2022&period=2&donvi=1",
  # "CASH_FLOWS_DIRECT":"https://finance.tvsi.com.vn/Enterprises/LuuChuyenTienTe?symbol=AAA&YearView=2022&period=2&donvi=1",
}

URL_VIETSTOCK = {
    "LOGIN":  "https://finance.vietstock.vn/",
    "CLOSE":"",
    "DIVIDEND":"https://finance.vietstock.vn/lich-su-kien.htm?page=1",
    "CASH_DIVIDEND":"https://finance.vietstock.vn/lich-su-kien.htm?page=1&tab=1&group=13",
    "BONUS_SHARE":"https://finance.vietstock.vn/lich-su-kien.htm?page=1&tab=1&group=14",
    "STOCK_DIVIDEND":"https://finance.vietstock.vn/lich-su-kien.htm?page=1&tab=1&group=15",
    "ADDITIONAL_LISTING":"https://finance.vietstock.vn/lich-su-kien.htm?page=1&tab=2&code=SYMBOL&group=21#",
    "TREASURY_STOCK_TRANSACTIONS":"https://finance.vietstock.vn/giao-dich-noi-bo?page=1&tab=5&code=SYMBOL",
    "COMPANY_DELISTING":"https://finance.vietstock.vn/lich-su-kien.htm?page=1&tab=2&code=SYMBOL&group=18",
    "LIST_INFOR":"https://finance.vietstock.vn/SYMBOL/ho-so-doanh-nghiep.htm",
    "LISTING": "https://finance.vietstock.vn/doanh-nghiep-a-z?page=1",
    "LISTING_PTC": "https://finance.vietstock.vn/doanh-nghiep-a-z/doanh-nghiep-phi-tai-chinh?page=1",
    "LISTING_NH": "https://finance.vietstock.vn/doanh-nghiep-a-z/ngan-hang?page=1",
    "LISTING_CK": "https://finance.vietstock.vn/doanh-nghiep-a-z/chung-khoan?page=1",
    "LISTING_BH": "https://finance.vietstock.vn/doanh-nghiep-a-z/bao-hiem?page=1",
    "DELISTING":"https://finance.vietstock.vn/doanh-nghiep-a-z/huy-niem-yet?page=1",
    "BALANCE_SHEET":'https://finance.vietstock.vn/SYMBOL/tai-chinh.htm?tab=CDKT',
    'INCOME_STATEMENT':"https://finance.vietstock.vn/SYMBOL/tai-chinh.htm?tab=KQKD",
    'CASH_FLOWS':"https://finance.vietstock.vn/SYMBOL/tai-chinh.htm?tab=LC",
}

URL_68 = {
  "LINK_ALL_COMPANY":'https://www.cophieu68.vn/companylist.php?currentPage=PAGE&o=s&ud=a',
  "CLOSE":"https://www.cophieu68.vn/historyprice.php?currentPage=PAGE&id=SYMBOL",
  "INCOME_STATEMENT":"https://www.cophieu68.vn/financial_income.php?id=SYMBOL",
  "BALANCE_SHEET":"https://www.cophieu68.vn/financial_balance.php?view=bs&id=SYMBOL",
  "VOLUME_EVENT":"https://www.cophieu68.vn/financial_income.php?id=SYMBOL&view=ist&year=YEAR",
  "DIVIDEND":'https://www.cophieu68.vn/eventschedule.php?id=SYMBOL',
}