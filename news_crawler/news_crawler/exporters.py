import logging
import posixpath
from ftplib import FTP

from scrapy.extensions import feedexport
from scrapy.utils.ftp import ftp_makedirs_cwd
from scrapy.utils.log import failure_to_exc_info
from twisted.internet import defer

from six.moves.urllib.parse import urlparse

logger = logging.getLogger(__name__)


class FTPFeedStorage(feedexport.BlockingFeedStorage):

    def __init__(self, uri):
        u = urlparse(uri)
        self.host = u.hostname
        self.port = int(u.port or '21')
        self.username = u.username
        self.password = u.password
        self.path = u.path

    def _store_in_thread(self, file):
        file.seek(0)
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(self.host, self.port)
        ftp.login(self.username, self.password)
        dirname, filename = posixpath.split(self.path)
        ftp_makedirs_cwd(ftp, dirname)
        ftp.storbinary('STOR %s' % filename, file)
        ftp.quit()


class MySpiderSlot(object):
    def __init__(self, file, exporter, storage, uri, exporting):
        self.file = file
        self.exporter = exporter
        self.storage = storage
        self.uri = uri
        self.itemcount = 0
        self.exporting = exporting


def store_all_slots(slots):
    for _, slot in slots.items():
        slot.storage.store(slot.file)


class FeedExporter(feedexport.FeedExporter):

    def __init__(self, settings):
        super().__init__(settings)
        self.slot_cache = {}

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        uri_list = set()
        total_itemcount = 0
        for _, slot in self.slot_cache.items():
            if not slot.itemcount and not self.store_empty:
                return
            if slot.exporting:
                slot.exporter.finish_exporting()
                slot.exporting = False
            total_itemcount += slot.itemcount
            uri_list.add(slot.uri)
        logfmt = "%s %%(format)s feed (%%(itemcount)d items) in: %%(uri)s"
        log_args = {'format': self.format,
                    'itemcount': total_itemcount,
                    'uri': uri_list}
        d = defer.maybeDeferred(store_all_slots, self.slot_cache)
        d.addCallback(lambda _: logger.info(logfmt % "Stored", log_args,
                                            extra={'spider': spider}))
        d.addErrback(lambda f: logger.error(logfmt % "Error storing", log_args,
                                            exc_info=failure_to_exc_info(f),
                                            extra={'spider': spider}))
        return d

    def item_scraped(self, item, spider):
        category = item['category']
        if category not in self.slot_cache:

            uri = self.urifmt % {'category': category,
                                 'starttime': spider.starttime}

            storage = self._get_storage(uri)
            file = storage.open(spider)
            exporter = self._get_exporter(file,
                                          fields_to_export=self.export_fields,
                                          encoding=self.export_encoding,
                                          indent=self.indent)
            self.slot_cache[category] = MySpiderSlot(
                file, exporter, storage, uri, False)

        slot = self.slot_cache[category]
        if self.store_empty:
                exporter.start_exporting()
                slot.exporting = True

        if not slot.exporting:
            slot.exporter.start_exporting()
            slot.exporting = True
        slot.exporter.export_item(item)
        slot.itemcount += 1
        return item
