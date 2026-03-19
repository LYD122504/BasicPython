from abc import ABC,abstractmethod
class TableFormatter(ABC):
    @abstractmethod
    def headings(self,headers):
        raise NotImplementedError()
    @abstractmethod
    def row(self,rowdata):
        raise NotImplementedError()
    
class TextTableFormatter(TableFormatter):
    def headings(self,headers):
        print(' '.join('%10s' % h for h in headers))
        print(('-'*10+' ')*len(headers))
    def row(self,rowdata):
        print(' '.join('%10s' % d for d in rowdata))

class CSVTableFormatter(TableFormatter):
    def headings(self,headers):
        print(','.join('%s' % h for h in headers))
    def row(self,rowdata):
        print(','.join('%s' % d for d in rowdata))

class HTMLTableFormatter(TableFormatter):
    def headings(self,headers):
        print('<tr>',end=' ')
        for h in headers:
            print('<th>%s</th>' % h,end=' ')
        print('</tr>')
    def row(self,rowdata):
        print('<tr>',end=' ')
        for r in rowdata:
            print('<td>%s</td>' % r,end=' ')
        print('</tr>')
class ColumnFormatMixin:
    formats=[]
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)
class PortfolioFormatter(ColumnFormatMixin,TextTableFormatter):
    formats=['%s','%d','%0.2f']
class UpperHeadersMixin:
    def headings(self,headers):
        super().headings([h.upper() for h in headers])
class UpperHeadersFormatter(UpperHeadersMixin,TextTableFormatter):
    pass
def create_formatter(name,column_formats=None,upper_headers=False):
    if name == 'text':
        formatter_cls = TextTableFormatter
    elif name == 'csv':
        formatter_cls = CSVTableFormatter
    elif name == 'html':
        formatter_cls = HTMLTableFormatter
    else:
        raise RuntimeError('Unknown format %s' % name)
    if column_formats:
         class formatter_cls(ColumnFormatMixin, formatter_cls):
              formats = column_formats
    if upper_headers:
        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass
    return formatter_cls()
def print_table(record,fields,formatter):
    if not isinstance(formatter,TableFormatter):
        raise TypeError("Expected a TableFormatter")
    formatter.headings(fields)
    for r in record:
        rowdata=[getattr(r,fieldname) for fieldname in fields]
        formatter.row(rowdata)
