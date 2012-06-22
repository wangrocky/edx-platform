import json
import logging

from lxml import etree

from x_module import XModule, XModuleDescriptor
from progress import Progress

log = logging.getLogger("mitx.courseware.modules")

class ModuleDescriptor(XModuleDescriptor):
    pass

class Module(XModule):
    id_attribute = 'youtube'
    video_time = 0

    def handle_ajax(self, dispatch, get):
        '''
        Handle ajax calls to this video.
        TODO (vshnayder): This is not being called right now, so the position
        is not being saved.
        '''
        log.debug(u"GET {0}".format(get))
        log.debug(u"DISPATCH {0}".format(dispatch))
        if dispatch == 'goto_position':
            self.position = int(float(get['position']))
            log.info(u"NEW POSITION {0}".format(self.position))
            return json.dumps({'success':True})
        raise Http404()

    def get_progress(self):
        ''' TODO (vshnayder): Get and save duration of youtube video, then return
        fraction watched.
        (Be careful to notice when video link changes and update)

        For now, we have no way of knowing if the video has even been watched, so
        just return None.
        '''
        return None

    def get_state(self):
        log.debug(u"STATE POSITION {0}".format(self.position))
        return json.dumps({ 'position': self.position })

    @classmethod
    def get_xml_tags(c):
        '''Tags in the courseware file guaranteed to correspond to the module'''
        return ["video"]

    def video_list(self):
        return self.youtube

    def get_html(self):
        return self.system.render_template('video.html', {
            'streams': self.video_list(),
            'id': self.item_id,
            'position': self.position,
            'name': self.name,
            'annotations': self.annotations,
        })

    def __init__(self, system, xml, item_id, state=None):
        XModule.__init__(self, system, xml, item_id, state)
        xmltree = etree.fromstring(xml)
        self.youtube = xmltree.get('youtube')
        self.name = xmltree.get('name')
        self.position = 0

        if state is not None:
            state = json.loads(state)
            if 'position' in state:
                self.position = int(float(state['position']))

        self.annotations=[(e.get("name"),self.render_function(e)) \
                      for e in xmltree]


class VideoSegmentDescriptor(XModuleDescriptor):
    pass
