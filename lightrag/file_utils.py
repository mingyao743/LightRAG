import re, os
import jionlp as jio
from moviepy.editor import VideoFileClip
from bs4 import BeautifulSoup
from ebooklib import epub


def merge_newlines(text):
    return re.sub(r'\n+', '\n', text)

def clean_content(content):
    content = merge_newlines(content)
    content = content.strip()
    content = jio.remove_exception_char(content)
    content = jio.remove_redundant_char(content)
    return content

def percent_of_chinese(text):
    char_count = len(text)
    if char_count == 0:
        return 0.
      
    chinese_count = 0.
    for c in text:
        if jio.check_any_chinese_char(c):
            chinese_count += 1.
    return chinese_count / char_count

def download_video(url, out_dir):
    os.system(f'you-get -o {out_dir} {url}') # use you-get download video
    files = [os.path.join(our_dir, f) for f in os.listdir(outdir) if f.endswith('mp4')]
    return files

def extract_audio_from_video(video_path, out_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(out_path)

def extract_text_from_audio(audio_path):
    """ """

def extract_content_from_xhs(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    items = soup.find_all('div', {'class': 'note-content'})
    text = items[0].text if len(items) > 0 else ''
    return text

def parse_nav_points(nav_points, hrefs):
    nodes = []
    for nav_point in nav_points:
        if isinstance(nav_point, epub.Link) or isinstance(nav_point, epub.Section):
            title = nav_point.title
            href = nav_point.href
            children = []
        elif isinstance(nav_point, tuple):
            title = nav_point[0].title
            href = nav_point[0].href
            children = nav_point[1]
        else:
            title = None
            href = None
            Children = []

        if href is not None: hrefs.append(href)

        node = {'title': title, 'href': href}
        if len(children) != 0:
            children = parse_nav_points(children, hrefs)
            node['children'] = node
        nodes.append(node)
    return nodes

class EpubExtracter():
    def __init__(self, file_path):
        self.book = epub.read_epub(file_path)
        self.build_navigations()
        self.build_navi_content()

    def build_navigations(self):
        toc = self.book.toc
        hrefs = []
        self.navigatin = parse_nav_points(toc, hrefs)
        self.hrefs = hrefs
        print(f'{len(self.hrefs)} navigation links found')

    def extract_contnt(self, href, chunks):
        soup = BeautifulSoup(self.book.get_item_with_href(href).get_content())
        if len(chunks) == 0:
            content = soup.get_text()
            content = clean_content(content)
            return { href:[content] }
        elif len(chunks) == 1:
            content = soup.get_text()
            content = clean_content(content)
            return { href + '#' + chunks[0]: [content] }
        else:
            href_tags = {href:[]}
            cur_chunk = None
            for div in soup.find('body'):
                if div.name is None: continue
                if div.get('id') in chunks:
                    cur_chunk = div.get('id')
                    href_tags[href+'#'+cur_chunk] = []
    
                if cur_chunk is not None:
                    href_tags[href+'#'+cur_chunk].append(div)
                if cur_chunk is None:
                    href_tags[href].append(div)
    
            href_contents = {}
            for href, tags in href_tags.items():
                if len(tags) == 0:
                    continue
                tags = [clean_content(v.get_text().strip()) for v in tags]
                href_contents[href] = tags
    
            return href_contents

    def build_navi_content(self):
        href_chunks = {}
        for href in self.hrefs:
            chunk = None
            if '#' in href:
                href, chunk = href.split('#')
            
            if href not in href_chunks:
                href_chunks[href] = []
            if chunk is not None:
                href_chunks[href].append(chunk)

        href_contents = {}
        for href, chunks in href_chunks.items():
            part_href_contents = self.extract_content(href, chunks)
            for h, contents in part_href_contents.items():
                href_contents[h] = contents
                
        # match content to navigation tree
        def recur(ll):
            for l in ll:
                if l['href'] in href_contents:
                    l['content'] = '\n'.join(href_contents[l['href']])
                if 'children' in l:
                    recur(l['children'])
        recur(self.navigation)


